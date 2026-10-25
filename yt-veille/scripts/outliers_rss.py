"""Outliers des chaînes de référence, par les flux RSS YouTube (stdlib, sans clé API).

Pour chaque chaîne de config/channels.json (clé « channels » seulement) : flux RSS
(15 dernières vidéos, Shorts compris), médiane des vues de la chaîne. Outlier =
vidéo publiée il y a --min-days à --max-days jours (jours entiers, bornes comprises),
avec au moins --min-views vues et au moins --ratio fois la médiane de sa chaîne.

Écrit outputs/veille-<AAAA-MM-JJ>-outliers.md (remplace celui du jour) : méthode,
puis tableau trié par ratio décroissant. La section « Thèmes » reste à rédiger
(Claude, en lisant le tableau). Indépendant de la veille automatique : ni API, ni veille.db.

    python outliers_rss.py                     # 2×, 2 000 vues, 2 à 30 jours
    python outliers_rss.py --ratio 3 --stdout  # affiche au lieu d'écrire
"""
import argparse
import http.client
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CHANNELS_PATH = SCRIPT_DIR / "config" / "channels.json"
OUTPUTS_DIR = SCRIPT_DIR.parent / "outputs"

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
TIMEOUT = 20   # secondes par requête
RETRIES = 2    # nouvelles tentatives par chaîne : le flux renvoie parfois 404/5xx à tort
WORKERS = 8

MIN_DAYS, MAX_DAYS, MIN_VIEWS, RATIO = 2, 30, 2000, 2.0  # valeurs du passage du 2026-10-14

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}
NNBSP = "\u202f"  # espace fine insécable entre les milliers, comme dans le rapport du 2026-10-14
# Contrôles bidi invisibles (YouTube en met autour des @mentions) : supprimés des cellules.
BIDI_CONTROLS = dict.fromkeys([0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A)])
RETRYABLE = (OSError, http.client.HTTPException, ET.ParseError, ValueError)


# --- Calcul (sans réseau) ---

def _parse_date(text: str | None) -> datetime | None:
    try:
        dt = datetime.fromisoformat(text.strip())
    except (AttributeError, ValueError):
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _parse_int(text: str | None) -> int | None:
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def parse_feed(xml_data: str | bytes) -> list[dict]:
    """Entrées d'un flux RSS YouTube : video_id, title, published (UTC), views (None si absent), short.

    Lève ET.ParseError si le XML est illisible, ValueError si ce n'est pas un flux Atom.
    """
    root = ET.fromstring(xml_data)
    if root.tag != f"{{{NS['atom']}}}feed":
        raise ValueError(f"pas un flux Atom (racine {root.tag!r})")
    entries = []
    for entry in root.findall("atom:entry", NS):
        video_id = (entry.findtext("yt:videoId", "", NS)
                    or entry.findtext("atom:id", "", NS).removeprefix("yt:video:")).strip()
        published = _parse_date(entry.findtext("atom:published", None, NS))
        if not video_id or published is None:
            continue
        title = entry.findtext("atom:title", "", NS) or entry.findtext("media:group/media:title", "", NS)
        stats = entry.find("media:group/media:community/media:statistics", NS)
        link = entry.find("atom:link[@rel='alternate']", NS)
        entries.append({
            "video_id": video_id,
            "title": " ".join(title.split()),
            "published": published,
            "views": _parse_int(stats.get("views")) if stats is not None else None,
            "short": link is not None and "/shorts/" in link.get("href", ""),
        })
    return entries


def median_views(entries: list[dict]) -> float | None:
    """Médiane des vues des entrées qui en ont ; None s'il n'y en a aucune."""
    views = [e["views"] for e in entries if e["views"] is not None]
    return statistics.median(views) if views else None


def select_outliers(entries: list[dict], *, now: datetime, min_days: int = MIN_DAYS,
                    max_days: int = MAX_DAYS, min_views: int = MIN_VIEWS,
                    ratio: float = RATIO) -> list[dict]:
    """Outliers d'une chaîne : entrées complétées de age_days, median et ratio.

    Âge en jours entiers (24 h écoulées = 1 jour) ; toutes les bornes sont comprises.
    """
    median = median_views(entries)
    if not median:  # aucune vue lisible, ou médiane nulle
        return []
    found = []
    for e in entries:
        if e["views"] is None:
            continue
        age_days = (now - e["published"]).days
        r = e["views"] / median
        if min_days <= age_days <= max_days and e["views"] >= min_views and r >= ratio:
            found.append({**e, "age_days": age_days, "median": median, "ratio": r})
    return found


def collect_outliers(feeds: list[tuple[dict, list[dict]]], *, now: datetime, **criteria) -> list[dict]:
    """Outliers de toutes les chaînes (couples chaîne de channels.json, entrées), ratio décroissant."""
    rows = []
    for channel, entries in feeds:
        for o in select_outliers(entries, now=now, **criteria):
            rows.append({**o, "channel": channel.get("handle", channel["channel_id"]),
                         "market": channel.get("market", "?")})
    rows.sort(key=lambda r: (-r["ratio"], -r["views"], r["video_id"]))
    return rows


# --- Markdown ---

def fmt_int(n: float) -> str:
    """300085 → « 300 085 » (espace fine insécable)."""
    return f"{round(n):,}".replace(",", NNBSP)


def md_escape(text: str) -> str:
    """Texte sur une ligne, sans ce qui casserait une cellule de tableau ou un lien Markdown."""
    text = " ".join(str(text).translate(BIDI_CONTROLS).split())
    for ch in "\\`*<[]|":  # la barre oblique inverse d'abord
        text = text.replace(ch, "\\" + ch)
    return text


def video_url(row: dict) -> str:
    path = "shorts/" if row.get("short") else "watch?v="
    return f"https://www.youtube.com/{path}{row['video_id']}"


def render_markdown(rows: list[dict], *, day: str, n_channels: int, n_read: int,
                    errors: list[tuple[str, str]] = (), markets: list[str] = ("FR", "US", "ES"),
                    per_channel: int = 15, min_days: int = MIN_DAYS, max_days: int = MAX_DAYS,
                    min_views: int = MIN_VIEWS, ratio: float = RATIO) -> str:
    """Rapport au format de outputs/veille-2026-10-14-outliers.md, section « Thèmes » à rédiger."""
    source = f"des {n_channels} chaînes" if n_read == n_channels else f"de {n_read} des {n_channels} chaînes"
    ratio_txt = f"{ratio:g}".replace(".", ",")
    n = len(rows)
    lines = [
        f"# Veille du {day} : outliers des {n_channels} chaînes de référence",
        "",
        f"Méthode : flux RSS {source} de `channels.json` ({per_channel} dernières vidéos chacune, "
        f"Shorts compris), médiane de vues par chaîne, outlier = vidéo publiée il y a {min_days} "
        f"à {max_days} jours faisant au moins {ratio_txt}× la médiane de sa chaîne et au moins "
        f"{fmt_int(min_views)} vues. {n} outlier{'s' if n > 1 else ''}.",
    ]
    if errors:
        listed = " ; ".join(f"{md_escape(name)} ({md_escape(msg)})" for name, msg in errors)
        lines += ["", f"Chaînes en erreur ({len(errors)}) : {listed}."]
    lines += [
        "",
        f"## Thèmes qui ressortent ({', '.join(markets)} ensemble)",
        "",
        "_À rédiger par Claude en lisant le tableau ci-dessous._",
        "",
        "## Tableau complet",
        "",
        "| Ratio | Vues | Médiane chaîne | Âge | Marché | Chaîne | Vidéo |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['ratio']:.1f}× | {fmt_int(r['views'])} | {fmt_int(r['median'])} | {r['age_days']} j "
            f"| {md_escape(r['market'])} | {md_escape(r['channel'])} "
            f"| [{md_escape(r['title'])}]({video_url(r)}) |"
        )
    return "\n".join(lines) + "\n"


# --- Réseau ---

def fetch_feed(channel_id: str) -> bytes:
    request = urllib.request.Request(FEED_URL.format(channel_id), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read()


def describe_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}"
    if isinstance(exc, urllib.error.URLError):
        return f"réseau : {exc.reason}"
    return f"{type(exc).__name__} : {exc}"


def load_channel(channel_id: str) -> tuple[list[dict] | None, str | None]:
    """(entrées, None) si le flux est lu, (None, message) sinon. Ne lève pas."""
    error = None
    for attempt in range(RETRIES + 1):
        if attempt:
            time.sleep(attempt)
        try:
            return parse_feed(fetch_feed(channel_id)), None
        except RETRYABLE as exc:
            error = describe_error(exc)
        except Exception as exc:  # imprévu : signalé sans arrêter les autres chaînes
            return None, describe_error(exc)
    return None, error


# --- CLI ---

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Outliers des chaînes de référence (flux RSS YouTube, sans clé API).")
    parser.add_argument("--min-days", type=int, default=MIN_DAYS,
                        help="âge minimum en jours (défaut : %(default)s)")
    parser.add_argument("--max-days", type=int, default=MAX_DAYS,
                        help="âge maximum en jours (défaut : %(default)s)")
    parser.add_argument("--min-views", type=int, default=MIN_VIEWS,
                        help="vues minimum (défaut : %(default)s)")
    parser.add_argument("--ratio", type=float, default=RATIO,
                        help="vues / médiane de la chaîne, minimum (défaut : %(default)s)")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--out", type=Path,
                        help="fichier à écrire (défaut : yt-veille/outputs/veille-<date>-outliers.md)")
    output.add_argument("--stdout", action="store_true",
                        help="afficher le Markdown au lieu d'écrire un fichier")
    args = parser.parse_args(argv)
    if args.min_days > args.max_days:
        parser.error("--min-days doit être inférieur ou égal à --max-days")
    if args.ratio <= 0:
        parser.error("--ratio doit être positif")
    return args


def main(argv: list[str] | None = None, now: datetime | None = None) -> int:
    args = parse_args(argv)
    log = sys.stderr if args.stdout else sys.stdout  # --stdout : la sortie standard ne porte que le Markdown
    with open(CHANNELS_PATH, encoding="utf-8") as f:
        channels = json.load(f).get("channels", [])
    if not channels:
        print(f"Aucune chaîne dans {CHANNELS_PATH}", file=sys.stderr)
        return 1

    now = now or datetime.now(timezone.utc)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(load_channel, [ch["channel_id"] for ch in channels]))

    feeds, errors = [], []
    for channel, (entries, error) in zip(channels, results):
        if error is None:
            feeds.append((channel, entries))
        else:
            name = channel.get("handle", channel["channel_id"])
            errors.append((name, error))
            print(f"Erreur : {name} ({channel['channel_id']}) : {error}", file=log)
    if not feeds:
        print("Aucun flux lu : rien n'est écrit.", file=sys.stderr)
        return 1

    criteria = {"min_days": args.min_days, "max_days": args.max_days,
                "min_views": args.min_views, "ratio": args.ratio}
    rows = collect_outliers(feeds, now=now, **criteria)
    day = date.today().isoformat()
    markdown = render_markdown(
        rows, day=day, n_channels=len(channels), n_read=len(feeds), errors=errors,
        markets=list(dict.fromkeys(ch.get("market", "?") for ch in channels)),
        per_channel=max(len(entries) for _, entries in feeds), **criteria,
    )

    if args.stdout:
        sys.stdout.write(markdown)
    else:
        out = args.out or OUTPUTS_DIR / f"veille-{day}-outliers.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
    n_videos = sum(len(entries) for _, entries in feeds)
    n_shorts = sum(r["short"] for r in rows)
    print(f"Chaînes lues : {len(feeds)}/{len(channels)}, en erreur : {len(errors)} "
          f"({fmt_int(n_videos)} vidéos). Outliers : {len(rows)} (dont {n_shorts} Shorts).", file=log)
    if not args.stdout:
        print(f"Fichier : {out.resolve()}", file=log)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):  # consoles Windows en cp1252 : titres avec emojis
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
