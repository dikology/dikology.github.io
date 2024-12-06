---
layout: ../../layouts/MarkdownPostLayout.astro
title: Automating Anki Decks with GitHub Actions & Releases
description: Automating Anki Decks with GitHub Actions Releases
date: 2024-12-05
image:
  src: https://cdn.midjourney.com/d5205413-1fed-4ef0-bef5-27c5f0f4a6fb/0_0.png
featured: true
draft: true
category: tech
---
# Automating Anki Deck Generation and Updates with GitHub Actions & GitHub Releases

This guide will walk you through automating the creation and updating of Anki decks using GitHub Actions. Each Anki card is represented by individual `.md` files, and GitHub Releases will serve as a convenient way to distribute the generated deck.

---

## Prerequisites

1. **GitHub Repository**: Ensure you have a GitHub repository where `.md` files for the Anki cards are stored.
2. **Anki Export Tool**: Use [genanki](https://github.com/kerrickstaley/genanki) or a similar library to create `.apkg` files from `.md` files.
3. **Python Environment**: Python 3.x installed locally for testing.
4. **GitHub Actions**: Familiarity with basic GitHub Actions concepts.

---

## Folder Structure

```plaintext
.
├── cards/
│   ├── card1.md
│   ├── card2.md
│   └── ...
├── scripts/
│   └── generate_anki.py
├── .github/
│   └── workflows/
│       └── generate-deck.yml
└── requirements.txt
```

- **cards/**: Directory containing individual `.md` files for each card.
- **scripts/**: Directory for custom scripts like `generate_anki.py`.
- **.github/workflows/**: GitHub Actions workflows.

---

## Markdown Templates for Anki Cards

### 1. **Basic Card**

```markdown
---
type: basic
id: card1
tags: [example, basic]
---

**Front:**
What is the capital of France?

**Back:**
Paris
```

### 2. **Cloze Card**

```markdown
---
type: cloze
id: card2
tags: [example, cloze]
---

**Text:**
The capital of France is {{c1::Paris}}.
```

### 3. **Basic (Reversed) Card**

```markdown
---
type: basic-reversed
id: card3
tags: [example, reversed]
---

**Front:**
What is the capital of Japan?

**Back:**
Tokyo
```

---

## Python Script: `generate_anki.py`

```python
import genanki
import yaml
import os

def load_card(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    front, back = content.split('**Back:**', 1)
    front = front.split('**Front:**', 1)[-1].strip()
    back = back.strip()
    return front, back

def create_deck(deck_id, deck_name):
    return genanki.Deck(deck_id, deck_name)

def create_basic_card(front, back):
    return genanki.Note(
        model=genanki.BASIC_MODEL,
        fields=[front, back]
    )

def main():
    deck = create_deck(1234567890, "GitHub Anki Deck")
    
    for filename in os.listdir('cards'):
        if filename.endswith('.md'):
            front, back = load_card(os.path.join('cards', filename))
            deck.add_note(create_basic_card(front, back))

    genanki.Package(deck).write_to_file('output/anki_deck.apkg')

if __name__ == '__main__':
    main()
```

---

## GitHub Actions Workflow: `generate-deck.yml`

```yaml
name: Generate Anki Deck

on:
  push:
    paths:
      - 'cards/**'
  workflow_dispatch:

jobs:
  build-deck:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Generate Anki Deck
      run: python scripts/generate_anki.py

    - name: Upload Anki Deck as Release Asset
      uses: actions/upload-artifact@v3
      with:
        name: anki_deck
        path: output/anki_deck.apkg
```

---

## Publishing with GitHub Releases

1. Navigate to **Releases** in your repository.
2. Click **Draft a new release**.
3. Attach the `anki_deck.apkg` from the `output/` directory.
4. Provide a release title and description, then click **Publish Release**.

---

## Improvements & Extensions

1. **Metadata Parsing**: Use YAML front matter to support different card types (e.g., Cloze cards).
2. **Auto-tagging**: Parse `tags` from `.md` files to organize decks better.
3. **Custom Models**: Extend `genanki` to support custom note types.

---

### Conclusion

This setup automates the generation and distribution of Anki decks via GitHub, making it easy to manage and update your study material collaboratively.