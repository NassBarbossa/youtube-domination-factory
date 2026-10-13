#!/usr/bin/env python3
"""(Ré)autorise l'accès à l'API YouTube Analytics et écrit token.json.

Usage :
    python3 yt-analytics/auth.py

À lancer quand analyze.py ou feedback_analyzer.py répondent « invalid_grant » (jeton expiré ou révoqué).
Il faut client_secret.json dans yt-analytics/ (identifiants OAuth « application de bureau » de la console Google Cloud).
Le navigateur s'ouvre, tu choisis le compte YouTube de la chaîne, et token.json est réécrit. Ni l'un ni l'autre ne vont dans git.
"""
import json
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET = SCRIPT_DIR / "client_secret.json"
TOKEN_PATH = SCRIPT_DIR / "token.json"
SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def main():
    if not CLIENT_SECRET.exists():
        sys.exit(f"client_secret.json introuvable dans {SCRIPT_DIR} (console Google Cloud → identifiants OAuth, application de bureau).")
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    TOKEN_PATH.write_text(json.dumps({
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes or SCOPES),
    }, indent=2) + "\n")
    print(f"OK : {TOKEN_PATH} réécrit. Tu peux relancer analyze.py ou feedback_analyzer.py.")


if __name__ == "__main__":
    main()
