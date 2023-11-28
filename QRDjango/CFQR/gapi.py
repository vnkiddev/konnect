import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1mJTg-8OAhvW5a3TojddTZ-ibkySuanfOOSvpu7yOa_s"
def build_service():
    try:
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        service = build("sheets", "v4", credentials=creds)
        print("Service ready")
        return service
    except Exception as e:
        print(e)
        return None
service = build_service()
def get_row(sheet_name,row_num,first_row=True):
    sheet = service.spreadsheets()
    range = sheet_name + "!"+str(row_num)+":"+str(row_num)
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=range)
        .execute()
    )
    values = result.get("values")
    if first_row:
        range = sheet_name + "!1:1"
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=range)
            .execute()
        )
        values = [result.get("values")[0],values[0]]
    return values

def qr_lookup(qr_id):
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Lookup!A2",
        valueInputOption="RAW",
        body = {"values":[[qr_id]]}
    ).execute()
    return get_row("Lookup",2,False)

def qr_detail(qr_id):
    index = qr_lookup(qr_id)[0]
    print("index:",index)
    if index[2] =="#N/A":
        return [{"key":"QRID","value":"Mã QR với sản phẩm này chưa tồn tại"}]
    else:
        data =  get_row(index[1],index[2])
        result = []
        for i in range(1,len(data[0])):
            result.append({"key":data[0][i],"value":data[1][i]})
        return result

def sheet_names():
    sheet_list = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute().get('sheets')
    result = []
    for asheet in sheet_list:
        result.append(asheet['properties']['title'])
    return result

def sheet_values(sheet_name):
    values = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=sheet_name).execute().get('values')
    standard_len = len(values[0])
    for i in values[1:]:
        if len(i) < standard_len:
            i.extend([""] * (standard_len - len(i)))
    return values

if __name__ == "__main__":
    print(qr_detail("trye"))