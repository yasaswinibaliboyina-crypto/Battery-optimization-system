import psutil

battery = psutil.sensors_battery()

print("Battery:", battery.percent, "%")
print("Charging:", battery.power_plugged)
print("Remaining seconds:", battery.secsleft)