# %% [markdown]
# # Topic Modeling for Obsidian Vault
# Analyzing English and Russian content using BERTopic

# %% [markdown]
# ## Setup and Imports

# %%
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import frontmatter
import glob
import os
import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd
import plotly.express as px

# Download NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# %% [markdown]
# ## Helper Functions

# %%
def read_obsidian_files(vault_path):
    """Read all markdown files from Obsidian vault"""
    documents = []
    file_names = []
    
    for filepath in glob.glob(os.path.join(vault_path, "**/*.md"), recursive=True):
        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                post = frontmatter.load(file)
                content = post.content
                sentences = sent_tokenize(content)
                documents.extend(sentences)
                file_names.extend([os.path.basename(filepath)] * len(sentences))
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    return documents, file_names

# %%
def create_topic_model():
    """Create multilingual topic model"""
    embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        language="multilingual",
        calculate_probabilities=True,
        verbose=True
    )
    
    return topic_model

# %% [markdown]
# ## Main Analysis

# %%
# Set your vault path
vault_path = "/Users/denis/Yandex.Disk.localized/thinking mind/thinking mind"

# Read documents
print("Reading documents...")
documents, file_names = read_obsidian_files(vault_path)

print(f"Found {len(documents)} sentences in {len(set(file_names))} files")

# %% [markdown]
# ## Create and Train Topic Model

# %%
# Create and train the model
print("Creating topic model...")
topic_model = create_topic_model()

print("Fitting topic model...")
topics, probs = topic_model.fit_transform(documents)

# Create DataFrame with results
df = pd.DataFrame({
    'Document': documents,
    'File': file_names,
    'Topic': topics,
    'Probability': probs.max(axis=1)
})

# %% [markdown]
# ## Visualizations

# %%
# 1. Interactive topic visualization
fig_topics = topic_model.visualize_topics()
fig_topics.show()

# %%
# 2. Topic hierarchy visualization
fig_hierarchy = topic_model.visualize_hierarchy()
fig_hierarchy.show()

# %%
# 3. Topic barchart
fig_barchart = topic_model.visualize_barchart()
fig_barchart.show()

# %% [markdown]
# ## Analysis Results

# %%
# Show top topics
print("\nTop Topics:")
print(topic_model.get_topic_info())

# %% [markdown]
# ## Additional Analysis (Optional)

# %%
# Show documents for a specific topic (e.g., topic 0)
topic_num = 0
topic_docs = df[df['Topic'] == topic_num]
print(f"\nSample documents from Topic {topic_num}:")
print(topic_docs['Document'].head())

# %%
# Topic distribution visualization
topic_counts = df['Topic'].value_counts()
fig = px.bar(x=topic_counts.index, y=topic_counts.values,
             title='Distribution of Topics',
             labels={'x': 'Topic Number', 'y': 'Number of Documents'})
fig.show()