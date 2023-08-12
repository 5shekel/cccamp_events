import json
import argparse
from datetime import datetime, timedelta

def get_talk_details_by_text(data, text):
    matching_talks = []
    for talk in data['talks']:
        title_text = talk['title']['en'] if isinstance(talk['title'], dict) else talk['title']
        abstract_text = talk.get('abstract', '')
        speaker_codes = talk.get('speakers', [])

        if (text.lower() in title_text.lower() or
            text.lower() in abstract_text.lower() or
            any(text.lower() in speaker['name'].lower() for speaker in data['speakers'] if speaker['code'] in speaker_codes)):

            speaker_names = [speaker['name'] for speaker in data['speakers'] if speaker['code'] in speaker_codes]
            talk['speakers'] = speaker_names

            track_id = talk.get('track', None)
            if track_id:
                track_name_obj = next((track['name'] for track in data['tracks'] if track['id'] == track_id), None)
                track_name = track_name_obj.get('en', track_name_obj.get('de', '')) if track_name_obj else ''
                talk['track'] = track_name

            room_name_obj = next((room['name'] for room in data['rooms'] if room['id'] == talk['room']), None)
            room_name = room_name_obj.get('en', room_name_obj.get('de', '')) if room_name_obj else ''
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

            # Calculate the duration
            duration = end_time - start_time
            duration_parts = []
            duration_hours = duration.seconds // 3600
            duration_minutes = (duration.seconds % 3600) // 60
            if duration_hours > 0:
                duration_parts.append(f'{duration_hours} hours')
            if duration_minutes > 0:
                duration_parts.append(f'{duration_minutes} minutes')
            talk['duration'] = ' '.join(duration_parts) if duration_parts else '0 minutes'

            matching_talks.append(talk)
            
    return matching_talks

def main():
    parser = argparse.ArgumentParser(description='Extract talk details from JSON data.')
    parser.add_argument('--file', required=False, help='Path to the JSON file.', default='cccamp.json')
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
