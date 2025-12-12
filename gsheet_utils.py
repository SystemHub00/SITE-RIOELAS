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
    sheet_id = os.environ.get("GOOGLE_SHEETS_ID", "1DOiy5jkpjfOooUHs5pvsyopDeGDql1hQYVx0js_6Ob0")
    sheet_name = os.environ.get("GOOGLE_SHEETS_TAB", "DADOS")
    max_leads = int(os.environ.get("GOOGLE_SHEETS_MAX_LEADS", 1000))
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    # Cabeçalho desejado
    header = [
        'Data/Hora Envio',
        'Protocolo', 'Nome', 'CPF', 'Nascimento', 'Whatsapp', 'Email',
        'CEP', 'Endereço', 'Número', 'Complemento', 'Bairro', 'Cidade', 'Estado',
        'Curso', 'Como Conheceu'
    ]
    # Verifica se o cabeçalho já existe
    existing_header = sheet.row_values(1)
    if existing_header != header:
        sheet.insert_row(header, 1)
    # Proteção: não salva se já atingiu o limite de leads
    total_leads = len(sheet.get_all_values()) - 1  # -1 por causa do cabeçalho
    if total_leads >= max_leads:
        raise Exception(f"Limite de leads atingido ({max_leads}). Novos dados não serão salvos.")
    # Adiciona data/hora atual no início dos dados
    from datetime import datetime
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data_to_save = [now] + data
    # Procura a próxima linha vazia
    next_row = len(sheet.get_all_values()) + 1
    sheet.insert_row(data_to_save, next_row)
