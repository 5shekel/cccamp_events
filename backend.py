
import json
import requests

def load_events(url='https://pretalx.c3voc.de/camp2023/schedule/export/schedule.json'):
    response = requests.get(url)
    content = json.loads(response.text)
    days_content = content['schedule']['conference']['days']
    events = [event for day in days_content for room, events in day['rooms'].items() for event in events]
    return events

def search_events(query, events):
    return [event for event in events if any(query.lower() in str(value).lower() for value in event.values())]

def extract_event_by_id(event_id, events):
    for event in events:
        if event['id'] == event_id:
            return event
    return None
