import json
import boto3
import csv
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request  # Import Request
from google.oauth2 import service_account

import re
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def append_data_to_google_sheets(spreadsheet_id, range_name, values):
    # Créer les credentials et le client pour l'API Google Sheets
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    # Appeler l'API Google Sheets pour ajouter les données
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    return result

def read_csv_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    # Décodez le contenu du fichier
    content = obj['Body'].read().decode('utf-8')
    lines = content.split('\n')
    reader = csv.reader(lines)
    data = list(reader)
    return data

date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

def clear_google_sheet(spreadsheet_id, range_name):
    """
    Clear a specific range in a Google Sheet.
    
    :param spreadsheet_id: The ID of the spreadsheet.
    :param range_name: The range to clear, in A1 notation.
    """
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    
    # Call the Sheets API to clear the range
    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_name)
    response = request.execute()
    
    print(f"Range {range_name} cleared successfully.")

def is_date(string):
    return bool(date_pattern.match(string))

def transform_data_for_sheets(csv_data):
    transformed_data = []
    for row in csv_data:
        transformed_row = []
        for item in row:
            try:
                # Attempt to convert the string to a float
                float_value = float(item)
                # If the conversion succeeds but the float value is actually an integer, convert it to int to remove the decimal part
                if float_value.is_integer():
                    transformed_row.append(int(float_value))
                else:
                    transformed_row.append(float_value)
            except ValueError:
                # If conversion to float fails, it might be a date or another string
                if is_date(item):  # Check if the item is a date
                    try:
                        formatted_date = datetime.strptime(item, '%Y-%m-%d')
                        # Convert to a full ISO 8601 format string with a dummy time part
                        iso_date = formatted_date.strftime('%Y-%m-%dT12:00:00Z')
                        transformed_row.append(iso_date)
                    except ValueError:
                        transformed_row.append(item)  # Keep the original string if date conversion also fails
                else:
                    # For items that are neither float nor date, keep them as is
                    transformed_row.append(item)
        transformed_data.append(transformed_row)
    return transformed_data

def upload_ESI():
    bucket_name = 'talyco-data'
    spreadsheet_id = '1JCaWCKYW_l4jsvdeed6MJJJwgCAhA5gQjlSo3Xmj9Pw'
    
    # List of tuples, each containing the file_key and the corresponding range_name
    files_and_ranges = [
        ('gema/data-processed/ESI-monitoring.csv', 'monitoring'),
        ('gema/data-processed/ESI-campus-sheet.csv', 'campus-sheet'),
        ('gema/data-processed/ESI-source-sheet.csv', 'source-sheet'),
        ('gema/data-processed/ESI-mastersheet.csv', 'mastersheet'),
        # Add more tuples here as needed
    ]
    
    for file_key, range_name in files_and_ranges:
        print(f"Clearing range {range_name}...")
        clear_google_sheet(spreadsheet_id, range_name)

        # Read and transform CSV data from S3
        print(f"Updating range {range_name} with data from {file_key}...")
        csv_data = read_csv_from_s3(bucket_name, file_key)
        csv_data = transform_data_for_sheets(csv_data)
        
        # Append data to Google Sheets
        result = append_data_to_google_sheets(spreadsheet_id, range_name, csv_data)
        print(f"Data transferred successfully to {range_name}: {result}")

def upload_IA():
    bucket_name = 'talyco-data'
    spreadsheet_id = '1NRFK7xyHYvvczaZli-xDm0FyVsqnd_m0AjgxaIcPz0Q'
    
    # List of tuples, each containing the file_key and the corresponding range_name
    files_and_ranges = [
        ('gema/data-processed/IA-monitoring.csv', 'monitoring'),
        ('gema/data-processed/IA-campus-sheet.csv', 'campus-sheet'),
        ('gema/data-processed/IA-source-sheet.csv', 'source-sheet'),
        ('gema/data-processed/IA-mastersheet.csv', 'mastersheet'),
        # Add more tuples here as needed
    ]
    
    for file_key, range_name in files_and_ranges:
        print(f"Clearing range {range_name}...")
        clear_google_sheet(spreadsheet_id, range_name)

        # Read and transform CSV data from S3
        print(f"Updating range {range_name} with data from {file_key}...")
        csv_data = read_csv_from_s3(bucket_name, file_key)
        csv_data = transform_data_for_sheets(csv_data)
        
        # Append data to Google Sheets
        result = append_data_to_google_sheets(spreadsheet_id, range_name, csv_data)
        print(f"Data transferred successfully to {range_name}: {result}")

def upload_cyber():
    bucket_name = 'talyco-data'
    spreadsheet_id = '1l3CszsnsJf7gV_Qbrekv5uyfsv7URLhqbtjNuYzS3nk'
    
    # List of tuples, each containing the file_key and the corresponding range_name
    files_and_ranges = [
        ('gema/data-processed/cyber-monitoring.csv', 'monitoring'),
        ('gema/data-processed/cyber-campus-sheet.csv', 'campus-sheet'),
        ('gema/data-processed/cyber-source-sheet.csv', 'source-sheet'),
        ('gema/data-processed/cyber-mastersheet.csv', 'mastersheet'),
        # Add more tuples here as needed
    ]
    
    for file_key, range_name in files_and_ranges:
        print(f"Clearing range {range_name}...")
        clear_google_sheet(spreadsheet_id, range_name)

        # Read and transform CSV data from S3
        print(f"Updating range {range_name} with data from {file_key}...")
        csv_data = read_csv_from_s3(bucket_name, file_key)
        csv_data = transform_data_for_sheets(csv_data)
        
        # Append data to Google Sheets
        result = append_data_to_google_sheets(spreadsheet_id, range_name, csv_data)
        print(f"Data transferred successfully to {range_name}: {result}")

def lambda_handler(event, context):
    # Exemple de noms de bucket et clé S3
    upload_ESI()
    upload_IA()
    upload_cyber()

    return {
        'statusCode': 200,
        'body': 'Data transferred successfully to Google Sheets'
    }

print("It's working!")