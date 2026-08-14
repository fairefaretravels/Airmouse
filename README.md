# Air Mouse

Turn your phone (Android or iPhone, no app install needed) into a
motion-controlled mouse for your Windows PC. Move the phone, the cursor
moves — no touchpad tapping.

## How it works
Your PC runs a small local server. Your phone opens a webpage served by
that server (over your home WiFi) and uses its motion sensors to send
cursor movement to the PC over a WebSocket. Nothing goes over the
internet — it's all on your local network.

## One-time setup (on the Windows PC)

1. Install Python 3.9+ if you don't have it: https://www.python.org/downloads/
   (check "Add python.exe to PATH" during install)

2. Open Command Prompt in this folder and install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Generate the HTTPS certificate (only needed once):
   ```
   python gen_cert.py
   ```

## Running it

1. Start the server:
   ```
   python server.py
   ```
   Leave this window open — closing it stops the server.

2. Windows Firewall may prompt "Allow Python to communicate on this
   network" — click **Allow** (for Private networks).

3. Find your PC's local IP address. Open a *second* Command Prompt and run:
   ```
   ipconfig
   ```
   Look for "IPv4 Address" under your active WiFi or Ethernet adapter,
   e.g. `192.168.1.42`.

4. On your phone (connected to the **same WiFi network** as the PC),
   open a browser and go to:
   ```
   https://192.168.1.42:8443
   ```
   (using your PC's actual IP)

5. Your phone browser will warn the site isn't secure — that's expected,
   it's just because the certificate is self-signed by your own PC.
   Tap **Advanced** → **Proceed** (wording varies by browser).

6. Tap **Enable Motion**. On iPhone, Safari will ask permission to
   access motion & orientation — tap **Allow**.

7. Hold the phone comfortably in front of you, tap **Recenter**, then
   tilt/move it to steer the cursor. Use the on-screen Left Click /
   Right Click buttons, and swipe the strip at the bottom to scroll.

## Adjusting feel
- The **Sensitivity** slider on the phone controls how far the cursor
  moves per degree of tilt — turn it down for finer control, up for
  faster sweeps across the screen.
- Tap **Recenter** any time the cursor drifts or you change how you're
  holding the phone.

## Notes
- Works over WiFi only (phone and PC must be on the same network).
  It won't work over cellular data or across different networks.
- If the connection drops, the page auto-reconnects — just refresh if
  it doesn't pick back up.
- This is unencrypted-by-trust-but-still-TLS local traffic; it's not
  exposed to the internet, only devices on your WiFi network could
  reach the server's port.
