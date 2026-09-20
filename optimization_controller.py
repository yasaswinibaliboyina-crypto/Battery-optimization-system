import psutil
import joblib


TRACKED_APPS = {
    "chrome": "Chrome",
    "code": "VSCode",
    "whatsapp": "WhatsApp",
    "onenote": "OneNote",
    "wps": "WPS"
}


DRAIN_RATES = {
    "Coding": 13.27,
    "Light": 13.19,
    "Video": 16.14,
    "Whatsapp": 9.42
}


# --------------------------------------------------
# LOAD ML MODELS
# --------------------------------------------------

try:
    workload_model = joblib.load("workload_model.pkl")
    battery_model = joblib.load("battery_model.pkl")

    workload_features = joblib.load(
        "workload_features.pkl"
    )

    battery_features = joblib.load(
        "battery_features.pkl"
    )

    ML_AVAILABLE = True

except Exception as e:
    print("ML models could not be loaded.")
    print("Error:", e)

    ML_AVAILABLE = False


# --------------------------------------------------
# SYSTEM MONITORING
# --------------------------------------------------

def get_battery():

    return psutil.sensors_battery()


def get_cpu():

    return psutil.cpu_percent(interval=1)


def get_ram():

    return psutil.virtual_memory().percent


# --------------------------------------------------
# APPLICATION DETECTION
# --------------------------------------------------

def get_active_apps():

    active_apps = {}

    for process in psutil.process_iter(
        ["name", "cpu_percent", "memory_percent"]
    ):

        try:

            name = process.info["name"]

            if not name:
                continue

            name_lower = name.lower()

            for key, display_name in TRACKED_APPS.items():

                if key in name_lower:

                    if display_name not in active_apps:

                        active_apps[display_name] = {
                            "cpu": process.info["cpu_percent"] or 0,
                            "memory":
                                process.info["memory_percent"] or 0
                        }

                    else:

                        active_apps[display_name]["cpu"] += (
                            process.info["cpu_percent"] or 0
                        )

                        active_apps[display_name]["memory"] += (
                            process.info["memory_percent"] or 0
                        )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):

            continue

    return active_apps


# --------------------------------------------------
# ML WORKLOAD PREDICTION
# --------------------------------------------------

def predict_workload(
    battery,
    cpu,
    ram,
    apps
):

    chrome = 1 if "Chrome" in apps else 0
    vscode = 1 if "VSCode" in apps else 0
    whatsapp = 1 if "WhatsApp" in apps else 0
    onenote = 1 if "OneNote" in apps else 0
    wps = 1 if "WPS" in apps else 0

    active_app_count = len(apps)

    battery_info = get_battery()

    if battery_info:

        charging = int(
            battery_info.power_plugged
        )

        seconds_left = battery_info.secsleft

        if seconds_left in (
            psutil.POWER_TIME_UNKNOWN,
            psutil.POWER_TIME_UNLIMITED
        ):

            seconds_left = -1

    else:

        charging = 0
        seconds_left = -1


    data = {
        "Battery": battery,
        "CPU": cpu,
        "RAM": ram,
        "Brightness": 23,
        "Charging": charging,
        "Estimated_Seconds_Left": seconds_left,
        "Chrome": chrome,
        "VSCode": vscode,
        "WhatsApp": whatsapp,
        "OneNote": onenote,
        "WPS": wps,
        "Active_App_Count": active_app_count
    }


    try:

        input_data = [
            data[feature]
            for feature in workload_features
        ]

        prediction = workload_model.predict(
            [input_data]
        )[0]

        return prediction

    except Exception:

        return "Light"


# --------------------------------------------------
# ML BATTERY PREDICTION
# --------------------------------------------------

def predict_battery(
    cpu,
    ram,
    apps
):

    chrome = 1 if "Chrome" in apps else 0
    vscode = 1 if "VSCode" in apps else 0
    whatsapp = 1 if "WhatsApp" in apps else 0
    onenote = 1 if "OneNote" in apps else 0
    wps = 1 if "WPS" in apps else 0

    active_app_count = len(apps)

    battery_info = get_battery()

    if battery_info:

        charging = int(
            battery_info.power_plugged
        )

        seconds_left = battery_info.secsleft

        if seconds_left in (
            psutil.POWER_TIME_UNKNOWN,
            psutil.POWER_TIME_UNLIMITED
        ):

            seconds_left = -1

    else:

        charging = 0
        seconds_left = -1


    data = {
        "CPU": cpu,
        "RAM": ram,
        "Brightness": 23,
        "Charging": charging,
        "Estimated_Seconds_Left": seconds_left,
        "Chrome": chrome,
        "VSCode": vscode,
        "WhatsApp": whatsapp,
        "OneNote": onenote,
        "WPS": wps,
        "Active_App_Count": active_app_count
    }


    try:

        input_data = [
            data[feature]
            for feature in battery_features
        ]

        prediction = battery_model.predict(
            [input_data]
        )[0]

        return prediction

    except Exception:

        return None


# --------------------------------------------------
# BATTERY PRESSURE
# --------------------------------------------------

def get_pressure(
    battery,
    cpu,
    ram
):

    score = 0


    if battery <= 10:

        score += 50

    elif battery <= 20:

        score += 40

    elif battery <= 30:

        score += 25


    if cpu >= 20:

        score += 25

    elif cpu >= 10:

        score += 15


    if ram >= 65:

        score += 20

    elif ram >= 60:

        score += 10


    if score >= 70:

        return "Critical", score

    elif score >= 50:

        return "High", score

    elif score >= 30:

        return "Moderate", score

    return "Normal", score


# --------------------------------------------------
# TIME ESTIMATION
# --------------------------------------------------

def estimate_time_remaining(
    battery,
    workload
):

    drain_rate = DRAIN_RATES.get(
        workload,
        13.19
    )

    if drain_rate <= 0:

        return 0

    return battery / drain_rate


def format_time(hours):

    minutes = int(hours * 60)

    h = minutes // 60
    m = minutes % 60

    return f"{h}h {m}m"


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

def generate_recommendations(
    battery,
    cpu,
    ram,
    apps,
    workload
):

    recommendations = []


    if battery <= 30:

        recommendations.append({
            "action":
                "Enable Battery Saver / power-saving mode.",

            "reason":
                "Battery level is getting low."
        })


    if battery <= 20:

        recommendations.append({
            "action":
                "Reduce screen brightness to around 20-30%.",

            "reason":
                "Lower brightness can reduce display power consumption."
        })


    if workload == "Video":

        recommendations.append({
            "action":
                "Reduce screen brightness for video playback.",

            "reason":
                "Video has the highest observed drain rate."
        })


    for name, data in apps.items():

        if data["memory"] >= 10:

            recommendations.append({
                "action":
                    f"Close {name} if not needed.",

                "reason":
                    f"{name} is using "
                    f"{data['memory']:.1f}% RAM"
            })


        if data["cpu"] >= 10:

            recommendations.append({
                "action":
                    f"Reduce activity in {name}.",

                "reason":
                    f"{name} is using "
                    f"{data['cpu']:.1f}% CPU"
            })


    if ram >= 65:

        recommendations.append({
            "action":
                "Close unused applications.",

            "reason":
                f"RAM usage is high at {ram:.1f}%"
        })


    elif ram >= 60:

        recommendations.append({
            "action":
                "Review unused applications.",

            "reason":
                f"RAM usage is moderately high at {ram:.1f}%"
        })


    if cpu >= 20:

        recommendations.append({
            "action":
                "Reduce unnecessary background processes.",

            "reason":
                f"CPU usage is high at {cpu:.1f}%"
        })


    return recommendations


# --------------------------------------------------
# MAIN OPTIMIZER
# --------------------------------------------------

def optimize():

    battery_info = get_battery()


    if battery_info is None:

        print("Battery information unavailable.")
        return


    battery = battery_info.percent

    cpu = get_cpu()

    ram = get_ram()

    apps = get_active_apps()


    # --------------------------------------------------
    # ML WORKLOAD
    # --------------------------------------------------

    if ML_AVAILABLE:

        workload = predict_workload(
            battery,
            cpu,
            ram,
            apps
        )

    else:

        workload = "Light"


    # --------------------------------------------------
    # PRESSURE
    # --------------------------------------------------

    pressure, score = get_pressure(
        battery,
        cpu,
        ram
    )


    # --------------------------------------------------
    # HISTORICAL ESTIMATE
    # --------------------------------------------------

    drain_rate = DRAIN_RATES.get(
        workload,
        13.19
    )


    remaining_hours = estimate_time_remaining(
        battery,
        workload
    )


    # --------------------------------------------------
    # ML BATTERY PREDICTION
    # --------------------------------------------------

    predicted_battery = predict_battery(
        cpu,
        ram,
        apps
    )


    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------

    print("\n========================================")

    print(
        "       BATTERY OPTIMIZATION SYSTEM"
    )

    print("========================================")


    print(
        f"Battery: {battery:.0f}%"
    )


    print(
        f"CPU: {cpu:.1f}%"
    )


    print(
        f"RAM: {ram:.1f}%"
    )


    print(
        f"Workload: {workload}"
    )


    print(
        f"Battery Pressure: {pressure}"
    )


    print(
        f"Pressure Score: {score}"
    )


    print(
        f"Estimated remaining time: "
        f"{format_time(remaining_hours)}"
    )


    print(
        f"Historical observed drain rate: "
        f"{drain_rate:.2f}% per hour"
    )


    if predicted_battery is not None:

        print(
            f"ML predicted battery: "
            f"{predicted_battery:.1f}%"
        )


    # --------------------------------------------------
    # APPLICATIONS
    # --------------------------------------------------

    print(
        "\nACTIVE USER APPLICATIONS"
    )


    if apps:

        for name, data in apps.items():

            print(
                f"- {name:<10} "
                f"CPU: {data['cpu']:>5.1f}% | "
                f"RAM: {data['memory']:>5.1f}%"
            )

    else:

        print(
            "- No tracked applications detected."
        )


    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = generate_recommendations(
        battery,
        cpu,
        ram,
        apps,
        workload
    )


    print(
        "\n----------------------------------------"
    )

    print(
        "RECOMMENDED ACTIONS"
    )

    print(
        "----------------------------------------"
    )


    if not recommendations:

        print(
            "\n✓ No immediate optimization required."
        )

    else:

        for i, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print(
                f"\n{i}. ACTION"
            )

            print(
                f"   {recommendation['action']}"
            )

            print(
                f"   Reason: "
                f"{recommendation['reason']}"
            )


    print(
        "\n========================================"
    )


if __name__ == "__main__":

    optimize()