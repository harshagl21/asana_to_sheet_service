
import os
from flask import Flask, request, jsonify
from asana_util import get_asana_tasks
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

@app.route("/fetch-asana", methods=["GET"])
def fetch_and_write_asana():
    token = os.environ["ASANA_TOKEN"]
    workspace_id = request.args.get("workspace_id")
    user_id = request.args.get("user_id")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    tasks = get_asana_tasks(token, workspace_id, user_id, from_date, to_date)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("/etc/secrets/service_account.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1-erzJK5KStrylPxfgOO20VUNa_zIs75HqELHGfT_6OA").worksheet("Sheet1")

    for task in tasks:
        sheet.append_row([
            task["name"],
            task.get("created_at"),
            task.get("completed_at"),
            "✅" if task["completed"] else ""
        ])

    return jsonify({"status": "done", "tasks_written": len(tasks)})

if __name__ == "__main__":
    app.run(debug=True)
