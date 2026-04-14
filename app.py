import streamlit as st
import pandas as pd

from src.preprocessing import load_and_clean_data
from src.analysis import generate_monthly_summary, category_expense
from src.report import savings_rate

st.set_page_config(page_title="AI Personal Finance Analyzer", layout="wide")

st.title("💰 AI-Powered Personal Finance Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

if uploaded_file:

    # Load data
    df = load_and_clean_data(uploaded_file)

    # Generate analysis
    monthly_summary = generate_monthly_summary(df)
    category_spend = category_expense(df)
    rate = savings_rate(monthly_summary)

    # ========================
    # 📊 Metrics Section
    # ========================
    total_income = monthly_summary['Credit'].sum()
    total_expense = monthly_summary['Debit'].sum()
    total_savings = total_income - total_expense

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"₹ {total_income:,.2f}")
    col2.metric("Total Expense", f"₹ {total_expense:,.2f}")
    col3.metric("Savings Rate", f"{rate:.2f}%")

    st.divider()

    # ========================
    # 📈 Monthly Trend
    # ========================
    st.subheader("📈 Monthly Spending Trend")
    st.line_chart(monthly_summary[['Debit', 'Credit']])

    # ========================
    # 📊 Category Breakdown
    # ========================
    st.subheader("📊 Expense by Category")
    st.bar_chart(category_spend)

    # ========================
    # 📋 Raw Data (Optional)
    # ========================
    with st.expander("View Raw Data"):
        st.dataframe(df)

else:
    st.info("Upload a CSV file to start analysis.")
