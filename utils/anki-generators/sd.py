# deck generator
# inspiration: https://github.com/pranavdeshai/anki-prettify/blob/main/tools/build.py
import json
from random import randrange
from pathlib import Path
import genanki
import yaml
import os

# Field contents for each note type
NOTE_FIELDS = {
    "basic": [
        "What is <b>Anki</b>?",
        "<b>Anki</b>&nbsp;is a <u>free and open-source</u>&nbsp;flashcard&nbsp;program using&nbsp;<i>spaced repetition</i>, a technique from&nbsp;cognitive science&nbsp;for fast and long-lasting memorization.<br><br><img src='https://upload.wikimedia.org/wikipedia/commons/9/9a/Anki_2.1.6_screenshot.png'><br>Anki 2.1.6 screenshot (<a href='https://en.wikipedia.org/wiki/Anki_(software)'>https://en.wikipedia.org/wiki/Anki_(software)</a>)",
    ],
    "basic_reverse": [
        "What is <b>Anki</b>?",
        "<b>Anki</b>&nbsp;is a <u>free and open-source</u>&nbsp;flashcard&nbsp;program using&nbsp;<i>spaced repetition</i>, a technique from&nbsp;cognitive science&nbsp;for fast and long-lasting memorization.<br><br><img src='https://upload.wikimedia.org/wikipedia/commons/9/9a/Anki_2.1.6_screenshot.png'><br>Anki 2.1.6 screenshot (<a href='https://en.wikipedia.org/wiki/Anki_(software)'>https://en.wikipedia.org/wiki/Anki_(software)</a>)",
    ],
    "cloze": [
        "<b>Anki</b>&nbsp;is a <u>free and open-source</u>&nbsp;{{c1::flashcard}}&nbsp;program using&nbsp;<i>spaced repetition</i>, a technique from&nbsp;cognitive science&nbsp;for fast and long-lasting memorization.<br><br><img src='https://upload.wikimedia.org/wikipedia/commons/9/9a/Anki_2.1.6_screenshot.png'>",
        "Anki 2.1.6 screenshot (<a href='https://en.wikipedia.org/wiki/Anki_(software)'>https://en.wikipedia.org/wiki/Anki_(software)</a>)",
    ],
}

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
    return {'type': 'basic', 'front': front, 'back': back, 'id': meta.get('id', None)}

def create_card(model, front, back, id):
    note = genanki.Note(
            guid=id,
            fields=[front, back],
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
    ) as f2, open((root / "utils/anki-generators/templates" / "nord.css")) as f3:
        front_html = f1.read()
        back_html = f2.read()
        css = f3.read()
        
        templates = [
                {
                    "name": "Card 1",
                    "qfmt": front_html,
                    "afmt": back_html,
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

        model = genanki.Model(
            model_id=ids[n_deck]["model_id"],
            name=f"prettify-{n_deck}",
            fields=model_fields,
            templates=templates,
            css=css,
            model_type=genanki.Model.FRONT_BACK,
        )

        deck = genanki.Deck(
            ids[n_deck]["deck_id"],
            f"Prettify::{n_deck.capitalize()}",
        )
        
        deck.add_model(model)
        
        for filename in os.listdir(f"src/content/docs/{n_deck}"): 
            print(filename)
            if filename.endswith('.md'):
                card_data = load_card(os.path.join(f'src/content/docs/{n_deck}', filename))
                
                if card_data:  # Check if card_data is not None
                    deck.add_note(create_card(model, card_data['front'], card_data['back'], card_data['id']))

        # Note type-wise packages
        genanki.Package(deck).write_to_file(
            root / "public" / "decks" / f"prettify-{n_deck}.apkg"
        )