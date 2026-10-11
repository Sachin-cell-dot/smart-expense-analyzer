import pandas as pd
import os

# Load original dataset
df = pd.read_csv(
    "data/raw/credit_card/credit_card_transaction_flow.csv"
)

print("Original dataset shape:", df.shape)

# 1. Remove duplicate records
df = df.drop_duplicates()

# 2. Convert Date into datetime format
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# 3. Handle missing Gender values
df["Gender"] = df["Gender"].fillna("Unknown")

# 4. Remove unnecessary personal information
df = df.drop(
    columns=["Name", "Surname", "Birthdate", "Customer ID"]
)

# 5. Remove records with invalid dates or amounts
df = df.dropna(
    subset=["Date", "Transaction Amount", "Category"]
)

# 6. Keep only valid positive transaction amounts
df = df[df["Transaction Amount"] > 0]

# 7. Create useful date columns
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

# Create processed-data folder
os.makedirs("data/processed", exist_ok=True)

# Save cleaned dataset
df.to_csv(
    "data/processed/cleaned_expenses.csv",
    index=False
)

print("\n========== CLEANING SUMMARY ==========")
print("Cleaned dataset shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate records:", df.duplicated().sum())
print("\nCleaned dataset saved successfully!")