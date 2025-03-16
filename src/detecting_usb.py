import platform
import subprocess


def detect_usb_devices():
    usb_devices = []
    system_name = platform.system()

    if system_name == "Windows":
        result = subprocess.run(["wmic", "logicaldisk", "get", "caption,description,volumename"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "Removable Disk" in line:
                columns = line.split()
                if len(columns) > 2:
                    usb_devices.append(f"{columns[0]}\\")

    elif system_name == "Linux":
        result = subprocess.run(["lsblk", "-o", "NAME,LABEL,MOUNTPOINT"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "/media" in line or "/mnt" in line:
                columns = line.split()
                if len(columns) > 1:
                    usb_devices.append(f"{columns[1]} ({columns[0]})")

    return usb_devices if usb_devices else ["Brak wykrytych nośników"]
