# USB-TELE-BOT
# USB-TELE-BOT 🔌📲

A Python-based USB activity monitor and remote control tool that uses Telegram Bot API for alerts and commands.

> Built for security enthusiasts, researchers, and defenders.  
> **Author**: Kartik Rajput

---

## 🛡 Features

- 🔄 Real-time USB plug/unplug detection
- 📂 File access + movement logging
- 🤖 Telegram bot command control
- 🔒 USB locking / unlocking
- 💻 Remote shutdown & lockscreen
- 📷 Webcam snapshot (/camshot)

---

## 💻 Setup

### 1. Clone the Repo

```bash
git clone https://github.com/Kartikrajpu/USB-TELE-BOT.git
cd USB-TELE-BOT
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Set Your Bot Token & Chat ID
Edit usb_bot_control.py:

python
Copy
Edit
BOT_TOKEN = "YOUR_BOT_TOKEN"
AUTHORIZED_CHAT_ID = 123456789
4. Run as Admin (important)
Use a .bat launcher like:

bat
Copy
Edit
@echo off
powershell -Command "Start-Process 'python' -ArgumentList 'usb_bot_control.py' -Verb RunAs"
Or compile to .exe with PyInstaller (optional).

📜 Commands
Command	Description
/start	Start monitoring
/stop	Stop monitoring
/status	Check if running
/log	Get USB logs
/lockusb	Disable USB ports (admin)
/unlockusb	Enable USB ports (admin)
/shutdown	Shut down PC (admin)
/lockscreen	Lock the screen
/camshot	Capture webcam photo

⚠️ Disclaimer
This tool is for educational and defensive security purposes only. Do not use it on systems without explicit authorization.
