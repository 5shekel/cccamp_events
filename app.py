import streamlit as st
from datetime import datetime, timedelta, timezone

current_time = datetime.now(tz=timezone.utc) + timedelta(hours=2)

from parser_backend import get_talk_details_by_text
import json

def main():
    st.title('Conference Talks')

    # Load data from JSON file
    with open('cccamp.json', 'r') as file:
        data = json.load(file)

    # User input for text search
    text_to_search = st.text_input("Search for talks by title, abstract, or speakers:")

    # Get matching talks
    matching_talks = get_talk_details_by_text(data, text_to_search)

    current_time = datetime.now(tz=timezone.utc) + timedelta(hours=2)

    in_progress_displayed = False
    upcoming_displayed = False

    for idx, talk in enumerate(matching_talks):
        start_time = datetime.strptime(talk['unmodified_start'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)
        end_time = datetime.strptime(talk['unmodified_end'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)

        if current_time >= start_time and current_time <= end_time:
            if not in_progress_displayed:
                st.subheader('In Progress Talks')
                in_progress_displayed = True
            st.markdown(f"**{talk['title']}**", unsafe_allow_html=True)
        else:
            if not upcoming_displayed:
                st.subheader('Upcoming Talks')
                upcoming_displayed = True
            st.markdown(f"**{talk['title']}**", unsafe_allow_html=True)

        abstract = talk.get('abstract')
        if abstract:
            st.write(f"**Abstract:** {abstract}")

        if talk['speakers']:
            st.write(f"**Speakers:** {', '.join(talk['speakers'])}")

        track = talk.get('track')
        if track:
            st.write(f"**Track:** {talk['track']}")
        st.write(f"**Room:** {talk['room']}")
        st.write(f"**Start Time:** {talk['start']}")
        st.write(f"**Duration:** {talk['duration']}")
        st.write("---")

if __name__ == '__main__':
    main()
