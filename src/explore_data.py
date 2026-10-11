
import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/raw/credit_card/credit_card_transaction_flow.csv"
)

# 1. Category distribution
print("\n========== CATEGORY DISTRIBUTION ==========")
print(df["Category"].value_counts())

# 2. Total spending
print("\n========== TOTAL TRANSACTION AMOUNT ==========")
print(df["Transaction Amount"].sum())

# 3. Average transaction
print("\n========== AVERAGE TRANSACTION ==========")
print(df["Transaction Amount"].mean())

# 4. Highest transaction
print("\n========== HIGHEST TRANSACTION ==========")
print(df["Transaction Amount"].max())

# 5. Lowest transaction
print("\n========== LOWEST TRANSACTION ==========")
print(df["Transaction Amount"].min())

# 6. Top 10 merchants by transaction count
print("\n========== TOP 10 MERCHANTS ==========")
print(df["Merchant Name"].value_counts().head(10))

# 7. Spending by category
print("\n========== SPENDING BY CATEGORY ==========")
print(
    df.groupby("Category")["Transaction Amount"]
    .agg(["count", "sum", "mean"])
    .sort_values(by="sum", ascending=False)
)

# 8. Date range (assuming DD-MM-YYYY; we'll validate it)
dates = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("\n========== DATE RANGE ==========")
print("Invalid dates:", dates.isna().sum())
print("Earliest date:", dates.min())
print("Latest date:", dates.max())
