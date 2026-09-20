import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score


print("=" * 50)
print("       BATTERY OPTIMIZATION - ML TRAINING")
print("=" * 50)


# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

df = pd.read_csv("battery_augmented.csv")

print("\nDataset loaded.")
print("Total rows:", len(df))


# --------------------------------------------------
# 2. FEATURES
# --------------------------------------------------

features = [
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
    "Active_App_Count"
]

X = df[features].copy()


# Convert True/False to 0/1
X["Charging"] = X["Charging"].astype(int)


# --------------------------------------------------
# 3. WORKLOAD CLASSIFICATION
# --------------------------------------------------

print("\n" + "-" * 50)
print("WORKLOAD CLASSIFICATION")
print("-" * 50)

y_workload = df["workload"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_workload,
    test_size=0.2,
    random_state=42,
    stratify=y_workload
)


workload_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)


workload_model.fit(
    X_train,
    y_train
)


predictions = workload_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("Workload model accuracy:",
      round(accuracy * 100, 2),
      "%")


# Save workload model
joblib.dump(
    workload_model,
    "workload_model.pkl"
)

print("Saved: workload_model.pkl")


# --------------------------------------------------
# 4. BATTERY PREDICTION
# --------------------------------------------------

print("\n" + "-" * 50)
print("BATTERY PREDICTION")
print("-" * 50)


# We predict remaining battery percentage
# using system conditions.

battery_features = [
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
    "Active_App_Count"
]


X_battery = df[battery_features].copy()

X_battery["Charging"] = X_battery["Charging"].astype(int)


y_battery = df["Battery"]


X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(
    X_battery,
    y_battery,
    test_size=0.2,
    random_state=42
)


battery_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


battery_model.fit(
    X_train_b,
    y_train_b
)


battery_predictions = battery_model.predict(
    X_test_b
)


mae = mean_absolute_error(
    y_test_b,
    battery_predictions
)

r2 = r2_score(
    y_test_b,
    battery_predictions
)


print("Battery prediction MAE:",
      round(mae, 2))

print("Battery prediction R2:",
      round(r2, 3))


# Save battery model
joblib.dump(
    battery_model,
    "battery_model.pkl"
)

print("Saved: battery_model.pkl")


# --------------------------------------------------
# 5. SAVE FEATURE LISTS
# --------------------------------------------------

joblib.dump(
    features,
    "workload_features.pkl"
)

joblib.dump(
    battery_features,
    "battery_features.pkl"
)


print("\nSaved:")
print("- workload_model.pkl")
print("- battery_model.pkl")
print("- workload_features.pkl")
print("- battery_features.pkl")


# --------------------------------------------------
# 6. TEST MODEL WITH ONE SAMPLE
# --------------------------------------------------

print("\n" + "-" * 50)
print("MODEL TEST")
print("-" * 50)


sample = X.iloc[[0]]

predicted_workload = workload_model.predict(
    sample
)[0]


battery_sample = X_battery.iloc[[0]]

predicted_battery = battery_model.predict(
    battery_sample
)[0]


print("Predicted workload:",
      predicted_workload)

print("Predicted battery:",
      round(predicted_battery, 2),
      "%")


print("\n" + "=" * 50)
print("ML TRAINING COMPLETED")
print("=" * 50)