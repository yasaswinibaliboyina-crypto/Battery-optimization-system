def battery_optimizer(battery, cpu, ram, brightness, workload, whatsapp, active_apps):

    score = 0
    reasons = []
    recommendations = []

    # Battery pressure
    if battery <= 10:
        score += 60
        reasons.append("Battery level is critically low.")
    elif battery <= 20:
        score += 45
        reasons.append("Battery level is very low.")
    elif battery <= 30:
        score += 25
        reasons.append("Battery level is getting low.")

    # CPU pressure
    if cpu >= 15:
        score += 25
        reasons.append("CPU usage is high.")
    elif cpu >= 10:
        score += 15
        reasons.append("CPU usage is moderately high.")

    # RAM pressure
    if ram >= 63:
        score += 20
        reasons.append("RAM usage is high.")
    elif ram >= 61:
        score += 10
        reasons.append("RAM usage is moderately high.")

    # Multiple applications
    if active_apps >= 4:
        score += 10
        reasons.append("Multiple applications are active.")

    # Workload-specific recommendations
    if workload == "Video" and battery <= 20:
        recommendations.append(
            "Reduce screen brightness for video playback."
        )

    if workload == "Coding" and battery <= 20:
        recommendations.append(
            "Close unnecessary background applications while coding."
        )

    if workload == "Whatsapp" and battery <= 20 and whatsapp == 1:
        recommendations.append(
            "Close WhatsApp Web if it is not currently needed."
        )

    if ram >= 63:
        recommendations.append(
            "Close unused applications to reduce memory usage."
        )

    if cpu >= 15:
        recommendations.append(
            "Reduce unnecessary background processes."
        )

    if battery <= 20:
        recommendations.append(
            "Enable battery saver / power-saving mode."
        )

    # Pressure level
    if battery <= 10 or score >= 70:
        level = "Critical"
    elif battery <= 20 or score >= 50:
        level = "High"
    elif battery <= 30 or score >= 30:
        level = "Moderate"
    else:
        level = "Normal"

    if not reasons:
        reasons.append(
            "System resource usage is currently within normal limits."
        )

    if not recommendations:
        recommendations.append(
            "No immediate optimization required."
        )

    return level, score, reasons, recommendations