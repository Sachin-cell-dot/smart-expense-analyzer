import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_expenses.csv")

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# 1. Overall spending statistics
print("\n========== OVERALL SPENDING ==========")

print("Total Spending:", df["Transaction Amount"].sum())
print("Average Transaction:", df["Transaction Amount"].mean())
print("Median Transaction:", df["Transaction Amount"].median())
print("Maximum Transaction:", df["Transaction Amount"].max())
print("Minimum Transaction:", df["Transaction Amount"].min())


# 2. Category-wise spending
print("\n========== CATEGORY ANALYSIS ==========")

category_analysis = (
    df.groupby("Category")["Transaction Amount"]
    .agg(["sum", "count", "mean"])
    .sort_values("sum", ascending=False)
)

category_analysis["Percentage"] = (
    category_analysis["sum"] /
    category_analysis["sum"].sum()
) * 100

print(category_analysis)


# 3. Monthly spending
print("\n========== MONTHLY ANALYSIS ==========")

monthly_analysis = (
    df.groupby(df["Date"].dt.to_period("M"))["Transaction Amount"]
    .agg(["sum", "count", "mean"])
    .sort_index()
)

print(monthly_analysis)


# 4. Top 10 merchants by transaction count
print("\n========== TOP 10 MERCHANTS ==========")

print(
    df["Merchant Name"]
    .value_counts()
    .head(10)
)


# 5. Top 10 merchants by transaction value
print("\n========== TOP 10 MERCHANTS BY SPENDING ==========")

print(
    df.groupby("Merchant Name")["Transaction Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)