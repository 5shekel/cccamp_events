
import json
import sys
from datetime import datetime
from bs4 import BeautifulSoup, Comment
from collections import defaultdict

def generate_id(label, content):
    id_string = f"{label}_{content}".replace(" ", "_").replace(":", "").replace("-", "").replace(".", "")
    return id_string[:100]

def main(input_json_path, input_html_path, output_html_path):
    # Read JSON Data
    with open(input_json_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Read HTML Data
    with open(input_html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

    # Extract CSS Content and Neon Colors
    css_content = soup.head.style.string
    neon_colors = {
        'body_bg': '#000000',
        'text': '#FFFFFF',
        'headers': '#FF00FF',
        'paragraph': '#00FFFF',
        'links': '#FFAA00',
        'link_hover': '#FF55AA',
        'button_bg': '#FF00FF',
        'button_hover_bg': '#FF55AA'
    }

    # Extract Talks and Transpose
    rows = soup.select('tr')
    transposed_talks = []
    for row in rows[1:]:
        cells = row.select('td')
        talk = [cell.text.strip() for cell in cells]
        transposed_talks.append(talk)

    # Headers
    headers = ["title", "abstract", "presenters", "track", "room", "duration"]

    # Map Start Times to Titles
    talk_start_times_by_title = {talk["title"] if isinstance(talk["title"], str) else talk["title"]["en"]: talk["start"] for talk in json_data["talks"]}

    # Group Talks by Day and Starting Hour
    talks_by_day_and_hour = defaultdict(lambda: defaultdict(list))
    for talk_row in transposed_talks:
        title = talk_row[0]
        start_time = talk_start_times_by_title.get(title)
        if start_time:
            start_datetime = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            start_day = start_datetime.strftime("%Y-%m-%d")
            start_hour_minute = start_datetime.strftime("%H:%M")
            if start_hour_minute == "22:00":  # Correcting 10pm to 10am
                start_hour_minute = "10:00"
            talks_by_day_and_hour[start_day][start_hour_minute].append(talk_row)

    # Create New HTML with Talks Grouped by Day and Starting Hour, Titles in 2x Size, and IDs
    new_soup_day_grouped_with_ids = BeautifulSoup("", 'html.parser')

    # Comment to Attribute Neon Futurism Style
    comment_day_grouped_with_ids = new_soup_day_grouped_with_ids.new_string("<!-- Neon Futurism Color Palette -->")
    new_soup_day_grouped_with_ids.append(comment_day_grouped_with_ids)

    # Create Head Tag
    head_tag_day_grouped_with_ids = new_soup_day_grouped_with_ids.new_tag('head')
    new_soup_day_grouped_with_ids.append(head_tag_day_grouped_with_ids)
    style_tag_day_grouped_with_ids = new_soup_day_grouped_with_ids.new_tag('style')
    style_tag_day_grouped_with_ids.string = css_content
    head_tag_day_grouped_with_ids.append(style_tag_day_grouped_with_ids)

    new_soup_day_grouped_with_ids.append(new_soup_day_grouped_with_ids.new_tag('body', style=f"background-color:{neon_colors['body_bg']}; color:{neon_colors['text']}; font-family:'Arial', sans-serif;"))
    table_day_grouped_with_ids = new_soup_day_grouped_with_ids.new_tag('table')
    new_soup_day_grouped_with_ids.body.append(table_day_grouped_with_ids)

    # Add Talks Grouped by Day and Starting Hour with IDs
    for day, talks_by_hour in talks_by_day_and_hour.items():
        # Day Title in 8x Font Size
        day_title_row = new_soup_day_grouped_with_ids.new_tag('tr', style="text-align:center; font-size:8em; color:{neon_colors['headers']};")
        table_day_grouped_with_ids.append(day_title_row)
        day_title_cell = new_soup_day_grouped_with_ids.new_tag('td')
        day_title_cell.string = day
        day_title_row.append(day_title_cell)

        # Rest of the Structure for Talks with Titles in 2x Size and IDs, Special Handling for "Lunch"
        for start_hour, talks in talks_by_hour.items():
            start_time_row = new_soup_day_grouped_with_ids.new_tag('tr', style="text-align:center; font-size:4em; color:{neon_colors['headers']};")
            table_day_grouped_with_ids.append(start_time_row)
            start_time_cell = new_soup_day_grouped_with_ids.new_tag('td')
            start_time_cell.string = start_hour
            start_time_row.append(start_time_cell)

            # Unique Consecutive Rows with Titles in 2x Size and IDs, Special Handling for "Lunch"
            previous_row_content = None
            omit_empty_rows_after_lunch = False
            for talk in talks:
                for idx, cell_content in zip(headers, talk):
                    if cell_content != previous_row_content and not (omit_empty_rows_after_lunch and cell_content == ""):
                        row = new_soup_day_grouped_with_ids.new_tag('tr', style=f"text-align:center; color:{neon_colors['paragraph']};")
                        table_day_grouped_with_ids.append(row)
                        td = new_soup_day_grouped_with_ids.new_tag('td')
                        td['id'] = generate_id(idx, cell_content)
                        td['style'] = ""
                        if idx == "title":
                            td['style'] = "font-size:2em;"
                            if cell_content.lower() == "lunch":
                                td['style'] = "font-size:6em;"
                                omit_empty_rows_after_lunch = True
                        td.string = cell_content
                        row.append(td)
                        previous_row_content = cell_content

                if not omit_empty_rows_after_lunch:
                    # Empty One-Line Grey Row Between Talks
                    empty_row = new_soup_day_grouped_with_ids.new_tag('tr', style="background-color:grey;")
                    table_day_grouped_with_ids.append(empty_row)
                    empty_td = new_soup_day_grouped_with_ids.new_tag('td')
                    empty_row.append(empty_td)

    # Apply Table Class from Original HTML
    new_table_day_grouped_with_ids = new_soup_day_grouped_with_ids.find('table')
    new_table_day_grouped_with_ids['class'] = 'table-8bit'

    # Save Updated HTML with Grouped Talks by Day and Start Times, and IDs for Each Member
    with open(output_html_path, 'w', encoding='utf-8') as file:
        file.write(str(new_soup_day_grouped_with_ids.prettify()))

    print(f"Transformed HTML file has been successfully saved to {output_html_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input.json input.html output.html")
        sys.exit(1)

    input_json_path = sys.argv[1]
    input_html_path = sys.argv[2]
    output_html_path = sys.argv[3]

    main(input_json_path, input_html_path, output_html_path)

                        td['style'] = ""
                        if idx == "title":
                            td['style'] = "font-size:2em;"
                            if cell_content.lower() == "lunch":
                                td['style'] = "font-size:6em;"
                                omit_empty_rows_after_lunch = True
                        td.string = cell_content
                        row.append(td)
                        previous_row_content = cell_content

                if not omit_empty_rows_after_lunch:
                    # Empty One-Line Grey Row Between Talks
                    empty_row = new_soup_day_grouped_with_ids.new_tag('tr', style="background-color:grey;")
                    table_day_grouped_with_ids.append(empty_row)
                    empty_td = new_soup_day_grouped_with_ids.new_tag('td')
                    empty_row.append(empty_td)

    # Apply Table Class from Original HTML
    new_table_day_grouped_with_ids = new_soup_day_grouped_with_ids.find('table')
    new_table_day_grouped_with_ids['class'] = 'table-8bit'

    # Save Updated HTML with Grouped Talks by Day and Start Times, and IDs for Each Member
    with open(output_html_path, 'w', encoding='utf-8') as file:
        file.write(str(new_soup_day_grouped_with_ids.prettify()))

    print(f"Transformed HTML file has been successfully saved to {output_html_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input.json input.html output.html")
        sys.exit(1)

    input_json_path = sys.argv[1]
    input_html_path = sys.argv[2]
    output_html_path = sys.argv[3]

    main(input_json_path, input_html_path, output_html_path)
