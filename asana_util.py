
import requests
from datetime import datetime

def get_asana_tasks(token, workspace_id, user_id, from_date, to_date):
    url = "https://app.asana.com/api/1.0/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "assignee": user_id,
        "workspace": workspace_id,
        "completed_since": from_date,
        "opt_fields": "name,created_at,completed_at,completed"
    }

    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    tasks = res.json()["data"]

    filtered = [
        t for t in tasks
        if datetime.fromisoformat(t["created_at"].replace("Z", "+00:00")) < datetime.fromisoformat(to_date)
    ]

    return filtered
