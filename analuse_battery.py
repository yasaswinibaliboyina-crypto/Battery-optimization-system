import pandas as pd

df = pd.read_csv("battery_data_v3.csv")

df["Time"] = pd.to_datetime(df["Time"])

start_battery = df["Battery"].iloc[0]
end_battery = df["Battery"].iloc[-1]

start_time = df["Time"].iloc[0]
end_time = df["Time"].iloc[-1]

duration_minutes = (end_time - start_time).total_seconds() / 60

battery_used = start_battery - end_battery

if duration_minutes > 0:
    drain_per_hour = battery_used / duration_minutes * 60
else:
    drain_per_hour = 0

print("Start battery:", start_battery, "%")
print("End battery:", end_battery, "%")
print("Battery used:", battery_used, "%")
print("Duration:", round(duration_minutes, 2), "minutes")
print("Estimated drain:", round(drain_per_hour, 2), "% per hour")
print()
print("Average CPU:", round(df["CPU"].mean(), 2), "%")
print("Average RAM:", round(df["RAM"].mean(), 2), "%")
