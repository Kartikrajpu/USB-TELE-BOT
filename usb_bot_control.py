import os
import ctypes
import subprocess
import asyncio
import cv2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from usb_detector import (
    start_usb_monitoring,
    stop_usb_monitoring,
    is_monitoring,
    set_alert_callback,
    
)

# === BOT SETTINGS ===
BOT_TOKEN = "7667479593:AAHXBCe5hiP4yMQ5caDI4WNCR4DqLvbSJI8"
AUTHORIZED_CHAT_ID = 1550711726  # Replace with your Telegram user ID

# === ALERT CALLBACK SETUP ===
async def send_alert(message):
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    await app.bot.send_message(chat_id=AUTHORIZED_CHAT_ID, text=message)

def telegram_alert_handler(msg):
    asyncio.run(send_alert(msg))

set_alert_callback(telegram_alert_handler)

# === CORE COMMANDS ===
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    start_usb_monitoring()
    await update.message.reply_text("✅ USB Monitoring started.")

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    stop_usb_monitoring()
    await update.message.reply_text("🛑 USB Monitoring stopped.")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    status = "Running ✅" if is_monitoring() else "Stopped ❌"
    await update.message.reply_text(f"📊 Status: {status}")

async def logs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    try:
        with open("usb_logs.txt", "rb") as f:
            await update.message.reply_document(f)
    except FileNotFoundError:
        await update.message.reply_text("❌ Log file not found.")

# === SYSTEM CONTROL COMMANDS ===
async def lock_usb_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    try:
        subprocess.run('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f', shell=True)
        await update.message.reply_text("🔒 USB ports disabled.")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to lock USB: {e}")

async def unlock_usb_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    try:
        subprocess.run('reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f', shell=True)
        await update.message.reply_text("🔓 USB ports enabled.")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unlock USB: {e}")

async def shutdown_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    await update.message.reply_text("⚠️ Shutting down system...")
    os.system("shutdown /s /t 0")

async def lockscreen_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    await update.message.reply_text("🔐 Locking screen...")
    ctypes.windll.user32.LockWorkStation()

async def camshot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite("camshot.jpg", frame)
            with open("camshot.jpg", "rb") as photo:
                await context.bot.send_photo(chat_id=AUTHORIZED_CHAT_ID, photo=photo)
        else:
            await update.message.reply_text("❌ Failed to capture from webcam.")
    except Exception as e:
        await update.message.reply_text(f"❌ Webcam error: {e}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return
    commands = """
🤖 *USB Telegram Bot Commands*:
/start – Start USB monitoring  
/stop – Stop USB monitoring  
/status – Check monitoring status  
/logs – Get USB activity logs  
/camshot – Capture webcam photo  
/lockscreen – Lock the system screen  
/shutdown – Shutdown the system  
/lockusb – Disable all USB storage ports  
/unlockusb – Re-enable USB ports  
/help – Show this command list
"""
    await update.message.reply_text(commands, parse_mode="Markdown")


# === BOT INITIALIZATION ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Core monitoring commands
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("logs", logs_cmd))

    # Advanced system control
    app.add_handler(CommandHandler("lockusb", lock_usb_cmd))
    app.add_handler(CommandHandler("unlockusb", unlock_usb_cmd))
    app.add_handler(CommandHandler("shutdown", shutdown_cmd))
    app.add_handler(CommandHandler("lockscreen", lockscreen_cmd))
    app.add_handler(CommandHandler("camshot", camshot_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    app.run_polling()
