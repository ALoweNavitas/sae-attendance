import pandas as pd
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import sqlite3

def main():
    pass

if __name__ == '__main__':
    main()

class updateModReg:

    def __init__(self):
        self.self = self

    def update():
        # Create/ Connect to the SQLite database
        cnx = sqlite3.connect('modRegDB.db')

        #  Google sheets setup
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'keys.json'
        credentials = None
        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # This downloads the Module Registration database as a dataframe.
        ModReg = '1vg5DwP1ToRY9Rkp-6837x5wBFOu1Mh_-7XOANyTP0KA'
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result =  sheet.values().get(spreadsheetId=ModReg, range='ModReg_All!A:AB').execute()
        values = result.get('values',[])
        df = pd.DataFrame(data=values, index=None)
        df.columns = df.iloc[0] # Sets the column headers to the top row
        df.columns = df.columns.str.replace(' ','') # Removes spaces to make it easier for SQLite
        df = df[1:] # Sets the column headers to the top row
        df.drop([""], axis=1, inplace=True) # Gets rid of the annoying blank column

        # Write to SQLite
        df.to_sql('modReg', con=cnx, if_exists='replace')
        print('Module registrations have been updated.')