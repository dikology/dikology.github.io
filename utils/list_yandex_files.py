import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load OAuth token from .env file
load_dotenv()
OAUTH_TOKEN = os.getenv("YANDEX_DISK_OAUTH_TOKEN")

# Yandex Disk API Base URL
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"

def get_files_created_in_period(path="/", month=None, week=None):
    headers = {"Authorization": f"OAuth {OAUTH_TOKEN}"}
    params = {"path": path}
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.json().get('message')}")
        return []
    
    files = response.json().get("_embedded", {}).get("items", [])
    filtered_files = []

    for file in files:
        created_time = datetime.fromisoformat(file["created"].replace("Z", "+00:00"))

        if month and created_time.month == month:
            filtered_files.append(file)
        elif week and created_time.isocalendar()[1] == week:
            filtered_files.append(file)

    return filtered_files

if __name__ == "__main__":
    # Example: Get files from a specific month or week
    month = 12  # December
    week = None  # No filtering by week

    files = get_files_created_in_period(month=month, week=week)

    for file in files:
        print(f"Name: {file['name']}, Created: {file['created']}")