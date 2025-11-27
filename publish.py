import pandas as pd
from sqlalchemy import create_engine, text
import gspread
from gspread_dataframe import set_with_dataframe

def run_publish():
    engine = create_engine("postgresql://admin:secure_password@localhost:5432/1000000_bandcamp_sales")
    table_name = "production"
    df = pd.read_sql_table(table_name, con=engine, schema="public")
    print("Data from PostgreSQL:" , df.head())

    # Google Sheet
    SERVICE_ACCOUNT_FILE = "ageless-arcanum-479310-k7-cbe8a06a0176.json"
    SHEET_NAME = "production"
    WORKSHEET_NAME = "production"

    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = gc.open(SHEET_NAME)

    required_cols = df.shape[1]
    required_rows = 10000

    # print(required_cols)
    # print(required_rows)
    # print("total cell use")
    # print((required_cols)*(required_rows))
    try:
        worksheet = sh.worksheet(WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=WORKSHEET_NAME, rows=str(required_rows + 10), cols=str(required_cols + 5))

    if worksheet.col_count < required_cols:
        worksheet.resize(cols=required_cols)
    if worksheet.row_count < required_rows:
        worksheet.resize(rows=required_rows)

    worksheet.clear()
    set_with_dataframe(worksheet, df.head(200000))
    print(f"Published to {SHEET_NAME} -> {WORKSHEET_NAME}")

if __name__ == "__main__":
    print("Script started...")
    run_publish()
