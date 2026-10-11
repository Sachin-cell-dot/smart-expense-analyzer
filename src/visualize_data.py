
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/raw/credit_card/credit_card_transaction_flow.csv"
)

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y"
)

df["Year_Month"] = df["Date"].dt.to_period("M")

# 1. Category-wise spending
category_spending = (
    df.groupby("Category")["Transaction Amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 5))
category_spending.plot(kind="bar")
plt.title("Total Spending by Category")
plt.xlabel("Category")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Monthly spending trend
monthly_spending = (
    df.groupby("Year_Month")["Transaction Amount"]
    .sum()
)

plt.figure(figsize=(10, 5))
monthly_spending.plot(kind="line", marker="o")
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Transaction distribution
plt.figure(figsize=(8, 5))
df["Category"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Transactions by Category")
plt.ylabel("")
plt.tight_layout()
plt.show()
