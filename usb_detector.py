import time
import threading
import psutil
import win32file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

monitoring = False
connected_devices = set()
observers = {}
alert_callback = None


def set_alert_callback(callback):
    global alert_callback
    alert_callback = callback


class USBFileEventHandler(FileSystemEventHandler):
    def __init__(self, usb_path):
        self.usb_path = usb_path

    def on_created(self, event):
        if not event.is_directory:
            log_event("CREATED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            log_event("DELETED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            log_event("MODIFIED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            log_event("MOVED", f"{event.src_path} ➜ {event.dest_path}")


def log_event(event_type, file_path):
    message = f"[{event_type}] {file_path}"
    print(message)
    with open("usb_logs.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

    if alert_callback:
        alert_callback(f"💾 {message}")


def start_usb_monitoring():
    global monitoring
    monitoring = True
    thread = threading.Thread(target=monitor_usb_loop)
    thread.daemon = True
    thread.start()


def stop_usb_monitoring():
    global monitoring
    monitoring = False
    # Stop all file observers
    for obs in observers.values():
        obs.stop()
    for obs in observers.values():
        obs.join()
    observers.clear()


def is_monitoring():
    return monitoring


def monitor_usb_loop():
    global connected_devices, observers
    while monitoring:
        current_devices = set()
        for part in psutil.disk_partitions(all=False):
            if 'removable' in part.opts or 'cdrom' in part.opts:
                current_devices.add(part.device)

        added = current_devices - connected_devices
        removed = connected_devices - current_devices

        for device in added:
            if alert_callback:
                alert_callback(f"🟢 USB Device Connected: {device}")
            # Start file system observer
            mount_path = device
            event_handler = USBFileEventHandler(mount_path)
            observer = Observer()
            observer.schedule(event_handler, path=mount_path, recursive=True)
            observer.start()
            observers[device] = observer

        for device in removed:
            if alert_callback:
                alert_callback(f"🔴 USB Device Removed: {device}")
            # Stop and remove observer
            if device in observers:
                observers[device].stop()
                observers[device].join()
                del observers[device]

        connected_devices = current_devices
        time.sleep(2)
