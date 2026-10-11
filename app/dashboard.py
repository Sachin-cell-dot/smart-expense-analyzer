import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    df["Date"] = pd.to_datetime(df["Date"])

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Check your data folder.")
    st.stop()


# ==========================================
# 3. HEADER
# ==========================================

st.title("💰 Smart Expense & Spending Analyzer")

st.write(
    "An interactive application to explore transaction "
    "patterns, spending categories and merchant activity."
)

st.divider()


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎛️ Dashboard Controls")

categories = sorted(df["Category"].unique())

if "reset_filters" not in st.session_state:
    st.session_state.reset_filters = False

if st.sidebar.button("🔄 Reset All Filters"):
    st.session_state.reset_filters = True
    st.rerun()

if st.session_state.reset_filters:
    for key in ["category_filter", "date_filter",
                "amount_filter", "merchant_filter"]:
        st.session_state.pop(key, None)

    st.session_state.reset_filters = False

st.sidebar.subheader("Category")

selected_categories = st.sidebar.multiselect(
    "Choose categories",
    categories,
    default=categories,
    key="category_filter"
)

st.sidebar.subheader("Date Range")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="date_filter"
)

st.sidebar.subheader("Transaction Amount")

min_amount = float(df["Transaction Amount"].min())
max_amount = float(df["Transaction Amount"].max())

selected_amounts = st.sidebar.slider(
    "Choose amount range",
    min_value=min_amount,
    max_value=max_amount,
    value=(min_amount, max_amount),
    key="amount_filter"
)

st.sidebar.subheader("Merchant Search")

merchant_search = st.sidebar.text_input(
    "Search merchant",
    placeholder="Enter merchant name...",
    key="merchant_filter"
)

# ==========================================
# 5. FILTER DATA
# ==========================================

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_categories)
]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]

filtered_df = filtered_df[
    (filtered_df["Transaction Amount"] >= selected_amounts[0])
    & (filtered_df["Transaction Amount"] <= selected_amounts[1])
]

if merchant_search:
    filtered_df = filtered_df[
        filtered_df["Merchant Name"].str.contains(
            merchant_search,
            case=False,
            na=False
        )
    ]


# ==========================================
# 6. HANDLE EMPTY DATA
# ==========================================

if filtered_df.empty:
    st.warning(
        "No transactions match your filters. "
        "Try changing your selections."
    )
    st.stop()


# ==========================================
# 7. KPI METRICS
# ==========================================

total_spending = filtered_df["Transaction Amount"].sum()

average_transaction = filtered_df["Transaction Amount"].mean()

median_transaction = filtered_df["Transaction Amount"].median()

total_transactions = len(filtered_df)

highest_category = (
    filtered_df.groupby("Category")["Transaction Amount"]
    .sum()
    .idxmax()
)

st.subheader("📊 Spending Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transaction Value",
    f"{total_spending:,.2f}"
)

col2.metric(
    "Average Transaction",
    f"{average_transaction:,.2f}"
)

col3.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col4.metric(
    "Top Category",
    highest_category
)

st.caption(
    f"Analysis based on {total_transactions:,} filtered transactions."
)

st.divider()


# ==========================================
# 8. CATEGORY DISTRIBUTION
# ==========================================

st.subheader("📂 Category Distribution")

category_spending = (
    filtered_df.groupby("Category")["Transaction Amount"]
    .sum()
    .reset_index()
    .sort_values("Transaction Amount", ascending=False)
)

fig_category = px.pie(
    category_spending,
    names="Category",
    values="Transaction Amount",
    hole=0.45,
    title="Spending Distribution by Category"
)

fig_category.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)

st.subheader("📊 Category Spending Breakdown")

category_breakdown = (
    filtered_df.groupby("Category")["Transaction Amount"]
    .agg(["sum", "count", "mean"])
    .reset_index()
)

category_breakdown["Percentage"] = (
    category_breakdown["sum"] / total_spending
) * 100

st.dataframe(
    category_breakdown,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 9. MONTHLY SPENDING TREND
# ==========================================

st.subheader("📈 Monthly Spending Trend")

monthly_spending = (
    filtered_df
    .assign(Month=filtered_df["Date"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)["Transaction Amount"]
    .sum()
)

fig_monthly = px.line(
    monthly_spending,
    x="Month",
    y="Transaction Amount",
    markers=True,
    title="Monthly Transaction Value"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Transaction Value"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

st.caption(
    "October 2023 contains data only through October 14 "
    "in the original dataset."
)


# ==========================================
# 10. TOP MERCHANTS
# ==========================================

st.subheader("🏪 Merchant Analysis")

merchant_spending = (
    filtered_df.groupby("Merchant Name")["Transaction Amount"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig_merchant = px.bar(
    merchant_spending.sort_values("Transaction Amount"),
    x="Transaction Amount",
    y="Merchant Name",
    orientation="h",
    title="Top 10 Merchants by Transaction Value"
)

st.plotly_chart(
    fig_merchant,
    use_container_width=True
)


# ==========================================
# 11. SMART INSIGHTS
# ==========================================

st.subheader("💡 Smart Spending Insights")

highest_category_name = category_spending.iloc[0]["Category"]

category_percentage = (
    category_spending.iloc[0]["Transaction Amount"]
    / total_spending
) * 100

highest_month = (
    monthly_spending.loc[
        monthly_spending["Transaction Amount"].idxmax(),
        "Month"
    ]
)

largest_transaction = filtered_df.loc[
    filtered_df["Transaction Amount"].idxmax()
]

top_merchant = merchant_spending.iloc[0]["Merchant Name"]

col1, col2 = st.columns(2)

with col1:
    st.info(f"Highest spending category: **{highest_category_name}**")

    st.info(f"Category contribution: **{category_percentage:.2f}%**")

    st.info(f"Highest transaction-value month: **{highest_month}**")

with col2:
    st.info(f"Top merchant: **{top_merchant}**")

    st.info(
        f"Largest transaction: "
        f"**{largest_transaction['Transaction Amount']:,.2f}**"
    )

    st.info(f"Median transaction: **{median_transaction:,.2f}**")

# ==========================================
# ML ANOMALY DETECTION
# ==========================================

st.divider()

st.subheader("🤖 Machine Learning Anomaly Detection")

st.write(
    "Isolation Forest identifies transactions "
    "that have unusual patterns based on transaction "
    "amount, month and day of week."
)

# Separate normal and unusual transactions
anomaly_df = filtered_df[
    filtered_df["Anomaly"] == "Anomaly"
]

normal_df = filtered_df[
    filtered_df["Anomaly"] == "Normal"
]

total_flagged = len(anomaly_df)
total_normal = len(normal_df)

anomaly_percentage = (
    total_flagged / len(filtered_df)
) * 100

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Flagged Transactions",
    f"{total_flagged:,}"
)

col2.metric(
    "Normal Transactions",
    f"{total_normal:,}"
)

col3.metric(
    "Flagged Percentage",
    f"{anomaly_percentage:.2f}%"
)

# Distribution chart
anomaly_counts = pd.DataFrame({
    "Transaction Type": ["Normal", "Anomaly"],
    "Count": [total_normal, total_flagged]
})

fig_anomaly = px.pie(
    anomaly_counts,
    names="Transaction Type",
    values="Count",
    hole=0.5,
    title="Normal vs Unusual Transactions",
    color="Transaction Type",
    color_discrete_map={
        "Normal": "#16A34A",
        "Anomaly": "#EF4444"
    }
)

st.plotly_chart(
    fig_anomaly,
    use_container_width=True
)

# Anomaly transaction table
st.subheader("🚨 Flagged Transactions")

if not anomaly_df.empty:

    st.write(
        "These transactions were identified as unusual "
        "by the Isolation Forest model."
    )

    st.dataframe(
        anomaly_df[
            [
                "Date",
                "Category",
                "Merchant Name",
                "Transaction Amount",
                "Anomaly"
            ]
        ].sort_values(
            "Transaction Amount",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    # Download flagged transactions
    anomaly_csv = anomaly_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Flagged Transactions",
        data=anomaly_csv,
        file_name="flagged_transactions.csv",
        mime="text/csv"
    )

else:
    st.success(
        "No unusual transactions found for the selected filters."
    )

st.caption(
    "Note: Anomaly means statistically unusual according "
    "to the model. It does not mean confirmed fraud."
)

# ==========================================
# 12. UNUSUAL TRANSACTION DETECTION
# ==========================================

st.subheader("🚨 Unusually Large Transactions")

q1 = filtered_df["Transaction Amount"].quantile(0.25)
q3 = filtered_df["Transaction Amount"].quantile(0.75)

iqr = q3 - q1

upper_limit = q3 + (1.5 * iqr)

unusual_transactions = filtered_df[
    filtered_df["Transaction Amount"] > upper_limit
]

st.write(
    f"Transactions above the statistical threshold "
    f"({upper_limit:,.2f}): {len(unusual_transactions)}"
)

if not unusual_transactions.empty:
    st.dataframe(
        unusual_transactions.sort_values(
            "Transaction Amount",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("No unusually large transactions found.")


# ==========================================
# 13. TRANSACTION EXPLORER
# ==========================================

st.subheader("🔎 Transaction Explorer")

search_text = st.text_input(
    "Search within filtered transactions",
    placeholder="Search category or merchant..."
)

transaction_view = filtered_df.copy()

if search_text:
    mask = (
        transaction_view["Category"].str.contains(
            search_text,
            case=False,
            na=False
        )
        |
        transaction_view["Merchant Name"].str.contains(
            search_text,
            case=False,
            na=False
        )
    )

    transaction_view = transaction_view[mask]

st.write(f"Showing {len(transaction_view):,} transactions")

st.dataframe(
    transaction_view.sort_values(
        "Date",
        ascending=False
    ),
    width="stretch",
    hide_index=True
)


# ==========================================
# 14. DOWNLOAD REPORT
# ==========================================

csv_data = transaction_view.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Transaction Report",
    data=csv_data,
    file_name="expense_analysis_report.csv",
    mime="text/csv"
)


# ==========================================
# 15. FOOTER
# ==========================================

st.divider()

st.caption(
    "Smart Expense & Spending Analyzer | "
    "Python • Pandas • Plotly • Streamlit"
)

st.caption(
    "Transaction amounts are shown in dataset units; "
    "the dataset does not specify a currency."
)