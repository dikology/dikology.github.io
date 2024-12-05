---
layout: ../../layouts/MarkdownPostLayout.astro
title: Working with Yandex Disk API
description: Trying to use API to get some memories
date: 2024-12-05
image:
  src: https://cdn.midjourney.com/d5205413-1fed-4ef0-bef5-27c5f0f4a6fb/0_0.png
featured: true
draft: true
category: tech
---
## Getting development token
[howto](https://yandex.ru/dev/id/doc/ru/tokens/debug-token)

## Experiments
[chatgpt](https://chatgpt.com/c/6751f38a-bb44-800c-b3c0-751d6f7518b0)

Here's a complete Python script using the **Yandex Disk API** that lists files created in a specific month or week number. It assumes the OAuth token is stored in a `.env` file, and it uses **Poetry** for dependency management.

### Step 1: Set up Poetry environment
1. **Initialize Poetry** (if not done yet):
   ```bash
   poetry init
   ```

2. **Add dependencies**:
   ```bash
   poetry add requests python-dotenv
   ```

### Step 2: Create `.env` file
Create a `.env` file in your project directory with the following content:
```ini
YANDEX_DISK_OAUTH_TOKEN=your_oauth_token_here
```

### Step 3: Python Script (`list_yandex_files.py`)
```python
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
```

### Explanation:
1. **OAuth Token**: Loaded from `.env` using `dotenv`.
2. **Yandex Disk API Request**: The script lists files in the root (`/`) directory by default.
3. **Filtering**:
   - Filters by month (`datetime.month`) or week number (`isocalendar()[1]`).
   
### Usage:
Run the script in your Poetry environment:
```bash
poetry run python list_yandex_files.py
```

### Customization:
1. **Change `path`** in `params` to target a specific directory.
2. Adjust `month` and `week` to filter as needed.
