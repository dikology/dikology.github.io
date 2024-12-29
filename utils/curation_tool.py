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
        readable_name = st.text_input("Human-readable name", value=row['readable_name'], key=f"name_{idx}")
        description = st.text_area("Description", value=row['description'], key=f"description_{idx}")
        relevance_options = ["Relevant", "Not Relevant", "Undecided"]  # Add options as needed
        relevance = st.selectbox(
            "Relevance",
            options=relevance_options,
            index=relevance_options.index(row['relevance']) if row['relevance'] in relevance_options else 0,
            key=f"relevance_{idx}"
        )

        # Update logic
        if st.button("Save", key=f"save_{idx}"):
            conn.execute(
                "UPDATE files SET readable_name=?, description=?, relevance=? WHERE path=?",
                (readable_name, description, relevance, row['path'])
            )
            st.success(f"Updated {row['name']}")