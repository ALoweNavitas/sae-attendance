from sqlite3.dbapi2 import Connection
import pandas as pd
import os
import json
import modreg
from sqlite3 import connect
from googleapiclient.discovery import build
from google.oauth2 import service_account

def main():
    pass

if __name__ == '__main__':
    main()

os.chdir(os.getcwd())
dir = os.getcwd()

# Modreg SQLite3 DB. Downloads the Google Sheet Mod Reg.
modreg.updateModReg.update()

# Variables
trimester = '21T3'
modRegDb = os.environ.get('modRegDB')
cnx = connect(modRegDb)

#  Google sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json' # this is a dangerous file. Do not share publically.
credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
attendanceSheet = '1kglRtY6yucrg6yL0cpq5mmbmyH6u2norcuZyo-uLAtQ' # Google Sheet ID, change each term.


# Student lookup using the ModReg in SQL
df = pd.read_sql('SELECT "StudentCode", "ModuleStatus", "CampusName" FROM modReg WHERE "StudyPeriod/RPL" = "%s" AND "ModuleStatus" = "Confirmed"' % (trimester), cnx)
df.drop_duplicates(['StudentCode'], inplace=True)
studentLookup = dict(zip(df['StudentCode'], df['CampusName']))

# New student lookup using attendance DB in SQL
df = pd.read_sql('SELECT * FROM newStudents', cnx)
newStudentLookup = dict(zip(df['StudentCode'], df['type']))

# Student route lookup using attendance DB in SQL
df = pd.read_sql('SELECT * FROM studentRoute', cnx)
studentRouteLookup = dict(zip(df['StudentCode'], df['type']))

# JSON file to lookup the teaching weeks
with open('dictionary.json') as json_file:
    data = json.load(json_file)

dates = data['dates'] # Converts the date of the lecture to the teaching week.

# Create the dataframe
df = pd.read_csv('Attendance Statement.csv')
df = df[df['studyPeriodName'].isin(['  Trimester 3, 2021 (Sept)'])] # Needs to be changed for each iteration of the script.
df.rename(columns={'Textbox178' : 'exportDate', 'Textbox137' : 'studentName', 'Textbox138': 'StudentCode', 'date' : 'lectureDate'}, inplace=True)
df.drop(['address1'], axis=1, inplace=True)
df['lectureDate'] = pd.to_datetime(df['lectureDate'], dayfirst=True)
df['teachingWeek'] = df['lectureDate'].dt.strftime('%V').map(dates)
df['campus'] = df['StudentCode'].map(studentLookup)
df['newStudent'] = df['StudentCode'].map(newStudentLookup)
df['studentRoute'] = df['StudentCode'].map(studentRouteLookup)
df['lectureDate'] = df['lectureDate'].astype(str) # Google API wont accept datetime due to JSON parsing.
df.fillna('', inplace=True) # Google API wont accept NaN values due to JSON parsing.
df.to_sql(name=trimester, con=cnx, if_exists='replace') # Creates a small SQLite3 DB for managing.

# Update Google Sheets
data = df.copy()
data.fillna('', inplace=True)
data = data.values.tolist()
sheet.values().update(spreadsheetId=attendanceSheet, range='data!A2', valueInputOption="USER_ENTERED", body={"values":data}).execute()
print('Attendance has been updated.')

