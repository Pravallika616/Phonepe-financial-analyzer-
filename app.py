import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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
    monthly_summary = generate_monthly_summary(df)

    # 🔥 FIX: Convert PeriodIndex to datetime
    if isinstance(monthly_summary.index, pd.PeriodIndex):
        monthly_summary.index = monthly_summary.index.to_timestamp()
    category_spend = category_expense(df)
    rate = savings_rate(monthly_summary)

    # ========================
    # 📊 KPI Metrics
    # ========================
    total_income = monthly_summary['Credit'].sum()
    total_expense = monthly_summary['Debit'].sum()
    net_savings = total_income - total_expense

    avg_monthly_spend = monthly_summary['Debit'].mean()

    top_category = category_spend.idxmax()
    top_category_value = category_spend.max()

    highest_spend_month = monthly_summary['Debit'].idxmax()
    highest_spend_value = monthly_summary['Debit'].max()

    expense_ratio = (total_expense / total_income) * 100 if total_income != 0 else 0

    monthly_summary['Savings'] = monthly_summary['Credit'] - monthly_summary['Debit']
    saving_consistency = (
        (monthly_summary['Savings'] > 0).sum() / len(monthly_summary)
    ) * 100

    # ========================
    # 🎯 KPI CARDS
    # ========================
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Income", f"₹ {total_income:,.0f}")
    col2.metric("💸 Total Expense", f"₹ {total_expense:,.0f}")
    col3.metric("📊 Savings Rate", f"{rate:.2f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("🏦 Net Savings", f"₹ {net_savings:,.0f}")
    col5.metric("📉 Avg Monthly Spend", f"₹ {avg_monthly_spend:,.0f}")
    col6.metric("⚖️ Expense Ratio", f"{expense_ratio:.2f}%")

    col7, col8 = st.columns(2)
    col7.metric("🔥 Top Category", f"{top_category}")
    col8.metric("📅 Highest Spend Month", f"{highest_spend_month}")

    st.metric("✅ Savings Consistency", f"{saving_consistency:.2f}%")

    st.divider()

    # ========================
    # 📈 Monthly Trend (Line Chart)
    # ========================
    st.subheader("📈 Income vs Expense Trend")
    fig_line = px.line(
    monthly_summary.reset_index(),
    x='Month',   # ✅ FIXED
    y=['Credit', 'Debit'],
    markers=True,
    color_discrete_sequence=["green", "red"]
    )
    fig_line.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount",
        template="plotly_dark"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # ========================
    # 🍩 Category Donut Chart
    # ========================
    st.subheader("🍩 Expense Distribution by Category")

    fig_pie = px.pie(
        values=category_spend.values,
        names=category_spend.index,
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig_pie.update_traces(textinfo='percent+label')
    fig_pie.update_layout(template="plotly_dark")

    st.plotly_chart(fig_pie, use_container_width=True)

    # ========================
    # 📊 Category Bar Chart
    # ========================
    st.subheader("📊 Category-wise Spending")

    fig_bar = px.bar(
        x=category_spend.index,
        y=category_spend.values,
        color=category_spend.values,
        color_continuous_scale="Blues"
    )

    fig_bar.update_layout(
        xaxis_title="Category",
        yaxis_title="Amount",
        template="plotly_dark"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # ========================
    # 📉 Savings Trend
    # ========================
    st.subheader("📉 Monthly Savings Trend")

    fig_savings = px.bar(
        monthly_summary,
        x=monthly_summary.index,
        y='Savings',
        color='Savings',
        color_continuous_scale="RdYlGn"
    )

    fig_savings.update_layout(template="plotly_dark")

    st.plotly_chart(fig_savings, use_container_width=True)

    # ========================
    # 🎯 Gauge Chart (Savings Rate)
    # ========================
    st.subheader("🎯 Savings Performance")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rate,
        title={'text': "Savings Rate (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"},
            ]
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    # ========================
    # 📋 Raw Data
    # ========================
    with st.expander("📋 View Raw Data"):
        st.dataframe(df)

else:

    st.info("Upload a CSV file to start analysis.")
