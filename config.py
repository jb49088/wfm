from pathlib import Path

APP_DIR = Path.home() / ".wfm"
COOKIES_FILE = APP_DIR / "cookies.json"
HISTORY_FILE = APP_DIR / "history"
SYNC_STATE_FILE = APP_DIR / "sync_state.json"

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
}

WS_URI = "wss://ws.warframe.market/socket"
AUTH_MESSAGE = '{"route":"@wfm|cmd/auth/signIn","payload":{"token":""}}'
