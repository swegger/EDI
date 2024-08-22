## README
EDI repository contains basic code for analysis of EDI data for the department of Neurobiology at Duke.

# speakerAnalysis
Jupyter notebook for the analysis of speaker data from a public google sheets document. Uses gspread to collect import data from the desired google sheet loads data into a pandas DataFrame.

Requires: gspread, pandas

Notes on gspread: requires an api key from google to access sheets that are open to the public (e.g. anyone with the link can access). To obtain a key:

1) Enable API Access for a Project if you haven’t done it yet.

    a) Head to Google Developers Console and create a new project (or select the one you already have).

    b) In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.

    c) In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it. 

3) Go to “APIs & Services > Credentials” and choose “Create credentials > API key”

4) A pop-up should display your newly created key.

5) Copy the key.

6) Enter the key into a local file named .keys
