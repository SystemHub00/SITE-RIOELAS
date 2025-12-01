import os
import gspread
from google.oauth2.service_account import Credentials

def get_gsheet_client():
    creds_path = os.environ.get("GOOGLE_SHEETS_CREDS", "plated-field-474017-b8-e00d977b2612.json")
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def append_to_sheet(data):
    client = get_gsheet_client()
    sheet = client.open_by_key("1DOiy5jkpjfOooUHs5pvsyopDeGDql1hQYVx0js_6Ob0").worksheet("DADOS")
    sheet.append_row(data)
