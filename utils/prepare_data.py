import duckdb
import json
from datetime import datetime

# Connect to the DuckDB file
conn = duckdb.connect('yandex_files.duckdb')

# Query to get results (modify the query as needed)
query = """
SELECT EXTRACT(YEAR FROM COALESCE(created, modified)) AS year, 
       created, 
       modified, 
       readable_name, 
       description, 
       relevance
FROM files
"""

# Execute the query
results = conn.execute(query).fetchall()

# Function to convert datetime to string
def serialize_datetime(dt):
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

# Prepare the data for Astro
entries = [
    {
        "year": row[0],
        "date": serialize_datetime(row[1]) or serialize_datetime(row[2]),  # Use created_date or modified_date
        "details": f"{row[3]} - {row[4]}"  # readable_name and description
    }
    for row in results
    if row[5] == 'Relevant' 
]

undecided_count = sum(1 for row in results if row[5] == 'Undecided')

# Prepare the final data to output as a JSON file
data = {
    "entries": entries,
    "undecidedCount": undecided_count
}

# Save the results as a JSON file
with open('src/data/results.json', 'w') as f:
    json.dump(data, f)

# Close the connection
conn.close()
