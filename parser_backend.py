import json
import argparse
from datetime import datetime, timedelta

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

            if 'track' in talk:
                track_name = next((track['name'] for track in data['tracks'] if track['id'] == talk['track']), None)
                talk['track'] = track_name
        
            room_name = next((room['name'] for room in data['rooms'] if room['id'] == talk['room']), None)
            talk['track'] = track_name
            talk['speakers'] = speaker_names
            talk['room'] = room_name

            # Convert start and end times to human-readable format with UTC+2 offset
            start_time = datetime.strptime(talk['start'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)
            end_time = datetime.strptime(talk['end'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)

            # Add unmodified start and end times to the talk
            talk['unmodified_start'] = talk['start']
            talk['unmodified_end'] = talk['end']

            # Replace day of the week with its literal name
            day_name = start_time.strftime('%A')
            talk['start'] = start_time.strftime(f'{day_name} %I:%M %p ')
            talk['end'] = end_time.strftime(f' {day_name} %I:%M %p ')

            # Convert unmodified start and end times with UTC+2 offset
            unmodified_start_time = datetime.strptime(talk['unmodified_start'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)
            unmodified_end_time = datetime.strptime(talk['unmodified_end'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)

            # Calculate the duration
            duration = unmodified_end_time - unmodified_start_time
            duration_hours = duration.seconds // 3600
            duration_minutes = (duration.seconds % 3600) // 60

            # Add the duration to the talk
            talk['duration'] = f'{duration_hours} hours {duration_minutes} minutes'


            matching_talks.append(talk)
            
    return matching_talks

def main():
    parser = argparse.ArgumentParser(description='Extract talk details from JSON data.')
    parser.add_argument('--file', required=False,  help='Path to the JSON file.', default='cccamp.json')
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
