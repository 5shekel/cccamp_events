import streamlit as st
import json
from datetime import datetime, timedelta

# Importing the provided parser function
from parser_backend import get_talk_details_by_text

def main():
    st.title("Conference Talk Search")

    # Load the JSON file
    json_file_path = "cccamp.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Get user input for text to search
    text_to_search = st.text_input("Enter text to search in title, abstract, and speakers:")
    
    # Get matching talks using the backend parser function
    matching_talks = get_talk_details_by_text(data, text_to_search)

    if not matching_talks:
        st.warning("No matching talks found.")
        return

    st.success(f"Found {len(matching_talks)} matching talks.")
    
    # Display matching talks
    for idx, talk in enumerate(matching_talks):
        st.subheader(f"{talk['title']}")
        st.write(f"**Abstract:** {talk['abstract']}")
        
        if talk['speakers']:
            st.write(f"**Speakers:** {', '.join(talk['speakers'])}")
        
        st.write(f"**Track:** {talk['track']}")
        st.write(f"**Room:** {talk['room']}")
        
        # Adjusted time format with UTC+2 offset
        start_time = datetime.strptime(talk['start'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)
        end_time = datetime.strptime(talk['end'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)

        # Replace day of the week with its literal name
        day_name = start_time.strftime('%A')
        formatted_start_time = start_time.strftime(f'{day_name} %I:%M %p')
        formatted_end_time = end_time.strftime(f'{day_name} %I:%M %p')

        # Calculate the duration
        duration = end_time - start_time
        duration_hours = duration.seconds // 3600
        duration_minutes = (duration.seconds % 3600) // 60
        
        st.write(f"**Start Time:** {formatted_start_time}")
        st.write(f"**End Time:** {formatted_end_time}")
        st.write(f"**Duration:** {duration_hours} hours {duration_minutes} minutes")
        
        st.write("---")

if __name__ == '__main__':
    main()
