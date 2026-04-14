def generate_monthly_summary(df):

    df['Month'] = df['Datetime'].dt.to_period('M')

    monthly_summary = df.groupby('Month', observed=True).agg({
        'Debit': 'sum',
        'Credit': 'sum'
    })

    monthly_summary['Savings'] = (
        monthly_summary['Credit'] - monthly_summary['Debit']
    )

    return monthly_summary


def category_expense(df):

    return (
        df.groupby('Category', observed=True)['Debit']
          .sum()
          .sort_values(ascending=False)
    )
