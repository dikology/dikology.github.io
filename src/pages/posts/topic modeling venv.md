---
layout: ../../layouts/MarkdownPostLayout.astro
title: Venv for topic modeling
description: I wasn't able to run the project with poetry, so I created a venv
date: 2025-01-24
image:
  src: https://cdn.midjourney.com/9e473473-ef85-40fb-b871-53f0b358e47e/0_0.png
  alt: image from midjourney
featured: false
draft: true
category: data
---

Create a virtual environment and install the necessary dependencies for [[topic modeling project]]. Here's what you need to do:

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
```

You can also create a `requirements.txt` file with these dependencies:

```text:requirements.txt
bertopic
sentence-transformers
python-frontmatter
nltk
pandas
plotly
nbformat
```

Then you can install everything at once using:

```bash
pip install -r requirements.txt
```
