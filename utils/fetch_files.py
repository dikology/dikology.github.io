import os
import requests
import concurrent.futures
from dotenv import load_dotenv
from datetime import datetime
import argparse  # For parsing command-line arguments
import time
import duckdb

# Load OAuth token from .env file
load_dotenv()
OAUTH_TOKEN = os.getenv("YANDEX_DISK_OAUTH_TOKEN")

# Yandex Disk API Base URL
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources/files"

# DuckDB database file
DB_FILE = "yandex_files.duckdb"

# Initialize DuckDB connection
conn = duckdb.connect(DB_FILE)
conn.execute("""
CREATE TABLE IF NOT EXISTS files (
    name TEXT,
    path TEXT PRIMARY KEY,
    created TIMESTAMP,
    modified TIMESTAMP
)
""")

def fetch_batch(offset, batch_size):
    """Fetch a batch of files from Yandex Disk starting from the given offset."""
    headers = {"Authorization": f"OAuth {OAUTH_TOKEN}"}
    params = {
        "limit": batch_size,
        "offset": offset,
        "fields": "items.name,items.path,items.created,items.modified"
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

def sync_files_to_db(files):
    """Sync the fetched files to the database."""
    conn = duckdb.connect(DB_FILE)

    for file in files:
        try:
            conn.execute("""
                DELETE FROM files WHERE path = ?
            """, (file["path"],))

            conn.execute("""
                INSERT INTO files (path, name, created, modified)
                VALUES (?, ?, ?, ?)
            """, (file["path"], file["name"], file["created"], file["modified"]))
        except Exception as e:
            print(f"[EXCEPTION] Failed to sync file {file['path']}: {e}")
    
    conn.close()

def get_files_created_in_period(month=None, week=None):
    """Get files created or modified in a given month or week."""
    batch_size = 100
    total_files_to_check = 60000
    offsets = [i for i in range(0, total_files_to_check, batch_size)]
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
                    break
                
                for file in files:
                    created_time = datetime.fromisoformat(file["created"].replace("Z", "+00:00"))
                    modified_time = datetime.fromisoformat(file["modified"].replace("Z", "+00:00"))
                    
                    if month and (created_time.month == month or modified_time.month == month):
                        filtered_files.append(file)
                    elif week and (created_time.isocalendar()[1] == week or modified_time.isocalendar()[1] == week):
                        filtered_files.append(file)
                
                if len(filtered_files) > 0:
                    sync_files_to_db(filtered_files)
                    filtered_files.clear()  # Clear the list to avoid duplicate syncs
                    
            except Exception as e:
                print(f"[EXCEPTION] Error processing batch at offset {offset}: {str(e)}")
            
            elapsed_time = time.time() - start_time
            time_per_batch = elapsed_time / i
            remaining_batches = total_batches - i
            estimated_time_left = time_per_batch * remaining_batches
            
            print(f"[PROGRESS] Batch {i}/{total_batches} completed. Elapsed time: {elapsed_time:.2f}s. Estimated time left: {estimated_time_left:.2f}s.")
        
        print("[INFO] Completed all batches.")
    return filtered_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch files from Yandex Disk created or modified in a specific period.")
    parser.add_argument("--month", type=int, help="Filter files created or modified in the given month (1-12).")
    parser.add_argument("--week", type=int, help="Filter files created or modified in the given ISO week (1-53).")
    
    args = parser.parse_args()
    
    month = args.month
    week = args.week

    if not month and not week:
        print("[ERROR] You must specify either --month or --week.")
        exit(1)

    # Fetch files
    files = get_files_created_in_period(month=month, week=week)
    
