def savings_rate(monthly_summary):

    total_income = monthly_summary['Credit'].sum()
    total_expense = monthly_summary['Debit'].sum()

    if total_income > 0:
        rate = ((total_income - total_expense) / total_income) * 100
    else:
        rate = 0

    return rate


def generate_basic_insights(monthly_summary, category_spend):

    highest_month = monthly_summary['Debit'].idxmax()
    top_category = category_spend.idxmax()

    return {
        "highest_spend_month": str(highest_month),
        "top_category": top_category
    }
