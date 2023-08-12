import json
import pytz
import argparse
from datetime import datetime, timedelta

def get_talk_details_by_text(data, text=None, current_time=None):
    matching_talks = []
    in_progress_talks = []
    upcoming_talks = []

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

        track_id = talk.get('track', None)
        if track_id:
            track_name_obj = next((track['name'] for track in data['tracks'] if track['id'] == track_id), None)
            track_name = track_name_obj.get('en', track_name_obj.get('de', '')) if track_name_obj else ''
            talk['track'] = track_name

        if text and (text.lower() in title_text.lower() or
                    text.lower() in abstract_text.lower() or
                    any(text.lower() in speaker_name.lower() for speaker_name in speaker_names) or
                    (text.lower() in track_name.lower())) or not text:

            talk['title'] = title_text  # Set the title to the extracted text


            room_name_obj = next((room['name'] for room in data['rooms'] if room['id'] == talk['room']), None)
            room_name = room_name_obj.get('en', room_name_obj.get('de', '')) if room_name_obj else ''
            talk['room'] = room_name

            start_time = datetime.strptime(talk['start'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)
            end_time = datetime.strptime(talk['end'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)

            # Skip past talks
            if end_time < current_time:
                continue

            talk['unmodified_start'] = talk['start']
            talk['unmodified_end'] = talk['end']

            day_name = start_time.strftime('%A')
            talk['start'] = start_time.strftime(f'{day_name} %I:%M %p ')
            talk['end'] = end_time.strftime(f' {day_name} %I:%M %p ')

            duration = end_time - start_time
            duration_parts = []
            duration_hours = duration.seconds // 3600
            duration_minutes = (duration.seconds % 3600) // 60
            if duration_hours > 0:
                duration_parts.append(f'{duration_hours} hour')
            if duration_minutes > 0:
                duration_parts.append(f'{duration_minutes} minutes')
            talk['duration'] = ' '.join(duration_parts) if duration_parts else '0 minutes'

            if current_time >= start_time and current_time <= end_time:
                in_progress_talks.append(talk)
            elif current_time < start_time:
                upcoming_talks.append(talk)

    if text:
        matching_talks = in_progress_talks + upcoming_talks[:10]
    else:
        matching_talks = in_progress_talks + upcoming_talks

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

    matching_talks = get_talk_details_by_text(data, text=text, current_time=datetime.now(pytz.utc) + timedelta(hours=2))
    print(json.dumps(matching_talks, indent=4))

if __name__ == '__main__':
    main()
