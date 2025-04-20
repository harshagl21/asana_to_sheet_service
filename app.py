import os
from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --- Google Sheets Setup ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]
SERVICE_ACCOUNT_PATH = "/etc/secrets/service_account.json"
SPREADSHEET_KEY = "1-erzJK5KStrylPxfgOO20VUNa_zIs75HqELHGfT_6OA"

def get_sheet():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_KEY).worksheet("Sheet1")
    return sheet

# --- Fetch specific row ---
@app.route("/sheet", methods=["GET"])
def get_row():
    try:
        row_number = int(request.args.get("row", 1))
        sheet = get_sheet()
        range_str = f"A{row_number}:Z{row_number}"
        row_data = sheet.get(range_str)

        if not row_data or not any(row_data[0]):
            return jsonify([])

        return jsonify(row_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Fetch all rows (excluding header) ---
@app.route("/fetch-all", methods=["GET"])
def fetch_all_rows():
    try:
        sheet = get_sheet()
        all_data = sheet.get_all_values()

        if not all_data or len(all_data) <= 1:
            return jsonify([])

        return jsonify(all_data[1:])  # Skip header row
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
