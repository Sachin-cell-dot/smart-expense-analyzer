
import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/raw/credit_card/credit_card_transaction_flow.csv"
)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y"
)

# Extract month and year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

# Monthly spending
monthly_spending = (
    df.groupby("Month")["Transaction Amount"]
    .agg(["sum", "count", "mean"])
)

print("\n========== MONTHLY SPENDING ==========")
print(monthly_spending)

# Category-wise monthly spending
monthly_category = pd.pivot_table(
    df,
    values="Transaction Amount",
    index="Month_Name",
    columns="Category",
    aggfunc="sum"
)

print("\n========== MONTHLY CATEGORY SPENDING ==========")
print(monthly_category)
