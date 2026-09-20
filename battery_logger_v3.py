import psutil
import time
import csv
from datetime import datetime
import subprocess

from battery_optimizer import battery_optimizer

workload = input("What are you doing? ")

apps_to_track = {
    "Chrome": "chrome.exe",
    "VSCode": "code.exe",
    "WhatsApp": "whatsapp.exe",
    "OneNote": "onenote.exe",
    "WPS": "wps.exe"
}

filename = "battery_dataset_v3.csv"


def get_brightness():
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness).CurrentBrightness"
            ],
            text=True
        )

        value = result.strip().splitlines()

        if value:
            return int(value[-1])

    except Exception:
        pass

    return -1


with open(filename, "a", newline="") as file:
    writer = csv.writer(file)

    if file.tell() == 0:
        writer.writerow([
            "Time",
            "Battery",
            "CPU",
            "RAM",
            "Brightness",
            "Charging",
            "Estimated_Seconds_Left",
            "Chrome",
            "VSCode",
            "WhatsApp",
            "OneNote",
            "WPS",
            "Active_App_Count",
            "workload"
        ])


print("Application-aware battery logger started.")
print("Press Ctrl+C to stop.")
print()

try:
    while True:

        battery = psutil.sensors_battery()

        if battery:
            battery_percent = battery.percent
            charging = battery.power_plugged
            seconds_left = battery.secsleft

            if seconds_left in (
                psutil.POWER_TIME_UNLIMITED,
                psutil.POWER_TIME_UNKNOWN
            ):
                seconds_left = -1
        else:
            battery_percent = -1
            charging = False
            seconds_left = -1

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        brightness = get_brightness()

        running = set()

        for process in psutil.process_iter(["name"]):
            try:
                name = process.info["name"]

                if name:
                    running.add(name.lower())

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        detected = {}

        for app, process_name in apps_to_track.items():
            detected[app] = (
                1 if process_name.lower() in running else 0
            )

        active_apps = sum(detected.values())

        level, score, reasons, recommendations = battery_optimizer(
            battery_percent,
            cpu,
            ram,
            brightness,
            workload,
            detected["WhatsApp"],
            active_apps
        )

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        row = [
            current_time,
            battery_percent,
            cpu,
            ram,
            brightness,
            charging,
            seconds_left,
            detected["Chrome"],
            detected["VSCode"],
            detected["WhatsApp"],
            detected["OneNote"],
            detected["WPS"],
            active_apps,
            workload
        ]

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

        print(
            f"Time: {current_time} | "
            f"Battery: {battery_percent}% | "
            f"CPU: {cpu}% | "
            f"RAM: {ram}% | "
            f"Brightness: {brightness}% | "
            f"Chrome: {detected['Chrome']} | "
            f"VSCode: {detected['VSCode']} | "
            f"WhatsApp: {detected['WhatsApp']} | "
            f"Active apps: {active_apps} | "
            f"Workload: {workload}"
        )

        print(f"Battery Pressure: {level} | Score: {score}")

        print("Reasons:")
        for reason in reasons:
            print(f"- {reason}")

        print("Recommended Actions:")
        for recommendation in recommendations:
            print(f"- {recommendation}")

        print("-" * 60)

        time.sleep(30)

except KeyboardInterrupt:
    print("\nLogger stopped.")