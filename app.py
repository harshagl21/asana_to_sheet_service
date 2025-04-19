import os
from flask import Flask, request, jsonify
from asana_util import get_asana_tasks
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

@app.route("/fetch-asana", methods=["GET"])
def fetch_and_write_sheet1():
    # Read required credentials from environment
    token = os.environ["ASANA_TOKEN"]
    workspace_id = os.environ["ASANA_WORKSPACE"]
    user_id = os.environ["ASANA_USER_ID"]
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    # Fetch filtered tasks from Asana
    tasks = get_asana_tasks(token, workspace_id, user_id, from_date, to_date)

    # Authenticate with Google Sheets
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("/etc/secrets/service_account.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1-erzJK5KStrylPxfgOO20VUNa_zIs75HqELHGfT_6OA").worksheet("Sheet1")

    # Write each task as a new row
    written = 0
    for task in tasks:
        try:
            sheet.append_row([
                task.get("name", ""),
                task.get("notes", ""),
                task.get("created_at", ""),
                task.get("completed_at", ""),
                "✅" if task.get("completed") else ""
            ])
            written += 1
        except Exception as e:
            print(f"Sheet write error: {e}")

    return jsonify({"status": "written_to_sheet1", "tasks_written": written})

# Local dev fallback
if __name__ == "__main__":
    app.run(debug=True)
