# %%

import pandas as pd

def main():
    df = pd.read_csv("data/sample_transaction.csv",sep="\t" )
    print(df.head())
    #cchecking datatypes
    print(df.dtypes)



if __name__ == "__main__":
    main()