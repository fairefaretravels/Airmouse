"""
Air Mouse server. Run this on the Windows PC you want to control.

Setup (one time):
    pip install -r requirements.txt
    python gen_cert.py

Run:
    python server.py

Then on your phone, open a browser to:
    https://<this-PC's-LAN-IP>:8443

(Find your PC's LAN IP with `ipconfig` in Command Prompt - look for
"IPv4 Address" under your active WiFi/Ethernet adapter.)
"""

import json
import ssl
from pathlib import Path

import pyautogui
from aiohttp import web, WSMsgType

pyautogui.FAILSAFE = False  # don't abort if the cursor hits a screen corner

BASE_DIR = Path(__file__).parent
PORT = 8443


async def index(request):
    return web.FileResponse(BASE_DIR / "index.html")


async def ws_handler(request):
    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(request)
    print(f"[+] Phone connected from {request.remote}")

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except json.JSONDecodeError:
                continue

            kind = data.get("type")

            if kind == "move":
                dx = data.get("dx", 0)
                dy = data.get("dy", 0)
                if dx or dy:
                    try:
                        pyautogui.moveRel(dx, dy, duration=0)
                    except Exception as e:
                        print("move error:", e)

            elif kind == "click":
                button = data.get("button", "left")
                pyautogui.click(button=button)

            elif kind == "scroll":
                amount = data.get("amount", 0)
                if amount:
                    pyautogui.scroll(amount)

        elif msg.type == WSMsgType.ERROR:
            print("WebSocket error:", ws.exception())

    print("[-] Phone disconnected")
    return ws


def build_app():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", ws_handler)
    return app


def main():
    cert_path = BASE_DIR / "cert.pem"
    key_path = BASE_DIR / "key.pem"

    if not cert_path.exists() or not key_path.exists():
        print("No certificate found. Run this first:  python gen_cert.py")
        raise SystemExit(1)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(str(cert_path), str(key_path))

    print(f"Air Mouse server starting on https://0.0.0.0:{PORT}")
    print(f"On your phone (same WiFi), open: https://<this-PC-LAN-IP>:{PORT}")
    print("Press Ctrl+C to stop.")

    web.run_app(build_app(), host="0.0.0.0", port=PORT, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
