---
layout: ../../layouts/MarkdownPostLayout.astro
title: Working with Yandex Disk API
description: Trying to use API to get some memories
date: 2024-12-05
image:
  src: https://cdn.midjourney.com/0baedd4a-2a01-45b1-8ed2-cc8e68a9830e/0_0.png
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

Here's a combined, optimized version of the script that:  
1️⃣ **Requests only necessary fields** (`name`, `path`, `created`, `modified`).  
2️⃣ **Uses parallel requests** with `concurrent.futures`.  
3️⃣ **Stops early** when the number of `filtered_files` exceeds 100.  

---

### **Updated Script**
```python
import os
import requests
import concurrent.futures
from dotenv import load_dotenv
from datetime import datetime

# Load OAuth token from .env file
load_dotenv()
OAUTH_TOKEN = os.getenv("YANDEX_DISK_OAUTH_TOKEN")

# Yandex Disk API Base URL
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources/files"

def fetch_batch(offset):
    """Fetch a batch of files from Yandex Disk starting from the given offset."""
    headers = {"Authorization": f"OAuth {OAUTH_TOKEN}"}
    params = {
        "limit": 100,  # Batch size
        "offset": offset,
        "fields": "items.name,items.path,items.created,items.modified"  # Only request essential fields
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error at offset {offset}: {response.json().get('message')}")
        return []

def get_files_created_in_period(month=None, week=None):
    """Get files created or modified in a given month or week."""
    batch_size = 100  # Batch size for requests
    max_files = 100  # Stop once we collect this many filtered files
    offsets = [i for i in range(0, 10000, batch_size)]  # Request offsets for the first 10,000 files

    filtered_files = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_offset = {executor.submit(fetch_batch, offset): offset for offset in offsets}
        
        for future in concurrent.futures.as_completed(future_to_offset):
            files = future.result()
            for file in files:
                created_time = datetime.fromisoformat(file["created"].replace("Z", "+00:00"))
                
                # Check if the file matches the filter (month or week)
                if month and created_time.month == month:
                    filtered_files.append(file)
                elif week and created_time.isocalendar()[1] == week:
                    filtered_files.append(file)
                
                # Stop early if we have enough files
                if len(filtered_files) >= max_files:
                    print(f"Stopping early: Collected {len(filtered_files)} files.")
                    return filtered_files

    return filtered_files

if __name__ == "__main__":
    # Example: Get files created or modified in December (month=12)
    month = 12  # December
    week = None  # No week filtering, only month

    files = get_files_created_in_period(month=month, week=week)

    print(f"Total files found: {len(files)}")
    for file in files[:5]:  # Print only the first 5 files for brevity
        print(f"Name: {file['name']}, Path: {file['path']}, Created: {file['created']}")
```

---

### 🔍 **Explanation of Key Changes**
1. **Request Only Essential Fields**
   ```python
   params = {
       "limit": 100,  
       "offset": offset,
       "fields": "items.name,items.path,items.created,items.modified"
   }
   ```
   This limits the amount of metadata we receive for each file to only the essentials:  
   - **name**: To display file names.  
   - **path**: In case you need to download or access the file later.  
   - **created**: Used to filter files by the month or week.  
   - **modified**: This could be used later if you'd like to filter by modified date.  

   This avoids unnecessary data like file size, mime type, or other unneeded properties.

---

2. **Parallel Requests**
   ```python
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
       future_to_offset = {executor.submit(fetch_batch, offset): offset for offset in offsets}
       
       for future in concurrent.futures.as_completed(future_to_offset):
           files = future.result()
   ```
   Here, we use Python's `concurrent.futures` to create multiple threads, each requesting a batch of files.  
   - **Batch size** is 100 files per request.  
   - **Max workers** is 5 threads, so up to 5 requests are running at the same time.  
   - Requests are processed in parallel, reducing the total response time.  

---

3. **Stop Early Once 100 Filtered Files Are Collected**
   ```python
   if len(filtered_files) >= max_files:
       print(f"Stopping early: Collected {len(filtered_files)} files.")
       return filtered_files
   ```
   After collecting 100 matching files, the script stops, even if other threads are still running.  
   This prevents unnecessary requests and speeds up execution.  

---

### ⚙️ **Customizations**
- **Max File Limit**: Change `max_files = 100` to collect a different number of files before stopping.  
- **Batch Size**: Adjust `batch_size` from 100 to 200 or 50 if you want larger/smaller requests.  
- **Max Workers**: Adjust `max_workers=5` to control how many requests run at the same time.  

---

### 🔥 **Performance Benefits**
- **Reduced Metadata**: Smaller response sizes (fewer fields).  
- **Parallel Requests**: Speeds up file collection with multiple concurrent threads.  
- **Early Exit**: Stops as soon as 100 files are found, avoiding unnecessary requests.  

This version balances speed and efficiency, especially when working with large file lists on Yandex Disk. Let me know if you'd like further optimizations or explanations! 🚀