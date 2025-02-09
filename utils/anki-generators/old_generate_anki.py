import genanki
import yaml
import os

def load_card(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    meta, body = content.split('---', 2)[1:]  # Split YAML front matter and card body
    meta = yaml.safe_load(meta)
    card_type = meta.get('type', 'basic')

    if card_type == 'cloze':
        text = body.strip().split('**Text:**', 1)[-1].strip()
        return {'type': 'cloze', 'text': text, 'id': meta.get('id', None), 'tags': meta.get('tags', [])}
    else:
        front, back = body.split('**Back:**', 1)
        front = front.split('**Front:**', 1)[-1].strip()
        back = back.strip()
        return {'type': 'basic', 'front': front, 'back': back, 'id': meta.get('id', None), 'tags': meta.get('tags', [])}

def create_deck(deck_id, deck_name):
    return genanki.Deck(deck_id, deck_name)

def create_basic_card(front, back):
    return genanki.Note(
        model=genanki.BASIC_MODEL,
        fields=[front, back]
    )

def main():
    deck = create_deck(1234567890, "Analytics Anki Deck")
    
    for filename in os.listdir('src/pages/posts/analytics'):  # Adjusted path
        if filename.endswith('.md'):
            card_data = load_card(os.path.join('src/pages/posts/analytics', filename))
            
            if card_data['type'] == 'basic':
                deck.add_note(create_basic_card(card_data['front'], card_data['back']))
            elif card_data['type'] == 'cloze':
                deck.add_note(
                    genanki.Note(
                        model=genanki.CLOZE_MODEL,
                        fields=[card_data['text']],
                        tags=card_data['tags']
                    )
                )

    output_path = 'public/decks'
    output_file = os.path.join(output_path, 'analytics.apkg')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    genanki.Package(deck).write_to_file(output_file)
    
if __name__ == '__main__':
    main()