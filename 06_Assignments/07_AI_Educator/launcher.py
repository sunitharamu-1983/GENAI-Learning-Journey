"""
AI Educator — Windows Desktop Launcher

Starts Streamlit silently in the background, waits until the server
is ready, then opens it in a native WebView2 desktop window.
Falls back to the default browser if WebView2 is unavailable.
"""

import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path

import requests

PORT = 8501
APP_DIR = Path(__file__).parent
APP_PATH = APP_DIR / "app.py"
PYTHON = sys.executable
URL = f"http://localhost:{PORT}"


def _start_streamlit():
    subprocess.Popen(
        [
            PYTHON, "-m", "streamlit", "run", str(APP_PATH),
            "--server.port",            str(PORT),
            "--server.headless",        "true",
            "--browser.serverAddress",  "localhost",
            "--browser.gatherUsageStats", "false",
        ],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW,  # no extra console window
    )


def _wait_for_server(timeout: int = 40) -> bool:
    for _ in range(timeout):
        try:
            if requests.get(URL, timeout=1).status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def _open_desktop_window():
    import webview
    webview.create_window(
        title="🎓 AI Educator",
        url=URL,
        width=1280,
        height=860,
        resizable=True,
        min_size=(900, 640),
    )
    webview.start()


def _open_browser_fallback():
    webbrowser.open(URL)
    print(f"AI Educator is running at {URL}")
    print("Close this window to stop the server.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")


if __name__ == "__main__":
    print("Starting AI Educator...")

    t = threading.Thread(target=_start_streamlit, daemon=True)
    t.start()

    print("Waiting for server to be ready...")
    if not _wait_for_server():
        print("ERROR: Server did not start. Check your setup.")
        sys.exit(1)

    print("Ready! Opening app...")
    try:
        _open_desktop_window()
    except Exception as exc:
        print(f"Native window unavailable ({exc}). Opening in browser instead.")
        _open_browser_fallback()
