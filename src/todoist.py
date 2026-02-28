from zoneinfo import ZoneInfo

from datetime import datetime
import json
import urllib.request
import urllib.parse

base_url = "https://api.todoist.com/api/v1"
tasks_url = f"{base_url}/tasks"


def get_local_today():
    local_tz = ZoneInfo("America/Chicago")
    return datetime.now(local_tz)


def create_todoist_task(
        token: str,
        project_id: str,
        section_id: str,
        email: str,
):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "content": f"Send email to {email}",
        "project_id": project_id,
        "section_id": section_id,
        "due_date": get_local_today().date().isoformat(),
    }
    try:
        req = urllib.request.Request(
            tasks_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req) as res:
            todoist_response = json.loads(res.read().decode())

        return todoist_response.get('id')
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def get_todays_completed_tasks_count(token: str) -> int:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    since = get_local_today().strftime('%Y-%m-%dT06:00:00Z')
    url = f"{tasks_url}/completed?since={since}"
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            return len(items)

    except Exception as e:
        print(f"Error calling v1 completed API: {e}")
        return 0


def get_current_open_tasks_count(token: str) -> int:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query = "query=today"
    url = f"{tasks_url}/filter?{query}"
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(data)
            items = data.get('results', [])
            return len(items)
    except Exception as e:
        print(f"Error calling v1 filter API: {e}")
        return 0
