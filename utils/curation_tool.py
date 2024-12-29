import streamlit as st
import duckdb
import pandas as pd

# Connect to DuckDB
conn = duckdb.connect("yandex_files.duckdb")

# Fetch data
st.title("File Curation Tool")
df = conn.execute("SELECT * FROM files").df()

# Display files
st.subheader("Curate Files")
for idx, row in df.iterrows():
    with st.expander(f"{row['name']} - {row['modified']}"):
        # Editable fields
        #readable_name = st.text_input("Human-readable name", value=row['human_readable_name'], key=f"name_{idx}")
        #description = st.text_area("Description", value=row['description'], key=f"description_{idx}")
        #relevance = st.checkbox("Mark as Relevant", value=row['relevance'], key=f"relevance_{idx}")

        # Update logic
        if st.button("Save", key=f"save_{idx}"):
            conn.execute(
                "UPDATE files SET human_readable_name=?, description=?, relevance=? WHERE id=?",
                (readable_name, description, relevance, row['id'])
            )
            st.success(f"Updated {row['name']}")

# Add new files manually (if needed)
st.sidebar.subheader("Add New File")
with st.sidebar.form("add_file"):
    new_name = st.text_input("File Name")
    new_path = st.text_input("File Path")
    new_date = st.date_input("Modified Date")
    if st.form_submit_button("Add"):
        conn.execute(
            "INSERT INTO files (name, path, modified_date) VALUES (?, ?, ?)",
            (new_name, new_path, new_date)
        )
        st.sidebar.success("File added!")
