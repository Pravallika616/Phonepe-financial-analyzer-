
import pandas as pd

def load_and_clean_data(file_path):

    df = pd.read_csv(file_path, sep="\t")  # change if needed
    
    # Clean column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")

    # Convert Date properly
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')

    # Convert Time properly (12-hour format)
    df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce')

# Combine Date + Time safely
    df['Datetime'] = df['Date'] + (df['Time'] - df['Time'].dt.normalize())

# Drop old columns
    df.drop(['Date', 'Time'], axis=1, inplace=True)

# Convert ID to string
    df['Transaction_ID'] = df['Transaction_ID'].astype('string')
    

    categorical_cols = ['Type', 'Mode', 'Merchant', 'Category', 'Status']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    # Convert money columns to float
    money_cols = ['Debit', 'Credit', 'Balance']
    for col in money_cols:
        df[col] = df[col].astype(float)       

    return df
#df1=load_and_clean_data(r"C:\Users\Suhana\OneDrive\Desktop\Phonepe-financial-analyzer-\data\sample_transaction.csv")
#print(df1.dtypes)