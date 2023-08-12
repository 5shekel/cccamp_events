import json
import pytz
import argparse
from datetime import datetime, timedelta

def get_talk_details_by_text(data, text=None):
    matching_talks = []
    for talk in data['talks']:
        title_obj = talk['title']
        if isinstance(title_obj, dict):
            title_text = title_obj.get('en', title_obj.get('de', ''))
        else:
            title_text = title_obj        
        
        abstract_text = talk.get('abstract', '')
        speaker_codes = talk.get('speakers', [])
        speaker_names = [speaker['name'] for speaker in data['speakers'] if speaker['code'] in speaker_codes]
        talk['speakers'] = speaker_names

        if text and (text.lower() in title_text.lower() or
                     text.lower() in abstract_text.lower() or
                     any(text.lower() in speaker_name.lower() for speaker_name in speaker_names)) or not text:

            talk['title'] = title_text  # Set the title to the extracted text

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

    # If the user entered a search query, return all matching talks
    if text:
        return matching_talks

    # If the user just entered the app, return the next 10 upcoming talks
    current_time = datetime.now(pytz.utc) + timedelta(hours=2)  # Convert to UTC+2 timezone
    upcoming_talks = [talk for talk in matching_talks if datetime.strptime(talk['unmodified_start'], '%Y-%m-%dT%H:%M:%S%z') > current_time]
    return upcoming_talks[:10]

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
