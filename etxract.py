import json
import argparse

def get_talk_details_by_text(data, text):
    matching_talks = []
    for talk in data['talks']:
        title_text = talk['title']['en'] if isinstance(talk['title'], dict) else talk['title']
        abstract_text = talk['abstract'] if 'abstract' in talk else ''
        speaker_codes = talk['speakers'] if 'speakers' in talk else []
        speaker_names = [speaker['name'] for speaker in data['speakers'] if speaker['code'] in speaker_codes]

        if (text.lower() in title_text.lower() or
            text.lower() in abstract_text.lower() or
            any(text.lower() in speaker_name.lower() for speaker_name in speaker_names)):

            track_name = next((track['name']['en'] for track in data['tracks'] if track['id'] == talk['track']), None)
            room_name = next((room['name']['en'] for room in data['rooms'] if room['id'] == talk['room']), None)
            talk['track'] = track_name
            talk['speakers'] = speaker_names
            talk['room'] = room_name
            matching_talks.append(talk)
            
    return matching_talks

def main():
    parser = argparse.ArgumentParser(description='Extract talk details from JSON data.')
    parser.add_argument('--file', required=True, help='Path to the JSON file.')
    parser.add_argument('--text', required=False, help='Text to search in title, abstract, and speakers.')
    args = parser.parse_args()

    with open(args.file, 'r') as file:
        data = json.load(file)

    text = args.text

    if not text:
        text = input("Please enter the text to search in title, abstract, or speakers: ")

    matching_talks = get_talk_details_by_text(data, text=text)
    print(json.dumps(matching_talks, indent=4))

if __name__ == '__main__':
    main()
