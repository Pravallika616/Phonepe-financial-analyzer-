from src.preprocessing import load_and_clean_data
from src.analysis import generate_monthly_summary, category_expense
from src.report import savings_rate, generate_basic_insights

def main():

    df = load_and_clean_data(r"C:\Users\Suhana\OneDrive\Desktop\Phonepe-financial-analyzer-\data\sample_transaction.csv")

    monthly_summary = generate_monthly_summary(df)
    category_spend = category_expense(df)

    rate = savings_rate(monthly_summary)
    insights = generate_basic_insights(monthly_summary, category_spend)

    print(f"Your savings rate is {rate:.2f}%")
    print("Highest spending month:", insights["highest_spend_month"])
    print("Top category:", insights["top_category"])

if __name__ == "__main__":
    main()