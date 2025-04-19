import requests
from datetime import datetime

def get_asana_tasks(token, workspace_id, user_id, from_date, to_date):
    url = "https://app.asana.com/api/1.0/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "assignee": user_id,
        "workspace": workspace_id,
        "completed_since": from_date,
        "opt_fields": "name,notes,created_at,completed_at,completed"
    }

    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    tasks = res.json()["data"]

    from_date_dt = datetime.fromisoformat(from_date)
    to_date_dt = datetime.fromisoformat(to_date)

    def in_range(ts):
        if ts:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return from_date_dt <= dt <= to_date_dt
        return False

    filtered = [
        t for t in tasks
        if in_range(t.get("created_at")) or in_range(t.get("completed_at"))
    ]

    return filtered
