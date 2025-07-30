import pandas as pd
def filter_data(df, state, year, quarter):
    if state != "All":
        df = df[df['State'] == state]
    if year != "All":
        df = df[df['Year'] == year]
    if quarter != "All":
        df = df[df['Quarter'] == quarter]
    return df

def get_kpis(df):
    total_amount = df['Transaction_amount'].sum()
    total_count = df['Transaction_count'].sum()
    unique_types = df['Transaction_type'].nunique()
    return total_amount, total_count, unique_types

def transaction_by_type(df):
    return df.groupby('Transaction_type')['Transaction_amount'].sum().sort_values()

def user_kpis(df):
    total_app_opens = df['AppOpens'].sum() if 'AppOpens' in df.columns else 0
    total_users = df['RegisteredUsers'].sum() if 'RegisteredUsers' in df.columns else 0
    return total_app_opens, total_users

def device_usage(df):
    return df.groupby('Brand')['Count'].sum().sort_values(ascending=False)

def top_kpi_by_location(df, col='Name', value='Transaction_amount', top_n=10):
    return df.groupby(col)[value].sum().sort_values(ascending=False).head(top_n)

def get_transaction_trend(df, state, trans_type):
    df = df.copy()
    if state != "All":
        df = df[df['State'] == state]
    if trans_type != "All":
        df = df[df['Transaction_type'] == trans_type]
    if df.empty:
        return pd.DataFrame()
    
    df["YearQuarter"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    trend_summary = df.groupby("YearQuarter")["Transaction_amount"].sum().reset_index()
    return trend_summary

def filter_insurance_data(df, state, year, quarter):
    if state != "All":
        df = df[df["State"] == state]
    if year != "All":
        df = df[df["Year"] == year]
    if quarter != "All":
        df = df[df["Quarter"] == quarter]
    return df

def insurance_kpis(df):
    total_amount = df["Transaction_amount"].sum()
    total_count = df["Transaction_count"].sum()
    unique_types = df["Type"].nunique()
    return total_amount, total_count, unique_types

def insurance_by_type(df):
    return df.groupby("Type")["Transaction_amount"].sum().reset_index()