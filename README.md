
# Smart Expense & Spending Analyzer

An interactive transaction analytics application built using Python, Pandas, Streamlit, Plotly and Scikit-learn.

The project analyzes 50,000 credit-card transaction records to identify spending patterns, compare categories, explore merchant activity and detect statistically unusual transactions using Isolation Forest.

## Features

- **Data preprocessing:** Handles missing values, duplicate records, date conversion and unnecessary identifying columns.
- **Exploratory data analysis:** Analyzes transaction values, categories, merchants and monthly trends.
- **Spending analytics:** Calculates total transaction value, average and median transaction values, and category contributions.
- **Interactive dashboard:** Provides category, date, amount and merchant filters.
- **Visualizations:** Interactive Plotly charts for category distribution, monthly trends and merchant rankings.
- **Automatic insights:** Identifies the highest-value category, month and merchant.
- **Anomaly detection:** Uses the Isolation Forest algorithm to identify unusual transaction patterns.
- **Transaction explorer:** Allows users to search, inspect and download filtered transaction records.

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Scikit-learn
- Joblib
- KaggleHub

## Project Structure

```text
Smart_expense_tracker/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── src/
│   ├── download_data.py
│   ├── inspect_data.py
│   ├── inspect_credit_data.py
│   ├── explore_data.py
│   ├── monthly_analysis.py
│   ├── visualize_data.py
│   ├── clean_data.py
│   ├── advanced_analysis.py
│   ├── generate_insights.py
│   ├── anomaly_detection.py
│   └── evaluate_anomalies.py
│
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

## Dataset

Dataset: [Comprehensive Credit Card Transactions Dataset](https://www.kaggle.com/datasets/rajatsurana979/comprehensive-credit-card-transactions-dataset)

The working dataset contains 50,000 transaction records and includes transaction amount, date, merchant and category information.

The dataset does not specify a currency. Therefore, transaction values are displayed in dataset units without assuming a currency.

The raw dataset and processed transaction records are excluded from this repository.

Check the dataset's license and terms before redistributing or publishing the data.

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Smart_expense_tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Download the dataset

The dataset can be downloaded using KaggleHub.

```bash
python src/download_data.py
```

Place the downloaded `credit_card_transaction_flow.csv` file at:

```text
data/raw/credit_card/credit_card_transaction_flow.csv
```

### 6. Prepare the dataset

```bash
python src/clean_data.py
```

### 7. Train the anomaly detection model

```bash
python src/anomaly_detection.py
```

### 8. Launch the dashboard

```bash
streamlit run app/dashboard.py
```

## Machine Learning

The project uses Isolation Forest, an unsupervised machine learning algorithm for anomaly detection.

Initial model features:

- Transaction Amount
- Month
- Day of Week

Model configuration:

- Estimators: 100
- Contamination: 0.02
- Random State: 42

In the initial experiment, the model flagged 1,000 of 50,000 transactions as anomalies.

These are statistically unusual observations, not confirmed fraudulent transactions. The contamination setting controls the expected proportion of flagged observations and does not establish actual fraud prevalence.

## Important Limitations

- The dataset does not specify its currency.
- The dataset contains transaction records, not a complete personal bank ledger.
- There are no verified fraud labels.
- The anomaly detection results are exploratory and require further evaluation.
- The dataset contains records from January through October 14, 2023.

## Future Improvements

- Improve anomaly detection through category-aware feature engineering.
- Evaluate different anomaly detection approaches.
- Add more advanced interactive visualizations.
- Improve dashboard design and usability.
- Deploy the application online.

## Author

Developed as a personal Data Science project to practice data preprocessing, exploratory analysis, visualization, machine learning and dashboard development.

# smart-expense-analyzer
An interactive expense analytics dashboard with spending insights and Isolation Forest-based anomaly detection
