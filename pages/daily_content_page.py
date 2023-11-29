import streamlit as st
import pandas as pd
import sqlite3
import datetime

# Constants for database and CSV file paths
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

def display_content_for_day(selected_day, learned_days, df, user_id):
    if selected_day < 1 or selected_day > len(df):
        st.error("Invalid day selection.")
        return
    
    # Content display logic
    day_data = df.loc[df['Day'] == f'Day {selected_day}'].iloc[0]
    title = day_data['Title']
    st.markdown(f"<h2 style='text-align: center; color: darkblue;'>{title}</h2>", unsafe_allow_html=True)
    
    # Check if the day has been learned
    if selected_day in learned_days:
        last_learned_date = learned_days[selected_day]
        last_learned_datetime = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d %H:%M:%S")
        days_ago = (datetime.datetime.now() - last_learned_datetime).days
        st.markdown(f"<h4 style='text-align: center; color: green;'>Learned {days_ago} days ago</h4>", unsafe_allow_html=True)
    else:
        if st.button('Mark Day as Learned', key=f"mark_{selected_day}"):
            mark_day_as_learned(user_id, selected_day)
            st.experimental_rerun()
    
    # Content headings and paragraphs
    for i in range(1, 10):
        heading_key = f'Heading{i}'
        paragraph_key = f'Paragraph{i}'
        if pd.notnull(day_data[heading_key]) and pd.notnull(day_data[paragraph_key]):
            # Add light blue background color to paragraph text
            st.subheader(day_data[heading_key])
            st.markdown(f"<p style='font-size: 20px; background-color: lightblue;'>{day_data[paragraph_key]}</p>", unsafe_allow_html=True)

def daily_content_page():
    # Check if the user is logged in
    if 'user_id' not in st.session_state:
        st.error("You need to log in to view this page.")
        return
    
    user_id = st.session_state['user_id']
    
    st.title("Daily Learning Content")

    df = pd.read_csv(CSV_FILE)
    learned_days = get_learned_days(user_id)
    
    # Ensure selected_day in the session state
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = 1

    # Layout for Previous, Day indicator, and Next buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button('⬅️ Previous'):
            st.session_state.selected_day = max(1, st.session_state.selected_day - 1)
    
    with col2:
        # Centering Day X in the middle column
        st.write(f"<h3 style='text-align: center;'>Day {st.session_state.selected_day}</h3>", unsafe_allow_html=True)

    with col3:
        if st.button('Next ➡️'):
            st.session_state.selected_day = min(len(df), st.session_state.selected_day + 1)
    
    # Display the content for the selected day
    display_content_for_day(st.session_state.selected_day, learned_days, df, user_id)

# Standalone testing or called from main.py
if __name__ == "__main__":
    # If running this file as a standalone app, assume the user is logged in for testing purposes
    st.session_state['user_id'] = 1  # For testing, replace with dynamic login session management
    daily_content_page()
