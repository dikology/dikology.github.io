import pandas as pd
import json

def generate_chart_data(files):
    df = pd.DataFrame(files)
    df['created_date'] = pd.to_datetime(df['created'])
    df['month'] = df['created_date'].dt.month

    chart_data = df['month'].value_counts().sort_index().to_dict()
    with open('src/public/chart_data.json', 'w') as f:
        json.dump(chart_data, f, indent=4)

if __name__ == "__main__":
    # Ensure files.json exists after running fetch_files.py
    if not os.path.exists('files.json'):
        print("[ERROR] 'files.json' not found. Run fetch_files.py first.")
    else:
        with open('files.json', 'r') as f:
            files = json.load(f)
        generate_chart_data(files)
        print("[INFO] Chart data generated.")
