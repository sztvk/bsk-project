import platform
import subprocess


def detect_usb_devices():
    """
    Detects USB devices connected to the system.

    This function identifies USB devices by checking the operating system. It handles both Windows and Linux platforms.
    - On Windows, it uses the `wmic` command to query information about logical disks and searches for devices marked as
      "Removable Disk."
    - On Linux, it uses the `lsblk` command to list block devices and identifies USB devices based on the mount points
      under `/media` or `/mnt`.

    The function returns a list of connected USB devices. If no USB devices are detected, it returns a default message
    indicating that no USB devices were found.

    The detected devices are returned in different formats depending on the operating system:
    - **Windows**: It returns the drive letter followed by a backslash (e.g., "C:\").
    - **Linux**: It returns the device label followed by the device name (e.g., "My USB (sdb1)").

    If no devices are found, the function returns a list containing the message "Brak wykrytych nośników" (which means
    "No detected media").

    Parameters
    ----------
    None.

    Returns
    -------
    usb_devices : list
        A list of detected USB devices or a message indicating no devices were found. The format depends on the
        operating system:
        - **Windows**: A list of drive letters with a backslash (e.g., ["C:\"]).
        - **Linux**: A list of device labels and names (e.g., ["My USB (sdb1)"]).
        If no devices are found, the list contains the string ["Brak wykrytych nośników"].
    """
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
