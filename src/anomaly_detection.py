import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load dataset
df = pd.read_csv(
    "data/processed/cleaned_expenses.csv"
)

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# Feature engineering
df["Month"] = df["Date"].dt.month
df["DayOfWeek"] = df["Date"].dt.dayofweek

# Select features
features = [
    "Transaction Amount",
    "Month",
    "DayOfWeek"
]

X = df[features]

# Train Isolation Forest
model = IsolationForest(
    n_estimators=100,
    contamination=0.02,
    random_state=42
)

model.fit(X)

# Predict anomalies
df["Anomaly"] = model.predict(X)

# Convert predictions
df["Anomaly"] = df["Anomaly"].map({
    1: "Normal",
    -1: "Anomaly"
})

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/isolation_forest.pkl"
)

# Save results
os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    "data/processed/anomaly_results.csv",
    index=False
)

# Display results
print("\n========== ANOMALY DETECTION RESULTS ==========")

print(df["Anomaly"].value_counts())

print("\n========== TOP FLAGGED TRANSACTIONS ==========")

print(
    df[df["Anomaly"] == "Anomaly"]
    [["Transaction Amount", "Category", "Date"]]
    .head(10)
)

print("\nModel saved successfully!")