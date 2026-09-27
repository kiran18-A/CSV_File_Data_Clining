import pandas as pd
import sqlite3

DB_NAME = "customer_data.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def load_data_from_db():
    conn = get_db_connection()
    query = "SELECT * FROM customers"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Automated data transformation workflow.
    """
    # Create a copy to avoid SettingWithCopyWarning
    df_transformed = df.copy()
    
    # 1. Fill missing numeric values with 0
    numeric_cols = ['Tenure_Months', 'Monthly_Charges', 'CLTV', 'Churn_Score']
    for col in numeric_cols:
        if col in df_transformed.columns:
            df_transformed[col] = df_transformed[col].fillna(0)
            
    # 2. Fill missing categorical values with 'Unknown'
    cat_cols = ['Gender', 'Partner', 'Dependents', 'Internet_Service']
    for col in cat_cols:
         if col in df_transformed.columns:
            df_transformed[col] = df_transformed[col].fillna('Unknown')
            
    # 3. Create a new feature: Is_Long_Term_Customer (Tenure > 24 months)
    if 'Tenure_Months' in df_transformed.columns:
        df_transformed['Is_Long_Term'] = df_transformed['Tenure_Months'] > 24
        
    return df_transformed

if __name__ == "__main__":
    df = load_data_from_db()
    print(f"Loaded {len(df)} records from database.")
    transformed_df = transform_data(df)
    print(f"Data transformed. Columns added: {set(transformed_df.columns) - set(df.columns)}")