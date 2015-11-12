import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import os.path
import uuid

#The spreadsheet should be shared with the email address from the json file
#see the docs here: http://gspread.readthedocs.org/en/latest/oauth2.html
class GoogleSpreadsheet(object):
    def __init__(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        jsonKeyPath = os.path.join(currentDir, 'google/WebTables-ec825f0c327b.json')
        jsonKey = json.load(open(jsonKeyPath))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(jsonKey['client_email'], jsonKey['private_key'].encode(), scope)
        gc = gspread.authorize(credentials)
        self.wks = gc.open_by_key("1oHpZuOg8LExEOMyTMjKzllbR5gCHZ7qHzQjwUhVc44M")

    def createOrGetNamedWorksheet(self, name):
        try:
            return self.wks.worksheet(name)
        except gspread.WorksheetNotFound:
            rows = 1
            cols = 4
            worksheet = self.wks.add_worksheet(name, rows, cols)
            worksheet.update_acell('A1', 'TableId')
            worksheet.update_acell('B1', 'SubjectColumnIndex')
            worksheet.update_acell('C1', 'NoSubjectColumn')
            worksheet.update_acell('D1', 'TableType')
            return worksheet

    def getIdentifiedTableIds(self):
        worksheets = self.wks.worksheets()
        identifiedIds = []
        for worksheet in worksheets:
            identifiedIds.extend(worksheet.col_values(1)[1:])
        return identifiedIds

if __name__ == "__main__":
    googleSpreadsheet = GoogleSpreadsheet()
    googleSpreadsheet.getIdentifiedTableIds()
    #ivanWorksheet = googleSpreadsheet.createOrGetNamedWorksheet("ivan")
    #ivanWorksheet.append_row(["fdsafdaf", "foidsjfo"])
