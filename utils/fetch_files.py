import os
import requests
import concurrent.futures
from dotenv import load_dotenv
from datetime import datetime
import time  # For tracking time progress

# Load OAuth token from .env file
load_dotenv()
OAUTH_TOKEN = os.getenv("YANDEX_DISK_OAUTH_TOKEN")

# Yandex Disk API Base URL
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources/files"

def fetch_batch(offset, batch_size):
    """Fetch a batch of files from Yandex Disk starting from the given offset."""
    headers = {"Authorization": f"OAuth {OAUTH_TOKEN}"}
    params = {
        "limit": batch_size,  # Batch size
        "offset": offset,
        "fields": "items.name,items.path,items.created,items.modified"  # Only request essential fields
    }
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            files = response.json().get("items", [])
            print(f"[INFO] Batch at offset {offset}: Retrieved {len(files)} files.")
            return files
        else:
            print(f"[ERROR] Failed to fetch batch at offset {offset}: {response.status_code} - {response.json().get('message')}")
            return []
    except Exception as e:
        print(f"[EXCEPTION] Error at offset {offset}: {str(e)}")
        return []

def get_files_created_in_period(month=None, week=None):
    """Get files created or modified in a given month or week."""
    batch_size = 100  # Batch size for requests
    max_files = 100  # Stop once we collect this many filtered files
    total_files_to_check = 100000  # Maximum files to process (change if needed)
    offsets = [i for i in range(0, total_files_to_check, batch_size)]  # Request offsets

    filtered_files = []
    total_batches = len(offsets)
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_offset = {executor.submit(fetch_batch, offset, batch_size): offset for offset in offsets}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_offset), start=1):
            offset = future_to_offset[future]
            
            try:
                files = future.result()

                if len(files) == 0:
                    print(f"[INFO] No files retrieved at offset {offset}. Stopping early as there may be no more files.")
                    break  # Stop if a batch returns 0 files
                
                for file in files:
                    created_time = datetime.fromisoformat(file["created"].replace("Z", "+00:00"))
                    modified_time = datetime.fromisoformat(file["modified"].replace("Z", "+00:00"))
                    
                    # Check if the file matches the filter (month or week)
                    if month and (created_time.month == month or modified_time.month == month):
                        filtered_files.append(file)
                    elif week and (created_time.isocalendar()[1] == week or modified_time.isocalendar()[1] == week):
                        filtered_files.append(file)
                    
                    # Stop early if we have enough files
                    if len(filtered_files) >= max_files:
                        print(f"[INFO] Stopping early: Collected {len(filtered_files)} files.")
                        return filtered_files
            except Exception as e:
                print(f"[EXCEPTION] Error processing batch at offset {offset}: {str(e)}")
            
            # Progress update
            elapsed_time = time.time() - start_time
            time_per_batch = elapsed_time / i
            remaining_batches = total_batches - i
            estimated_time_left = time_per_batch * remaining_batches
            
            print(f"[PROGRESS] Batch {i}/{total_batches} completed. Elapsed time: {elapsed_time:.2f}s. Estimated time left: {estimated_time_left:.2f}s.")
            print(f"[INFO] Files filtered so far: {len(filtered_files)} / {max_files} target files.")
        
        print("[INFO] Completed all batches.")
    return filtered_files

if __name__ == "__main__":
    # Example: Get files created or modified in December (month=12)
    month = None  # Month number
    week = 50  #  week filtering

    files = get_files_created_in_period(month=month, week=week)

    print(f"Total files found: {len(files)}")
    for file in files:  # Print only the first 5 files for brevity
        print(f"Name: {file['name']}, Path: {file['path']}, Created: {file['created']}")
