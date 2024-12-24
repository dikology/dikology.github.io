import json
from datetime import datetime
import os

def generate_calendar_data(files):
    calendar_data = []
    for file in files:
        created_date = datetime.fromisoformat(file['created'].replace("Z", "+00:00"))
        calendar_data.append({
            'name': file['name'],
            'path': file['path'],
            'date': created_date.strftime('%Y-%m-%d')
        })
    
    with open('src/public/calendar_data.json', 'w') as f:
        json.dump(calendar_data, f, indent=4)

if __name__ == "__main__":
    # Ensure files.json exists after running fetch_files.py
    if not os.path.exists('files.json'):
        print("[ERROR] 'files.json' not found. Run fetch_files.py first.")
    else:
        with open('files.json', 'r') as f:
            files = json.load(f)
        generate_calendar_data(files)
        print("[INFO] Calendar data generated.")
