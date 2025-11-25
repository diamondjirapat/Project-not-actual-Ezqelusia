import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('1000000-bandcamp-sales.csv')

engine = create_engine('postgresql://admin:secure_password@localhost:5432/1000000_bandcamp_sales')

try:
    df.to_sql(
        name='raw_data',
        con=engine,
        if_exists='append',
        index=False
    )
    print("successful")

except Exception as e:
    print(f"Error: {e}")
