import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random

# Constants for database and CSV file paths from design code
DATABASE_FILE = 'learning_platform.db'
CSV_FILE = 'old_ls3.csv'

def get_learned_days(user_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT day, MAX(timestamp) FROM learning_records WHERE user_id = ? GROUP BY day", (user_id,))
        learned_records = c.fetchall()
    return {day: timestamp for day, timestamp in learned_records}

def mark_day_as_learned(user_id, day):
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO learning_records (user_id, day) VALUES (?, ?)", (user_id, day))
        conn.commit()

def apply_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: grey;
        }
        /* Additional CSS styles from design code */
        </style>
        """,
        unsafe_allow_html=True
    )

def display_content_for_day(selected_day, learned_days, df, user_id):
    # Set the background color for the entire Streamlit app
    st.markdown(
        f"""
        <style>
        body {{
            background-color: grey;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    if selected_day < 1 or selected_day > len(df):
        st.error("Invalid day selection.")
        return
    
    # Content display logic
    day_data = df.loc[df['Day'] == f'Day {selected_day}'].iloc[0]
    title = day_data['Title']
    
    # Initialize days_ago with a default value
    days_ago = None
    
    # Check if the day has been learned
    if selected_day in learned_days:
        last_learned_date = learned_days[selected_day]
        last_learned_datetime = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d %H:%M:%S")
        days_ago = (datetime.datetime.now() - last_learned_datetime).days
    
    # Display the button for "Mark Day as Learned" only when the day has not been learned
    if days_ago is None:
        if st.button('Mark Day as Learned', key=f"mark_{selected_day}"):
            mark_day_as_learned(user_id, selected_day)
            st.rerun()
    
    # Apply CSS styling to create a thin black circular border and set a different soothing background color for each pair
    st.markdown(
        f"<div style='border: 1px solid grey; border-radius: 20px; padding: 0.5px; background-color: lightgrey;'>"
        f"<h1 style='text-align: center; color: blue;'>{title}</h1>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    # Define a list of soothing background colors
    background_colors = ["#FFF8E1", "#E0F7FA", "#F3E5F5", "#E8F5E9", "#F1F8E9", "#FCE4EC", "#E6EE9C", "#FFD180", "#B2DFDB"]
    
    # Shuffle the background colors randomly
    random.shuffle(background_colors)
    
    # Content headings and paragraphs with soothing colors and a 10px gap between pairs
    for i in range(1, 10):
        heading_key = f'Heading{i}'
        paragraph_key = f'Paragraph{i}'
        if pd.notnull(day_data[heading_key]) and pd.notnull(day_data[paragraph_key]):
            # Use modulo to cycle through the soothing background colors
            background_color = background_colors[i % len(background_colors)]
            
            # Display Day number, title, and mark as read/days ago
            st.markdown(
                f"<div style='border: 1px solid grey; border-radius: 20px; padding: 10px; margin-bottom: 10px; background-color: {background_color};'>"
                f"<div style='display: flex; justify-content: space-between;'>"
                f"<p style='color: red; font-weight: bold;'>Day {selected_day}</p>"
                f"<p style='color: green;'>{'Learned ' + str(days_ago) + ' days ago' if days_ago is not None else ''}</p>"
                f"</div>"
                f"<h3 style='color: darkblue;'>{day_data[heading_key]}</h3>"
                f"<p style='font-size: 20px;'>{day_data[paragraph_key]}</p>"
                f"</div>",
                unsafe_allow_html=True
            )

def daily_content_page():
    apply_custom_css()
    if 'user_id' not in st.session_state:
        st.error("You need to log in to view this page.")
        return

    user_id = st.session_state['user_id']
    df = pd.read_csv(CSV_FILE)
    learned_days = get_learned_days(user_id)
    
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = 1

    selected_day = st.session_state.selected_day
    
    # Move the "Previous Day" and "Next Day" buttons to the top
    col1, col2 = st.columns(2)
    with col1:
        if selected_day > 1 and st.button('Previous Day'):
            st.session_state.selected_day -= 1
            st.rerun()

    with col2:
        if selected_day < len(df) and st.button('Next Day'):
            st.session_state.selected_day += 1
            st.rerun()
    
    # Display the content for the selected day
    display_content_for_day(selected_day, learned_days, df, user_id)

if __name__ == "__main__":
    st.session_state['user_id'] = 1  # For testing, replace with dynamic login session management in production
    daily_content_page()
