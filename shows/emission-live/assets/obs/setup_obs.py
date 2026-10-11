"""Crée les scènes Convergence dans OBS via le WebSocket (obsws-python).
Usage : python setup_obs.py   (OBS ouvert, collection « Convergence » active, WebSocket activé)
"""
import json, os, secrets, sys, time
import obsws_python as obs

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # dossier Convergence
URL = lambda rel: "file:///" + os.path.join(BASE, rel).replace("\\", "/")
cfg = json.load(open(os.path.expandvars(r"%APPDATA%\obs-studio\plugin_config\obs-websocket\config.json")))
cl = obs.ReqClient(host="localhost", port=cfg["server_port"], password=cfg["server_password"], timeout=15)

if cl.get_scene_collection_list().current_scene_collection_name != "Convergence":
    sys.exit("Active d'abord la collection de scènes « Convergence » dans OBS.")

vs = cl.get_video_settings()
CW, CH = vs.base_width, vs.base_height
K = CW / 1920                                   # nos écrans sont dessinés en 1920 × 1080
MIC = sys.argv[1] if len(sys.argv) > 1 else "default"
VDO_ID = "convergence-" + secrets.token_hex(3)

def scene(name):
    names = [s["sceneName"] for s in cl.get_scene_list().scenes]
    if name not in names:
        cl.create_scene(name)

def add(scene_name, input_name, kind, settings, x=0, y=0, w=None, h=None, crop=None):
    """Ajoute (ou réutilise) une source, positionnée en coordonnées 1920 × 1080."""
    existing = [i["inputName"] for i in cl.get_input_list().inputs]
    if input_name in existing:
        item_id = cl.create_scene_item(scene_name, input_name, True).scene_item_id
    else:
        item_id = cl.create_input(scene_name, input_name, kind, settings, True).scene_item_id
    tr = {"positionX": x * K, "positionY": y * K}
    if w and h:
        tr.update({"boundsType": "OBS_BOUNDS_SCALE_OUTER" if crop == "cover" else "OBS_BOUNDS_STRETCH",
                   "boundsWidth": w * K, "boundsHeight": h * K, "boundsAlignment": 0, "cropToBounds": True})
    cl.set_scene_item_transform(scene_name, item_id, tr)
    return item_id

def browser(scene_name, name, rel, query="", audio=False):
    add(scene_name, name, "browser_source",
        {"is_local_file": False, "url": URL(rel) + query, "width": 1920, "height": 1080,
         "fps_custom": True, "fps": 30, "reroute_audio": audio, "shutdown": False, "restart_when_active": True},
        0, 0, 1920, 1080)

# 1. Attente
scene("1 · Attente")
browser("1 · Attente", "Écran attente", "obs/1-attente.html", "?min=5")
add("1 · Attente", "Micro", "wasapi_input_capture", {"device_id": MIC})

# 2. Intro (intro banger 15 s, plan-séquence + musique)
scene("2 · Intro")
add("2 · Intro", "Intro V", "ffmpeg_source",
    {"local_file": os.path.join(BASE, "video", "convergence-intro-banger-15s.mp4"),
     "restart_on_activate": True, "close_when_inactive": True, "looping": False}, 0, 0, 1920, 1080)

# 3. Live : caméras SOUS l'habillage percé
scene("3 · Live")
add("3 · Live", "Fond papier", "color_source_v3", {"color": 0xFFE8EFF2, "width": 1920, "height": 1080}, 0, 0, 1920, 1080)
# Co-host à distance via VDO.Ninja (gratuit) — fenêtre or : x 50, y 108, 702 × 848
add("3 · Live", "Caméra co-host (VDO.Ninja)", "browser_source",
    {"is_local_file": False, "url": f"https://vdo.ninja/?view={VDO_ID}&cover&cleanoutput&noaudiowarning",
     "width": 702, "height": 848, "reroute_audio": True, "shutdown": False},
    50, 108, 702, 848)
# Caméra de Nass — fenêtre verte : x 784, y 108, 702 × 848 (périphérique à choisir dans OBS)
add("3 · Live", "Caméra Nass", "dshow_input", {}, 784, 108, 702, 848, crop="cover")
browser("3 · Live", "Habillage live", "obs/2-live.html", "?ep=01&cohost=CO-HOST&nass=NASS")
add("3 · Live", "Micro", "wasapi_input_capture", {"device_id": MIC})

# 4. Sujet
scene("4 · Sujet")
browser("4 · Sujet", "Carte sujet", "obs/3-sujet.html",
        "?n=1&total=5&titre=Le titre de la tendance.&mot=titre&tags=OR,BTC")
add("4 · Sujet", "Micro", "wasapi_input_capture", {"device_id": MIC})

# 5. Fin
scene("5 · Fin")
browser("5 · Fin", "Écran fin", "obs/4-fin.html")
add("5 · Fin", "Micro", "wasapi_input_capture", {"device_id": MIC})

# Nettoyage de la scène vide créée par défaut
for s in [s["sceneName"] for s in cl.get_scene_list().scenes]:
    if s not in ("1 · Attente", "2 · Intro", "3 · Live", "4 · Sujet", "5 · Fin"):
        try: cl.remove_scene(s)
        except Exception: pass

cl.set_current_program_scene("1 · Attente")
print("VDO_ID", VDO_ID)
print("Lien à envoyer au co-host :", f"https://vdo.ninja/?push={VDO_ID}&webcam&quality=1")
