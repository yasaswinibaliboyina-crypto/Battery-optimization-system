import pandas as pd
import numpy as np

real = pd.read_csv("battery_model_real.csv")

rng = np.random.default_rng(42)

n = 40
rows = []

scenarios = [
    (1, 0, 0, "Browsing"),
    (1, 0, 1, "Whatsapp"),
    (0, 1, 0, "Coding"),
    (1, 1, 1, "Mixed")
]

workload_params = {
    "Browsing": (7.9, 61.7, 23),
    "Whatsapp": (10.4, 57.9, 23),
    "Coding": (8.5, 60.9, 23),
    "Mixed": (11.0, 63.0, 23)
}

bmin = int(real["Battery"].min())
bmax = int(real["Battery"].max())

rmin = real["RAM"].min()
rmax = real["RAM"].max()

cmin = real["CPU"].min()
cmax = real["CPU"].max()

for i in range(n):

    chrome, vscode, whatsapp, workload = scenarios[i % len(scenarios)]

    cpu_mean, ram_mean, brightness = workload_params[workload]

    cpu = float(
        np.clip(
            rng.normal(cpu_mean, 2.5),
            cmin,
            cmax
        )
    )

    ram = float(
        np.clip(
            rng.normal(ram_mean, 1.5),
            rmin,
            rmax
        )
    )

    battery = int(
        rng.integers(
            bmin,
            bmax + 1
        )
    )

    active_apps = chrome + vscode + whatsapp + 1

    rows.append([
        f"SYN_{i + 1:03d}",
        battery,
        cpu,
        ram,
        brightness,
        False,
        -1,
        chrome,
        vscode,
        whatsapp,
        0,
        1,
        active_apps,
        workload,
        "synthetic"
    ])


columns = [
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
    "workload",
    "data_source"
]

synthetic = pd.DataFrame(
    rows,
    columns=columns
)

synthetic.to_csv(
    "battery_model_synthetic.csv",
    index=False
)

print("Created synthetic rows:", len(synthetic))
print()
print(synthetic["workload"].value_counts())
print()
print(synthetic.head())