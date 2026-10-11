import pandas as pd

df = pd.read_csv("data/processed/cleaned_expenses.csv")

# Category analysis
category_spending = (
    df.groupby("Category")["Transaction Amount"]
    .sum()
    .sort_values(ascending=False)
)

total_spending = df["Transaction Amount"].sum()

highest_category = category_spending.idxmax()
highest_category_value = category_spending.max()

category_percentage = (
    highest_category_value / total_spending
) * 100

# Monthly analysis
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%Y-%m-%d"
)

monthly_spending = (
    df.groupby(df["Date"].dt.month)["Transaction Amount"]
    .sum()
)

highest_month = monthly_spending.idxmax()

month_name = pd.Timestamp(
    year=2023,
    month=highest_month,
    day=1
).strftime("%B")

# Transaction statistics
average_transaction = df["Transaction Amount"].mean()
median_transaction = df["Transaction Amount"].median()

# Merchant analysis
top_merchant = (
    df.groupby("Merchant Name")["Transaction Amount"]
    .sum()
    .idxmax()
)

print("\n========== AUTOMATIC SPENDING INSIGHTS ==========")

print(
    f"\n1. Highest spending category: {highest_category}"
)

print(
    f"2. {highest_category} contributes "
    f"{category_percentage:.2f}% of total transaction value."
)

print(
    f"3. Highest transaction-value month: {month_name}"
)

print(
    f"4. Average transaction value: {average_transaction:.2f}"
)

print(
    f"5. Median transaction value: {median_transaction:.2f}"
)

print(
    f"6. Merchant with highest transaction value: {top_merchant}"
)