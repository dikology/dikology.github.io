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
    
    for filename in os.listdir('src/pages/posts/analytics'):
        if filename.endswith('.md'):
            front, back = load_card(os.path.join('src/pages/posts/analytics', filename))
            deck.add_note(create_basic_card(front, back))

    genanki.Package(deck).write_to_file('output/anki_deck.apkg')

if __name__ == '__main__':
    main()