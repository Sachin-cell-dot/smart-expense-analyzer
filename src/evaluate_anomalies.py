
import pandas as pd

print("Starting anomaly evaluation...")

# Load model predictions
df = pd.read_csv(
    "data/processed/anomaly_results.csv"
)

print("\n========== DATASET OVERVIEW ==========")
print("Total transactions:", len(df))

# 1. Compare normal and anomaly transactions
print("\n========== TRANSACTION STATISTICS ==========")

print(
    df.groupby("Anomaly")["Transaction Amount"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)

# 2. Category distribution of flagged transactions
print("\n========== ANOMALIES BY CATEGORY ==========")

anomalies = df[df["Anomaly"] == "Anomaly"]

print(
    anomalies["Category"].value_counts()
)

# 3. Anomaly percentage by category
print("\n========== ANOMALY RATE BY CATEGORY ==========")

df["Is_Anomaly"] = (
    df["Anomaly"] == "Anomaly"
)

category_rate = (
    df.groupby("Category")["Is_Anomaly"]
    .mean() * 100
)

print(category_rate.round(2))

# 4. Compare transaction amounts by category
print("\n========== AVERAGE TRANSACTION BY CATEGORY ==========")

print(
    df.groupby("Category")["Transaction Amount"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\n========== EVALUATION COMPLETED ==========")
