import psutil

apps = {
    "Chrome": False,
    "VSCode": False,
    "WhatsApp": False,
    "OneNote": False,
    "WPS": False,
    "MySQL": False
}

for process in psutil.process_iter(["name"]):
    try:
        name = (process.info["name"] or "").lower()

        if name == "chrome.exe":
            apps["Chrome"] = True
        elif name == "code.exe":
            apps["VSCode"] = True
        elif "whatsapp" in name:
            apps["WhatsApp"] = True
        elif name == "onenote.exe":
            apps["OneNote"] = True
        elif name == "wps.exe":
            apps["WPS"] = True
        elif name == "mysqld.exe":
            apps["MySQL"] = True

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print("Detected applications:")
for app, running in apps.items():
    print(f"{app}: {1 if running else 0}")

print("Active tracked apps:", sum(apps.values()))