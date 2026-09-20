import psutil

apps = set()

for process in psutil.process_iter(["name"]):
    try:
        name = process.info["name"]

        if name:
            apps.add(name)

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print("Running applications/processes:")

for app in sorted(apps):
    print(app)