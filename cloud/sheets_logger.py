import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials/creds.json", scope)
client = gspread.authorize(creds)

# Sheet name must already exist in your Drive
SHEET_NAME = "Face_Recognition_Log"
sheet = client.open(SHEET_NAME).sheet1

def log_to_google_sheets(name, confidence, image_url):
    """
    Logs recognition data to Google Sheets with a direct image link.
    """
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_formula = f'=IMAGE("{image_url}")' if image_url else 'N/A'
        sheet.append_row([now, name, round(confidence, 2), image_formula])
        print(f"[LOG] Logged {name} at {now}")
    except Exception as e:
        print(f"[ERROR] Logging to Sheets failed: {e}")
