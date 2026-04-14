
import pandas as pd
import pdfplumber
import pandas as pd
import re



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

def convert_phonepe_pdf_to_df(pdf_path):
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Split transactions using date pattern
            transactions = re.split(r'(?=\w{3} \d{1,2}, \d{4})', text)

            for txn in transactions:
                lines = txn.split("\n")

                if len(lines) < 2:
                    continue

                try:
                    # Extract Date & Time
                    date_line = lines[0]
                    time_line = lines[1]

                    # Extract Amount & Type
                    amount_match = re.search(r'₹\s?([\d,]+)', txn)
                    amount = int(amount_match.group(1).replace(",", "")) if amount_match else 0

                    txn_type = "Debit" if "DEBIT" in txn.upper() else "Credit"

                    # Extract Merchant / Description
                    desc = ""
                    for line in lines:
                        if "Paid to" in line or "Received from" in line:
                            desc = line
                            break

                    merchant = desc.replace("Paid to", "").replace("Received from", "").strip()

                    # Assign Category (basic logic)
                    if "Swiggy" in txn or "Zomato" in txn:
                        category = "Food"
                    elif "Uber" in txn or "Ola" in txn:
                        category = "Travel"
                    elif "Electricity" in txn:
                        category = "Utilities"
                    elif "Recharge" in txn or "Jio" in txn:
                        category = "Mobile Recharge"
                    else:
                        category = "Others"

                    data.append({
                        "Date": date_line,
                        "Time": time_line,
                        "Transaction_ID": "N/A",
                        "Type": txn_type,
                        "Mode": "UPI",
                        "Merchant": merchant,
                        "Category": category,
                        "Debit": amount if txn_type == "Debit" else 0,
                        "Credit": amount if txn_type == "Credit" else 0,
                        "Balance": None,
                        "Status": "Success"
                    })

                except Exception as e:
                    continue

    df = pd.DataFrame(data)
    return df