import json
import boto3
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request  # Import Request
from google.oauth2 import service_account

from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def extract_data_from_dynamodb(table_name):
    # Initialiser le client DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Récupérer toutes les données de la table DynamoDB
    response = table.scan()
    data = response['Items']
    
    # Ajouter une logique pour gérer la pagination si votre table est grande
    return data

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

def lambda_handler(event, context):
    print("Function")
    
    dynamodb_table_name = 'test'
    spreadsheet_id = '1lEkfFbui3MsUf1vrBCqjtfcob7_SwuC9Loyt7afZU-Y'
    range_name = 'extract-dynamo'  # Nom de l'onglet dans Google Sheets

    # Extraire les données de DynamoDB
    dynamodb_data = extract_data_from_dynamodb(dynamodb_table_name)

    # Déterminer les noms de colonnes (supposant que tous les éléments ont les mêmes clés)
    if dynamodb_data:
        column_names = list(dynamodb_data[0].keys())  # Prend les clés du premier élément comme noms de colonnes
    else:
        column_names = []  # Ou spécifiez les noms de colonnes explicitement si préférable

    values = [column_names]

    # Then, for each item in your DynamoDB data
    for item in dynamodb_data:
        row_values = []  # Prepare a list for the current row's values
        for col in column_names:
            # Apply specific processing for each data type
            if col in ['date', 'date_first_contact']:
                date_value = item.get(col, '')  # Assume date_value is in 'YYYY-MM-DD' format
                if date_value:
                    try:
                        # Attempt to parse the date string to a datetime object
                        formatted_date = datetime.strptime(date_value, '%Y-%m-%d')
                        # Convert to a full ISO 8601 format string with a dummy time part
                        iso_date = formatted_date.strftime('%Y-%m-%dT00:00:00Z')
                        row_values.append(iso_date)
                    except ValueError:
                        # In case of a formatting error, keep the original value
                        row_values.append(date_value)
            elif col == 'id':
                # For IDs or other numbers, ensure they are treated as integers
                id_value = int(item.get(col, 0))  # Convert to integer, with a default value if necessary
                row_values.append(id_value)
            else:
                # For all other data types, insert them as is
                row_values.append(item.get(col, ''))
        # After processing all columns for the current item, add the row to the values
        values.append(row_values)

    # Ajouter les noms de colonnes et les données à Google Sheets
    append_data_to_google_sheets(spreadsheet_id, range_name, values)
    
    return {
        'statusCode': 200,
        'body': 'Données transférées avec succès à Google Sheets'
    }

print("It's working!")