from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql+psycopg2://postgres:sudharsan@localhost:5432/phonepe_db')

def load_agg_transaction():
    query = "SELECT * FROM agg_transaction"
    df = pd.read_sql(query, engine)
    return df

def load_agg_user():
    query = "SELECT * FROM agg_user"
    df = pd.read_sql(query, engine)
    return df

def load_agg_user_device():
    query = "SELECT * FROM agg_user_device"
    df = pd.read_sql(query, engine)
    return df

def load_top_transaction_district():
    return pd.read_sql("SELECT * FROM top_transaction_district", engine)

def load_top_transaction_pincode():
    return pd.read_sql("SELECT * FROM top_transaction_pincode", engine)

def load_top_user_district():
    return pd.read_sql("SELECT * FROM top_user_district", engine)

def load_top_user_pincode():
    return pd.read_sql("SELECT * FROM top_user_pincode", engine)

def load_agg_insurance():
    return pd.read_sql("SELECT * FROM agg_insurance", engine)

def load_map_insurance_country():
    return pd.read_sql("SELECT * FROM map_insurance_country", engine)

def load_map_insurance_country_meta():
    return pd.read_sql("SELECT * FROM map_insurance_country_meta", engine)

def load_map_insurance_hover():
    return pd.read_sql("SELECT * FROM map_insurance_hover", engine)

def load_top_insurance_district():
    return pd.read_sql("SELECT * FROM top_insurance_district", engine)

def load_top_insurance_pincode():
    return pd.read_sql("SELECT * FROM top_insurance_pincode", engine)