import json
import re
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import pytest

import outliers_rss
from outliers_rss import (
    collect_outliers, fmt_int, load_channel, main, md_escape, median_views,
    parse_feed, render_markdown, select_outliers,
)

NOW = datetime(2026, 10, 25, 12, 0, tzinfo=timezone.utc)

# Flux réduit, même structure que https://www.youtube.com/feeds/videos.xml?channel_id=...
FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">
 <title>Chaîne Test</title>
 <entry>
  <id>yt:video:vid00000001</id>
  <yt:videoId>vid00000001</yt:videoId>
  <title>Bitcoin : le  vrai
   signal 🚀</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=vid00000001"/>
  <published>2026-10-20T10:00:00+00:00</published>
  <media:group>
   <media:title>Bitcoin : le vrai signal 🚀</media:title>
   <media:community>
    <media:starRating count="120" average="5.00" min="1" max="5"/>
    <media:statistics views="12000"/>
   </media:community>
  </media:group>
 </entry>
 <entry>
  <id>yt:video:sho00000002</id>
  <yt:videoId>sho00000002</yt:videoId>
  <title>Un Short</title>
  <link rel="alternate" href="https://www.youtube.com/shorts/sho00000002"/>
  <published>2026-10-18T08:30:00+00:00</published>
  <media:group><media:community><media:statistics views="3000"/></media:community></media:group>
 </entry>
 <entry>
  <id>yt:video:live0000003</id>
  <yt:videoId>live0000003</yt:videoId>
  <title>Live à venir</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=live0000003"/>
  <published>2026-10-24T18:00:00+00:00</published>
  <media:group><media:title>Live à venir</media:title></media:group>
 </entry>
 <entry>
  <id>yt:video:vid00000004</id>
  <title>Ethereum | AMA [partie 1</title>
  <published>2026-09-01T12:00:00+00:00</published>
  <media:group><media:community><media:statistics views="1000"/></media:community></media:group>
 </entry>
 <entry>
  <title>Sans identifiant : ignorée</title>
  <published>2026-10-01T00:00:00+00:00</published>
 </entry>
</feed>
"""


def entry(video_id, views, age, short=False, title=None):
    """Entrée comme celles de parse_feed, publiée il y a `age` (jours ou timedelta)."""
    age = age if isinstance(age, timedelta) else timedelta(days=age)
    return {"video_id": video_id, "title": title or video_id, "published": NOW - age,
            "views": views, "short": short}


def cells(row):
    """Cellules d'une ligne de tableau GFM (les « \\| » ne séparent pas)."""
    return [c.strip() for c in re.split(r"(?<!\\)\|", row)[1:-1]]


# --- parse_feed ---

def test_parse_feed_reads_entries():
    entries = parse_feed(FEED)
    assert [e["video_id"] for e in entries] == ["vid00000001", "sho00000002", "live0000003", "vid00000004"]
    first = entries[0]
    assert first["title"] == "Bitcoin : le vrai signal 🚀"
    assert first["published"] == datetime(2026, 10, 20, 10, 0, tzinfo=timezone.utc)
    assert first["views"] == 12000
    assert first["short"] is False


def test_parse_feed_short_missing_stats_and_id_fallback():
    entries = {e["video_id"]: e for e in parse_feed(FEED.encode("utf-8"))}
    assert entries["sho00000002"]["short"] is True
    assert entries["live0000003"]["views"] is None
    assert entries["vid00000004"]["title"] == "Ethereum | AMA [partie 1"  # id lu dans <id>


def test_parse_feed_rejects_other_documents():
    with pytest.raises(ValueError):
        parse_feed("<html><body>consent</body></html>")
    with pytest.raises(ET.ParseError):
        parse_feed("<feed><entry>")


# --- median_views ---

def test_median_views_ignores_missing_views():
    assert median_views([entry("a", 100, 3), entry("b", 300, 3), entry("c", 200, 3)]) == 200
    assert median_views([entry("a", 100, 3), entry("b", 400, 3), entry("c", None, 3)]) == 250
    assert median_views([entry("a", None, 3)]) is None
    assert median_views([]) is None


# --- select_outliers ---

def test_select_outliers_on_parsed_feed():
    # vues lisibles 12000, 3000, 1000 : médiane 3000 ; seule la première fait 2x, 2 000 vues, 2 à 30 jours
    outliers = select_outliers(parse_feed(FEED), now=NOW)
    assert [o["video_id"] for o in outliers] == ["vid00000001"]
    assert outliers[0]["median"] == 3000
    assert outliers[0]["ratio"] == pytest.approx(4.0)
    assert outliers[0]["age_days"] == 5


def test_select_outliers_age_bounds_in_whole_days():
    normal = [entry(f"n{i}", 1000, 10) for i in range(6)]
    hits = [
        entry("1j23h", 10000, timedelta(days=1, hours=23)),
        entry("2j", 10000, 2),
        entry("30j22h", 10000, timedelta(days=30, hours=22)),
        entry("31j", 10000, 31),
    ]
    found = select_outliers(normal + hits, now=NOW, min_days=2, max_days=30)
    assert sorted(o["video_id"] for o in found) == ["2j", "30j22h"]
    assert {o["age_days"] for o in found} == {2, 30}


def test_select_outliers_min_views():
    entries = [entry(f"n{i}", 300, 10) for i in range(5)] + [entry("hit", 1500, 5)]  # 5x la médiane
    assert select_outliers(entries, now=NOW, min_views=2000) == []
    assert [o["video_id"] for o in select_outliers(entries, now=NOW, min_views=1000)] == ["hit"]


def test_select_outliers_ratio_threshold():
    entries = [entry(f"n{i}", 1000, 10) for i in range(5)] + [entry("x2", 2000, 5), entry("x199", 1990, 5)]
    assert [o["video_id"] for o in select_outliers(entries, now=NOW, min_views=0, ratio=2)] == ["x2"]
    assert select_outliers(entries, now=NOW, min_views=0, ratio=3) == []


def test_select_outliers_zero_median():
    entries = [entry("a", 0, 5), entry("b", 0, 5), entry("c", 5000, 5)]
    assert select_outliers(entries, now=NOW) == []


def test_collect_outliers_sorted_and_tagged():
    fr = {"handle": "Chaîne FR", "channel_id": "UC1", "market": "FR"}
    us = {"handle": "Chaîne US", "channel_id": "UC2", "market": "US"}
    feeds = [
        (fr, [entry(f"f{i}", 1000, 10) for i in range(5)] + [entry("fr3x", 3000, 4)]),
        (us, [entry(f"u{i}", 1000, 10) for i in range(5)] + [entry("us5x", 5000, 6)]),
    ]
    rows = collect_outliers(feeds, now=NOW)
    assert [(r["video_id"], r["channel"], r["market"]) for r in rows] == [
        ("us5x", "Chaîne US", "US"), ("fr3x", "Chaîne FR", "FR")]


# --- Markdown ---

def test_fmt_int_and_md_escape():
    assert fmt_int(300085) == "300\u202f085"
    assert fmt_int(478) == "478"
    assert fmt_int(4267.5) == "4\u202f268"
    assert md_escape("Seiya | Crypto & Finance") == "Seiya \\| Crypto & Finance"
    assert md_escape("Sell [Here's  The Case]\n") == "Sell \\[Here's The Case\\]"
    assert md_escape("Gold Is F*CKED (avec \u2068@Hasheur\u2069)") == "Gold Is F\\*CKED (avec @Hasheur)"


def test_render_markdown_format():
    channel = {"handle": "Seiya | Crypto & Finance", "channel_id": "UC1", "market": "FR"}
    # vues 12000, 3000, 1000 (flux) + 9000, 1500, 1500 : médiane 2250
    entries = parse_feed(FEED) + [
        entry("sho00000009", 9000, 3, short=True, title="Short | test [1"),
        entry("n1", 1500, 10), entry("n2", 1500, 10),
    ]
    rows = collect_outliers([(channel, entries)], now=NOW)
    md = render_markdown(rows, day="2026-10-25", n_channels=1, n_read=1, markets=["FR"])
    lines = md.splitlines()

    assert lines[0] == "# Veille du 2026-10-25 : outliers des 1 chaînes de référence"
    assert lines[2].startswith("Méthode : flux RSS des 1 chaînes de `channels.json` (15 dernières vidéos")
    assert "publiée il y a 2 à 30 jours faisant au moins 2× la médiane" in lines[2]
    assert "au moins 2\u202f000 vues. 2 outliers." in lines[2]
    assert "## Thèmes qui ressortent (FR ensemble)" in lines
    assert "_À rédiger par Claude en lisant le tableau ci-dessous._" in lines
    header = lines.index("| Ratio | Vues | Médiane chaîne | Âge | Marché | Chaîne | Vidéo |")
    assert lines[header + 1] == "|---|---|---|---|---|---|---|"

    table = lines[header + 2:]
    assert table == [
        "| 5.3× | 12\u202f000 | 2\u202f250 | 5 j | FR | Seiya \\| Crypto & Finance "
        "| [Bitcoin : le vrai signal 🚀](https://www.youtube.com/watch?v=vid00000001) |",
        "| 4.0× | 9\u202f000 | 2\u202f250 | 3 j | FR | Seiya \\| Crypto & Finance "
        "| [Short \\| test \\[1](https://www.youtube.com/shorts/sho00000009) |",
    ]
    assert all(len(cells(row)) == 7 for row in table)


def test_render_markdown_lists_errors_and_singular():
    md = render_markdown([], day="2026-10-25", n_channels=2, n_read=1, errors=[("Foo", "HTTP 404")])
    assert "flux RSS de 1 des 2 chaînes" in md
    assert "0 outlier." in md
    assert "Chaînes en erreur (1) : Foo (HTTP 404)." in md


# --- Réseau simulé ---

def test_load_channel_reports_error_without_raising(monkeypatch):
    calls = []

    def failing_fetch(channel_id):
        calls.append(channel_id)
        raise urllib.error.HTTPError("https://example.invalid", 404, "Not Found", None, None)

    monkeypatch.setattr(outliers_rss, "fetch_feed", failing_fetch)
    monkeypatch.setattr(outliers_rss.time, "sleep", lambda s: None)
    assert load_channel("UCx") == (None, "HTTP 404")
    assert len(calls) == outliers_rss.RETRIES + 1


def test_load_channel_parses_feed(monkeypatch):
    monkeypatch.setattr(outliers_rss, "fetch_feed", lambda cid: FEED.encode("utf-8"))
    entries, error = load_channel("UC1")
    assert error is None and len(entries) == 4


@pytest.fixture
def two_channels(tmp_path, monkeypatch):
    config = tmp_path / "channels.json"
    config.write_text(json.dumps({"channels": [
        {"handle": "Chaîne OK", "channel_id": "UC_OK", "market": "FR"},
        {"handle": "Chaîne KO", "channel_id": "UC_KO", "market": "US"},
    ], "exclus": [{"handle": "Ignorée", "channel_id": "UC_EXCLU"}]}), encoding="utf-8")
    monkeypatch.setattr(outliers_rss, "CHANNELS_PATH", config)
    monkeypatch.setattr(outliers_rss, "load_channel", lambda cid: (
        (parse_feed(FEED), None) if cid == "UC_OK" else (None, "HTTP 500")))


def test_main_writes_report_and_summary(two_channels, tmp_path, capsys):
    out = tmp_path / "rapport.md"
    assert main(["--out", str(out)], now=NOW) == 0
    md = out.read_text(encoding="utf-8")
    assert "flux RSS de 1 des 2 chaînes" in md
    assert "Chaînes en erreur (1) : Chaîne KO (HTTP 500)." in md
    assert "watch?v=vid00000001" in md
    printed = capsys.readouterr().out
    assert "Erreur : Chaîne KO (UC_KO) : HTTP 500" in printed
    assert "Chaînes lues : 1/2, en erreur : 1" in printed
    assert "Outliers : 1 (dont 0 Shorts)" in printed


def test_main_stdout_writes_no_file(two_channels, tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(outliers_rss, "OUTPUTS_DIR", tmp_path / "outputs")
    assert main(["--stdout", "--ratio", "5"], now=NOW) == 0
    captured = capsys.readouterr()
    assert captured.out.startswith("# Veille du ")
    assert "au moins 5× la médiane" in captured.out
    assert "Outliers : 0" in captured.err
    assert not (tmp_path / "outputs").exists()
