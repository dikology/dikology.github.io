---
title: Sailing Deck
description: A simple way to remember things that you frequently forget
created: March 29
modified: March 29
tags:
  - sailing-deck
---
Sailing requires a lot of knowledge that you'll use infrequently - which makes it the perfect candidate for spaced repetition. But existing Anki decks aren't always ideal. This article explains the "Sailing Deck" project, a system that creates personalized Anki flashcards from the same Markdown files that power an Astro-based website.

## The Problem with Existing Sailing Anki Decks

While there are sailing Anki decks available, they come with several limitations:

1. **Irrelevant Content**: Other people's decks often include concepts you either already know well or don't need for your specific sailing environment
2. **Limited Customization**: Standard Anki cards lack personality and design flexibility
3. **No Version Control**: Traditional Anki card creation doesn't integrate with modern development workflows
4. **Single-Purpose**: Most flashcard content exists only in the Anki ecosystem
5. **Clunky Editing**: Anki's built-in editor is functional but far from a modern code editor

## The Solution: Dual-Purpose Markdown Files

The Sailing Deck project solves these problems with a unique approach: create Markdown files that serve double duty as both web pages and flashcard content.

### How It Works

Each Markdown file follows a specific format:

```markdown
---
title: Bowline Knot
description: How to tie a bowline knot
type: basic-media
id: 1234567890
---

**Front:** How do you tie a bowline knot?

**Back:** The bowline creates a fixed loop at the end of a line.

1. Make a small loop in the standing part of the line
2. Pass the working end up through the loop
3. Bring the working end around behind the standing part
4. Pass the working end back down through the loop
5. Tighten by pulling the standing part

![Bowline Knot Demonstration](bowline-knot.gif)
```

The Python script `decks.py` then:

1. Reads these Markdown files
2. Parses the YAML frontmatter and content
3. Extracts the front and back content using the `**Front:**` and `**Back:**` markers
4. Identifies and processes any media files
5. Generates Anki deck packages (.apkg files)

## The Code: Anki Deck Generator

The heart of the system is a Python script that processes the Markdown files and generates Anki decks. Here's how the main components work:

### Loading Card Content

```python
def load_card(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    meta, body = content.split('---', 2)[1:]  # Split YAML front matter and card body
    meta = yaml.safe_load(meta)

    # Check if '**Back:**' is in the body
    if '**Back:**' not in body:
        print(f"Skipping file {file_path}: '**Back:**' not found.")
        return None  # Skip this file

    front, back = body.split('**Back:**', 1)
    front = front.split('**Front:**', 1)[-1].strip()
    back = back.strip()
    
    # Process media if present
    # ...
    
    return {'type': meta.get('type', 'basic'), 'front': front, 'back': back, 'media': media, 'id': meta.get('id', None)}
```

### Media Handling

The script handles both images and videos:

```python
if meta.get('type', 'basic') == 'basic-media':
    # Look for markdown image/video pattern ![...](filename)
    media_start = back.find('![')
    if media_start != -1:
        media_end = back.find(')', media_start) + 1
        markdown_media = back[media_start:media_end].strip()
        # Extract filename from markdown syntax
        filename = markdown_media[markdown_media.find('(')+1:markdown_media.find(')')]
        
        # Extract just the filename without directory path
        base_filename = os.path.basename(filename)
        
        # Determine if it's a video or image based on file extension
        if base_filename.lower().endswith(('.mp4', '.webm', '.mov')):
            media = f'[sound:{base_filename}]'
        else:
            media = f'<img src="{base_filename}">'
            
        back = back.replace(markdown_media, '').strip()  # Remove the markdown media
```

### Deck Generation

The script reads all Markdown files from the sailing-deck directory and generates an Anki package:

```python
deck = genanki.Deck(ids[n_deck]["deck_id"], f"{n_deck.capitalize()}")
media_files = []

for filename in os.listdir(f"src/content/docs/{n_deck}"): 
    if filename.endswith('.md'):
        card_data = load_card(os.path.join(f'src/content/docs/{n_deck}', filename))
        
        if card_data:
            if card_data['type'] == 'basic':
                deck.add_note(create_card(model, card_data['front'], card_data['back'], card_data['id']))
            if card_data['type'] == 'basic-media':
                deck.add_note(create_media_card(model_media, card_data['front'], card_data['back'], card_data['media'], card_data['id']))

    # Add media files
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mov')):
        media_files.append(os.path.join(f'src/content/docs/{n_deck}', filename))

my_package = genanki.Package(deck)
my_package.media_files = media_files
my_package.write_to_file(root / "public" / "decks" / f"{n_deck}.apkg")
```

## Benefits of This Approach

This dual-purpose Markdown system offers significant advantages:

1. **Personalized Content**: Create exactly the cards you need for your sailing knowledge gaps
2. **Design Flexibility**: Custom HTML/CSS templates for your cards
3. **Version Control**: Track changes to your flashcards with Git
4. **Dual Availability**: Content is available both as website documentation and Anki flashcards
5. **Superior Editing Experience**: Use your favorite code editor with syntax highlighting and other developer tools

## Getting Started

To use this system:

1. Create Markdown files following the format shown above
2. Organize them in a directory structure that makes sense for your Astro site
3. Run the deck generation script to create your Anki package
4. Import the generated .apkg file into Anki

The example sailing deck covers essential topics like points of sail, knots, navigation, safety procedures, and more - all maintained in a single repository and automatically converted to flashcards.

## Conclusion

By combining documentation and spaced repetition learning in one workflow, the Sailing Deck system makes it easier to maintain and learn sailing knowledge. The same content that serves as your reference documentation also powers your learning through Anki's proven spaced repetition system.

Whether you're studying for sailing certifications or just want to keep your sailing knowledge fresh between seasons, this system offers a developer-friendly approach to creating and maintaining personalized flashcards.

[[Sailing]]
[[Travel]]
