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
        if 'abstract' in talk:
            st.write(f"**Abstract:** {talk['abstract']}")
        
        if 'speakers' in talk:
            st.write(f"**Speakers:** {', '.join(talk['speakers'])}")
        if 'track' in talk:
            st.write(f"**Track:** {talk['track']}")
            
        st.write(f"**Room:** {talk['room']}")
        st.write(f"**Start Time:** {talk['start']}")
        st.write(f"**Duration:** {talk['duration']}")
        
        st.write("---")

if __name__ == '__main__':
    main()
