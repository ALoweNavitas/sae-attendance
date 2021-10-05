**<h1>Updating the Attendance Dashboard</h1>**

**<h2>Purpose</h2>**

This is a small script that takes the Attendance Statement csv file from Navigate, ingesting the data and performing various lookups to add additional elements, such as campus and relevant teaching week. The data is fed into an SQLite database, and also piped to Google Sheets which in turn is piped to a Data Studio report.

**<h2>Requirements and how to install them</h2>**

**<h3>Installing Python</h3>**

Install Python 3.XX following the instructions [found here](https://www.python.org/downloads/).

<h3>Python dependancies</h3>

Open Command Prompt and cd to the directory of the script, then use ```pip install -r requirements.txt``` to install the required dependenancies and versions if you do not have them installed already.

<h3>JSON Keys for Google API Client</h3>

You should be the owner of the ```moodleanalytics``` service account, which is the account setup by Adam Lowe to act as a bridge for pushing data from Python to a Google Sheet. To check you have ownership [click here](https://console.cloud.google.com/iam-admin/serviceaccounts/details/101202451532644359925/keys?project=moodleanalytics) and you should be able view the moodle analytics service account. Click the ```add key``` button and select ```Create New Key``` and then select ```JSON.```

:warning: **Service account keys could pose a security risk if compromised.** Keep this file safe and secure.

```
#  Google sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'C:\path_to_JSON_file'
credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
```

**<h2>Updating The Module Registrations Google Sheet</h2>**

[This sheet](https://docs.google.com/spreadsheets/d/1vg5DwP1ToRY9Rkp-6837x5wBFOu1Mh_-7XOANyTP0KA/edit) feeds into many of the process documents currently in use at SAE, such as the Gradebook Tracker. We use this to lookup various details of students, including what programme and campus they belong to. 

To update the Module Registrations sheet, search for all students on Navigate in the current term. Then go to ```Action > Report > Module Registrations```. In the ```filters```, select the current study period and under ```Status``` check all available statuses. RPL should be set to Yes.

Open the downloaded csv and delete all rows until you get to the headers row (usually around row 160). Select all of the data, apart from the header, and replace the trimester data in the Module Registrations Google Sheet (make sure you delete any current entries first i.e delete of the 21T3 data before you paste it back in). 

This should be done atleast once per week.

**<h2>How to use</h2>**

On Navigate, search for all the students registered in the given trimester. Once you have created the list, go to ```Actions > Report > Attendance > Attendance Statement``` and download the file as a .csv. Keep the file name as ```Attendance Statement.csv```, as the script references this as a filename. Save the file into the same directory as the script.

You can use Visual Studio to run the script manually. Alternatively, you can create a .bat file to launch the script, which can then be synced to a CRON job or GUI tool, like Windows Task Manager. An example of a .bat config can be seen below; 

```
"C:\Users\adam_\Documents\GitHub\Navitas\sae-attendance\venv\Scripts\python.exe" # path to your Python exe 

"C:\Users\adam_\Documents\GitHub\Navitas\sae-attendance\main.py" # path to the main python file
```
There is also an editable ```main.bat``` config file in the dir.

**<h3>Dictionary JSON</h3>**

This is a JSON file containing the gregorian week number, matching it to its corresponding teaching week at SAE. The script will look up the lecture date and return the equivalent teaching week.

**<h3>Databases</h3>**

The script will automatically create various SQLite3 databases to store data.

<b>Module Registrations SQL Database</b>

The ```modreg.py``` function queries the Mod Reg Google Sheet, downloading all of the data to a SQL table. This is then used in the script to do lookups. Refer to the top section for information on how to update this.

<b>Attendance SQL Database</b>

This stores the same information that is being uploaded to the Google Sheet, so you can perform SQL queries on the data or better manage it for other applications, such as PowerBI. 

There are also 2 lookup tables within this database. The first is the new students on the programme for 21T3, and the second is all of the student route students. This is so they can be identified in the data for seperate analysis and monitoring as key risk groups.

**<h2>Support</h2>**

If you require assistance with this script, please reach out via Teams or email. 

Email: [adam.lowe@navitas.com](mailto:adam.lowe@navitas.com)

Zoom: [http://navitas.zoom.us/my/adamlowenavitas](http://navitas.zoom.us/my/adamlowenavitas)

This script will be hosted on my GitHub account.