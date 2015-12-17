import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('google-key-example.json'))
#The spreadsheet should be shared with the email address from the json file
#see the docs here: http://gspread.readthedocs.org/en/latest/oauth2.html
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
wks = gc.open("Subject Column Identification").sheet1

wks.update_acell('B10', "it's down there somewhere, let me take another look.")

# Fetch a cell range
cell_list = wks.range('A1:B7')
