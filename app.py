import streamlit as st
from datetime import datetime, timedelta
import pytz
from parser_backend import get_talk_details_by_text
import json

neon_color = "#FF1493"

@st.cache_data
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    current_time = datetime.now(pytz.utc) + timedelta(hours=2)

    # //fake current timed
    current_time = datetime.strptime("2023-08-15T18:00:00+02:00", "%Y-%m-%dT%H:%M:%S%z") + timedelta(hours=2)

    st.title("Camp Talks")
    #subheader with current time
    st.markdown(f"<h2 style='font-weight: bold; font-size: 150%;'>Current Time: {current_time.strftime('%A %m %d %I:%M %p')}</h2>", unsafe_allow_html=True)

    # Load data from JSON file
    data = load_data("cccamp.json")

    # User input for text search
    text_to_search = st.text_input("Search for talks by title, abstract, track or speakers:")

    # Get matching talks
    matching_talks = get_talk_details_by_text(data, text_to_search, current_time)


    in_progress_displayed = False
    upcoming_displayed = False

    for idx, talk in enumerate(matching_talks):
        title = talk["title"]
        
        if talk["speakers"]:
            # st.write(f"**Speakers:** {', '.join(talk['speakers'])}")
            speakers = ", ".join(talk["speakers"]) if talk["speakers"] else "N/A"

        room = talk["room"]

        # Skip talks with "Lunch" in the title that are not in room 5834
        if "Lunch" in title and room != "Milliways":
            continue

        start_time = datetime.strptime(
            talk["unmodified_start"], "%Y-%m-%dT%H:%M:%S%z"
        ) + timedelta(hours=2)
        end_time = datetime.strptime(
            talk["unmodified_end"], "%Y-%m-%dT%H:%M:%S%z"
        ) + timedelta(hours=2)

        # title_html = f"<h2 style='font-weight: bold; font-size: 150%; display: inline;'>{title}</h2><h4 style='display: inline; font-size: 125%;'> ({speakers})</h4>"
        
        title_html = f"<div style='display: flex; align-items: baseline;'><h2 style='font-weight: bold; font-size: 150%; margin-right: 10px;'>{title}</h2><span style='font-size: 125%;'>({speakers})</span></div>"

        if current_time >= start_time and current_time <= end_time:
            if not in_progress_displayed:
                st.markdown("<h1 style='font-size: 200%; color: limegreen;'>in Progress</h1>", unsafe_allow_html=True)
                in_progress_displayed = True
            st.markdown(title_html, unsafe_allow_html=True)
        else:
            if not upcoming_displayed:
                st.markdown("<h1 style='font-size: 200%; color: limegreen;'>Upcoming</h1>", unsafe_allow_html=True)
                upcoming_displayed = True
            st.markdown(title_html, unsafe_allow_html=True)



        st.markdown(f"<div style='display: flex; justify-content: space-between;'><span style='color: white;'>{talk['start']},  {talk['duration']}</span></div>", unsafe_allow_html=True)


        abstract = talk.get("abstract")
        if abstract:
            words = abstract.split()
            split_num = 40
            abstract_preview = " ".join(words[:split_num])
            abstract_rest = " ".join(words[split_num:])
            if len(words) > split_num:
                with st.expander(f"{abstract_preview}..."):
                    st.write(f"{abstract_rest}")
            else:
                st.write(f"**Abstract:** {abstract}")

        track = talk.get("track")
        room = talk["room"]

        # Only display the room if it's not the same as the track
        if room != track:
            talk['room'] = ''

        if track:
            st.markdown(f"<div style='display: flex; justify-content: space-between;'><div <span style='color: white;'>{talk['track']}</span></div><div>{talk['room']}</div></div>", unsafe_allow_html=True)

        st.write("---")


if __name__ == "__main__":
    main()
