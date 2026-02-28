import json

from config import get_config
import todoist


def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"context: {context}")

    config = get_config()

    method = event.get('httpMethod')
    if method == "GET":
        completed = todoist.get_todays_completed_tasks_count(config['TODOIST_API_TOKEN'])
        today = todoist.get_current_open_tasks_count(config['TODOIST_API_TOKEN'])
        response_body = {
            "completed": completed,
            "open": today
        }
    elif method == "POST":
        body = json.loads(event.get('body', '{}'))
        target_email = body.get('email', 'Unknown Email')

        task_id = todoist.create_todoist_task(
            config['TODOIST_API_TOKEN'],
            config['PROFESSIONAL_PROJECT_ID'],
            config['GROWTH_SECTION_ID'],
            target_email
        )
        response_body = {
            "id": task_id
        }
    else:
        response_body = {
            "message": "unknown request type"
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "https://www.austinluing.com",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(response_body)
    }