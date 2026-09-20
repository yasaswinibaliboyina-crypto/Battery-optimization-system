from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
import joblib


app = FastAPI(
    title="Battery Optimization System API"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# LOAD ML MODELS
# --------------------------------------------------

workload_model = joblib.load(
    "workload_model.pkl"
)

battery_model = joblib.load(
    "battery_model.pkl"
)

workload_features = joblib.load(
    "workload_features.pkl"
)

battery_features = joblib.load(
    "battery_features.pkl"
)


# --------------------------------------------------
# TRACKED APPLICATIONS
# --------------------------------------------------

TRACKED_APPS = {
    "chrome": "Chrome",
    "code": "VSCode",
    "whatsapp": "WhatsApp",
    "onenote": "OneNote",
    "wps": "WPS"
}


# --------------------------------------------------
# HISTORICAL DRAIN RATES
# --------------------------------------------------

DRAIN_RATES = {
    "Coding": 13.27,
    "Light": 13.19,
    "Video": 16.14,
    "Whatsapp": 9.42
}


# --------------------------------------------------
# BATTERY
# --------------------------------------------------

def get_battery():

    return psutil.sensors_battery()


# --------------------------------------------------
# CPU
# --------------------------------------------------

def get_cpu():
    return psutil.cpu_percent(interval=0.1)


# --------------------------------------------------
# RAM
# --------------------------------------------------

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

                    cpu = (
                        process.info["cpu_percent"]
                        or 0
                    )

                    memory = (
                        process.info["memory_percent"]
                        or 0
                    )

                    if display_name not in active_apps:

                        active_apps[display_name] = {
                            "cpu": cpu,
                            "memory": memory
                        }

                    else:

                        active_apps[
                            display_name
                        ]["cpu"] += cpu

                        active_apps[
                            display_name
                        ]["memory"] += memory

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):

            pass

    return active_apps


# --------------------------------------------------
# PRESSURE
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

        level = "Critical"

    elif score >= 50:

        level = "High"

    elif score >= 30:

        level = "Moderate"

    else:

        level = "Normal"


    return level, score


# --------------------------------------------------
# TIME ESTIMATION
# --------------------------------------------------

def estimate_time(
    battery,
    workload
):

    drain = DRAIN_RATES.get(
        workload,
        13.19
    )

    if drain <= 0:

        return 0

    return battery / drain


def format_time(hours):

    total_minutes = int(
        hours * 60
    )

    h = total_minutes // 60
    m = total_minutes % 60

    return f"{h}h {m}m"


# --------------------------------------------------
# CREATE ML INPUT
# --------------------------------------------------

def create_features(
    battery,
    cpu,
    ram,
    apps,
    charging,
    seconds_left
):

    values = {

        "Battery": battery,

        "CPU": cpu,

        "RAM": ram,

        "Brightness": 23,

        "Charging": int(
            charging
        ),

        "Estimated_Seconds_Left":
            seconds_left,

        "Chrome":
            1 if "Chrome" in apps else 0,

        "VSCode":
            1 if "VSCode" in apps else 0,

        "WhatsApp":
            1 if "WhatsApp" in apps else 0,

        "OneNote":
            1 if "OneNote" in apps else 0,

        "WPS":
            1 if "WPS" in apps else 0,

        "Active_App_Count":
            len(apps)
    }

    return values


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

        recommendations.append(
            "Enable Battery Saver / power-saving mode."
        )


    if battery <= 20:

        recommendations.append(
            "Reduce screen brightness to around 20-30%."
        )


    if workload == "Video":

        recommendations.append(
            "Reduce screen brightness for video playback."
        )


    for name, data in apps.items():

        if data["memory"] >= 10:

            recommendations.append(
                f"Close {name} if not needed."
            )


        if data["cpu"] >= 10:

            recommendations.append(
                f"Reduce activity in {name}."
            )


    if ram >= 65:

        recommendations.append(
            "Close unused applications."
        )

    elif ram >= 60:

        recommendations.append(
            "Review unused applications."
        )


    if cpu >= 20:

        recommendations.append(
            "Reduce unnecessary background processes."
        )


    if not recommendations:

        recommendations.append(
            "No immediate optimization required."
        )


    return recommendations


# --------------------------------------------------
# MAIN STATUS FUNCTION
# --------------------------------------------------

def get_system_status():

    battery_info = get_battery()


    if battery_info is None:

        return {
            "error":
                "Battery information unavailable."
        }


    battery = battery_info.percent

    charging = battery_info.power_plugged

    seconds_left = battery_info.secsleft


    if seconds_left in (
        psutil.POWER_TIME_UNKNOWN,
        psutil.POWER_TIME_UNLIMITED
    ):

        seconds_left = -1


    cpu = get_cpu()

    ram = get_ram()

    apps = get_active_apps()


    features = create_features(
        battery,
        cpu,
        ram,
        apps,
        charging,
        seconds_left
    )


    # --------------------------------------------------
    # ML WORKLOAD PREDICTION
    # --------------------------------------------------

    workload_input = [
        features[feature]
        for feature in workload_features
    ]


    workload = workload_model.predict(
        [workload_input]
    )[0]


    # --------------------------------------------------
    # ML BATTERY PREDICTION
    # --------------------------------------------------

    battery_input = [
        features[feature]
        for feature in battery_features
    ]


    predicted_battery = (
        battery_model.predict(
            [battery_input]
        )[0]
    )


    # --------------------------------------------------
    # PRESSURE
    # --------------------------------------------------

    pressure, score = get_pressure(
        battery,
        cpu,
        ram
    )


    # --------------------------------------------------
    # TIME
    # --------------------------------------------------

    drain_rate = DRAIN_RATES.get(
        workload,
        13.19
    )


    remaining_hours = estimate_time(
        battery,
        workload
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


    # --------------------------------------------------
    # APPLICATION OUTPUT
    # --------------------------------------------------

    application_list = []


    for name, data in apps.items():

        application_list.append({

            "name": name,

            "cpu": round(
                data["cpu"],
                1
            ),

            "ram": round(
                data["memory"],
                1
            )
        })


    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return {

        "battery": round(
            battery,
            1
        ),

        "charging":
            charging,

        "cpu": round(
            cpu,
            1
        ),

        "ram": round(
            ram,
            1
        ),

        "workload":
            workload,

        "battery_pressure":
            pressure,

        "pressure_score":
            score,

        "estimated_remaining_time":
            format_time(
                remaining_hours
            ),

        "historical_drain_rate":
            round(
                drain_rate,
                2
            ),

        "ml_predicted_battery":
            round(
                float(predicted_battery),
                1
            ),

        "applications":
            application_list,

        "recommendations":
            recommendations
    }


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message":
            "Battery Optimization System API",

        "status":
            "running"
    }

@app.get("/status")
def status():

    return get_system_status()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)