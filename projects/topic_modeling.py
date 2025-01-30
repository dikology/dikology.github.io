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
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pymystem3 import Mystem

# Download NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


# %% [markdown]
# ## Helper Functions

# %%
# Add Russian stop words (common words that don't carry much meaning)
RUSSIAN_STOP_WORDS = set('''
а ах без более бы был была были было быть в вам вас весь во вот 
все всего всех вы где да даже для до его ее если есть еще же за 
здесь и из или им их к как ко когда кто ли либо мне может мы на над 
но ну о об однако он она они оно от очень по под при с со так также 
такой там те тем то того тоже той только том ты у уже хотя чего чей 
чем что чтобы чье чья эта эти это я
'''.split())

def preprocess_text(text):
    """
    Enhanced text preprocessing for English and Russian
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Initialize lemmatizers
    eng_lemmatizer = WordNetLemmatizer()
    rus_lemmatizer = Mystem()
    
    # 1. Basic cleaning
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove markdown
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_~`]', '', text)
    
    # Remove numbers and special characters
    text = re.sub(r'[^\w\s\.\,\!\?\-\—\–\"\«\»А-Яа-яЁё]', ' ', text)
    text = re.sub(r'\d+', '', text)
    
    # 2. Normalize text
    text = text.lower()
    
    # 3. Tokenization and stop words removal
    stop_words = set(stopwords.words('english')).union(RUSSIAN_STOP_WORDS)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    
    # 4. Lemmatization
    # Separate Russian and English words
    rus_words = [w for w in words if bool(re.search('[а-яА-ЯёЁ]', w))]
    eng_words = [w for w in words if w not in rus_words]
    
    # Lemmatize English words
    eng_lemmatized = [eng_lemmatizer.lemmatize(w) for w in eng_words]
    
    # Lemmatize Russian words
    if rus_words:
        rus_text = ' '.join(rus_words)
        rus_lemmatized = rus_lemmatizer.lemmatize(rus_text)
        rus_lemmatized = [w for w in rus_lemmatized if w.strip() and w not in stop_words]
    else:
        rus_lemmatized = []
    
    # 5. Combine and clean final results
    processed_words = eng_lemmatized + rus_lemmatized
    processed_words = [w.strip() for w in processed_words if len(w.strip()) > 2]
    
    return ' '.join(processed_words)
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
                # Apply preprocessing to the whole document
                processed_content = preprocess_text(content)
                documents.append(processed_content)
                file_names.append(os.path.basename(filepath))
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

print(f"Found {len(documents)} documents in {len(set(file_names))} files")

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