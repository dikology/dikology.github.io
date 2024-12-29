import streamlit as st
import duckdb
import pandas as pd

# Connect to DuckDB
conn = duckdb.connect("yandex_files.duckdb")

# Fetch data
st.title("File Curation Tool")
df = conn.execute("SELECT * FROM files").df()

# Sidebar Filters
st.sidebar.subheader("Filters")
relevance_filter = st.sidebar.selectbox(
    "Select Relevance",
    ["All", "Relevant", "Not Relevant", "Undecided"]
)
week_number_filter = st.sidebar.number_input(
    "Select Week Number (1-52)", min_value=1, max_value=52, value=1
)

# Convert 'created' and 'modified' to datetime
df['created'] = pd.to_datetime(df['created'])
df['modified'] = pd.to_datetime(df['modified'])

# Extract week numbers from 'created' and 'modified'
df['created_week'] = df['created'].dt.isocalendar().week
df['modified_week'] = df['modified'].dt.isocalendar().week

# Apply filters based on user input
if relevance_filter != "All":
    df = df[df['relevance'] == relevance_filter]

df = df[(df['created_week'] == week_number_filter) | (df['modified_week'] == week_number_filter)]

# Display Files with Checkboxes and Mark as Irrelevant Button
st.subheader(f"Curate Files ({len(df)} files)")
selected_files = []  # List to store selected file paths for batch processing

# Loop through files and display each with a checkbox and a "Mark as Irrelevant" button
for idx, row in df.iterrows():
    # Create columns for side-by-side layout
    col1, col2 = st.columns([4, 1])  # Adjust column width (4 for expander, 1 for buttons)
    
    with col1:  # This column will hold the expander and editable fields
        # Expandable row for detailed view (editable fields)
        with st.expander(f"{row['name']} - {row['modified']}", expanded=False):
            # Editable fields
            readable_name = st.text_input("Human-readable name", value=row['readable_name'], key=f"name_{idx}")
            description = st.text_area("Description", value=row['description'], key=f"description_{idx}")
            relevance_options = ["Relevant", "Not Relevant", "Undecided"]
            relevance = st.selectbox(
                "Relevance",
                options=relevance_options,
                index=relevance_options.index(row['relevance']) if row['relevance'] in relevance_options else 0,
                key=f"relevance_{idx}"
            )

            # Update logic for editable fields
            if st.button("Save", key=f"save_{idx}"):
                conn.execute(
                    "UPDATE files SET readable_name=?, description=?, relevance=? WHERE path=?",
                    (readable_name, description, relevance, row['path'])
                )
                st.success(f"Updated {row['name']}")

    with col2:  # This column will hold the checkbox and the "Mark as Irrelevant" button
        # Checkbox to select file
        if st.checkbox(f"Select", key=f"checkbox_{idx}"):
            selected_files.append(row['path'])

        # Mark as Irrelevant button for individual rows
        if st.button(f"Irrelevant", key=f"irrelevant_{idx}"):
            conn.execute(
                "UPDATE files SET relevance = 'Not Relevant' WHERE path = ?",
                (row['path'],)
            )
            st.success(f"Marked {row['name']} as Not Relevant")

# Batch Update (mark selected files as "Not Relevant")
if selected_files:
    batch_relevance = st.sidebar.button("Mark Selected as Irrelevant")
    if batch_relevance:
        # Apply batch update to selected files
        conn.execute(
            "UPDATE files SET relevance = 'Not Relevant' WHERE path IN ?", (tuple(selected_files),)
        )
        st.success(f"Marked {len(selected_files)} files as Not Relevant")
