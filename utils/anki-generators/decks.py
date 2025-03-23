# deck generator
# inspiration: https://github.com/pranavdeshai/anki-prettify/blob/main/tools/build.py
import json
from random import randrange
from pathlib import Path
import genanki
import yaml
import os

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
    
    # Check if the type is 'basic-media' and parse for markdown media syntax
    media = None
    if meta.get('type', 'basic') == 'basic-media':
        # Look for markdown image/video pattern ![...](filename)
        media_start = back.find('![')
        if media_start != -1:
            media_end = back.find(')', media_start) + 1
            markdown_media = back[media_start:media_end].strip()
            # Extract filename from markdown syntax
            filename = markdown_media[markdown_media.find('(')+1:markdown_media.find(')')]
            
            # For Anki, we should use just the filename, not the path
            # Extract just the filename without directory path
            base_filename = os.path.basename(filename)
            
            # Determine if it's a video or image based on file extension
            if base_filename.lower().endswith(('.mp4', '.webm', '.mov')):
                # Use [sound:filename] syntax for video files in Anki
                media = f'[sound:{base_filename}]'
            else:
                # For images, use <img> tag with just the filename
                media = f'<img src="{base_filename}">'
                
            back = back.replace(markdown_media, '').strip()  # Remove the markdown media

    return {'type': meta.get('type', 'basic'), 'front': front, 'back': back, 'media': media, 'id': meta.get('id', None)}

def create_card(model, front, back, id):
    note = genanki.Note(
            guid=id,
            fields=[front, back],
            model=model
        )
    return note

def create_media_card(model, front, back, media, id):
    note = genanki.Note(
            guid=id,
            fields=[front, back, media],
            model=model
        )
    return note

# Store the root path for future use
root = Path(f"{__file__}/../../..").resolve()

# Update genanki IDs
with open(root / "utils/anki-generators/ids.json", "r+") as ids_file:
    ids = json.load(ids_file)

for n_deck in ids:
    with open(
        (root / "utils/anki-generators/templates" / "basic-front.html"),
        "r+",
    ) as f1, open(
        (root / "utils/anki-generators/templates" / "basic-back.html"), "r+"
    ) as f2, open(
        (root / "utils/anki-generators/templates" / "basic-back-media.html"), "r+"
    ) as f4, open((root / "utils/anki-generators/templates" / "nord.css")) as f3:
        front_html = f1.read()
        back_html = f2.read()
        css = f3.read()
        back_media_html = f4.read()
        
        templates = [
                {
                    "name": "Card 1",
                    "qfmt": front_html,
                    "afmt": back_html,
                }
            ]

        templates_media = [
                {
                    "name": "Card 1",
                    "qfmt": front_html,
                    "afmt": back_media_html,
                }
            ]
        
        model_fields = [
            {
                # Cloze note types have different field names
                "name": "Front"
            },
            {
                "name": "Back"
            },
        ]
        
        model_fields_media = [
            {
                # Cloze note types have different field names
                "name": "Front"
            },
            {
                "name": "Back"
            },
            {
                "name": "Media"
            },
        ]

        model = genanki.Model(
            model_id=ids[n_deck]["model_id"],
            name=f"{n_deck}",
            fields=model_fields,
            templates=templates,
            css=css,
            model_type=genanki.Model.FRONT_BACK,
        )
        
        model_media = genanki.Model(
            model_id=ids[n_deck]["model_media_id"],
            name=f"{n_deck}",
            fields=model_fields_media,
            templates=templates_media,
            css=css,
            model_type=genanki.Model.FRONT_BACK,
        )

        deck = genanki.Deck(
            ids[n_deck]["deck_id"],
            f"{n_deck.capitalize()}",
        )
        
        deck.add_model(model)
        deck.add_model(model_media)
        
        media_files = []  # Initialize a list to store media filenames

        for filename in os.listdir(f"src/content/docs/{n_deck}"): 
            print(filename)
            if filename.endswith('.md'):
                card_data = load_card(os.path.join(f'src/content/docs/{n_deck}', filename))
                
                if card_data:  # Check if card_data is not None
                    if card_data['type'] == 'basic':
                        deck.add_note(create_card(model, card_data['front'], card_data['back'], card_data['id']))
                    if card_data['type'] == 'basic-media':
                        deck.add_note(create_media_card(model_media, card_data['front'], card_data['back'], card_data['media'], card_data['id']))

            # Identify media files by their filenames
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mov')):
                # Use full path for the file collection, but Anki will reference by filename only
                media_files.append(os.path.join(f'src/content/docs/{n_deck}', filename))
                print(f"Adding media file: {filename}")  # Debug output

        # Note type-wise packages
        my_package = genanki.Package(deck)
        my_package.media_files = media_files  # Assign the list of media files
        my_package.write_to_file(
            root / "public" / "decks" / f"{n_deck}.apkg"
        )