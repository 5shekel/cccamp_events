import streamlit as st
from datetime import datetime, timedelta
import backend

# Title
st.title("CCC camp")

# Display a search box
search_query = st.text_input("Search for an event:", value="")

# Function to filter out past events
def filter_past_events(events):
    current_time = datetime.now().isoformat()
    return [event for event in events if event['end_date'] > current_time]

# Function to filter in-progress events
def in_progress_events(events):
    current_time = datetime.now().isoformat()
    return [event for event in events if event['date'] <= current_time < event['end_date']]

# Function to filter upcoming events
def upcoming_events(events):
    current_time = datetime.now().isoformat()
    return [event for event in events if event['date'] > current_time]

# Load all events
events = backend.load_events()

# Calculate end_date for each event and filter past events
filtered_events = []
for event in events:
    start_datetime = datetime.fromisoformat(event['date'])
    duration_hours, duration_minutes = map(int, event['duration'].split(':'))
    end_datetime = start_datetime + timedelta(hours=duration_hours, minutes=duration_minutes)
    event['end_date'] = end_datetime.isoformat()
    if event['end_date'] > datetime.now().isoformat():
        filtered_events.append(event)

# Function to display an event
def display_event(event):
    st.markdown(f"**{event['title']}**")  # Bold title
    st.write(f"{start_datetime.strftime('%A')} {start_datetime.strftime('%I%p').lstrip('0')}, {event['duration']} hours")
    st.markdown(f"{event['abstract']} [Link]({event['url']})")  # URL as a hyperlink
    st.write(event['room'])
    st.write("---")  # Horizontal line

# If a search query is entered, display only the search results
if search_query:
    # Filter the events based on the search query
    search_results = backend.search_events(search_query, filtered_events)
    
    # Display the filtered events
    st.subheader("Search Results:")
    for event in search_results:
        display_event(event)
else:
    # Subheader with current time
    st.subheader(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Subheader for in-progress events
    st.subheader("In-Progress Events:")
    for event in in_progress_events(filtered_events):
        display_event(event)

    # Subheader for upcoming events
    st.subheader("Upcoming Events:")
    for event in upcoming_events(filtered_events):
        display_event(event)
