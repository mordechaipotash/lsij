import streamlit as st
import sqlite3
import datetime
import app_state  # Import the app_state module
import pandas as pd

# Load the CSV file
df = pd.read_csv("ls3.csv")

# Constants for database file path
DATABASE_FILE = 'database.db'

# Function to mark a day as learned
def mark_day_as_learned(username, day):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    today = datetime.date.today()

    # Get the user_id (username) from the 'users' table
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()

    if user_id:
        user_id = user_id[0]

        # Insert the day learned into user_data table using 'username' as 'user_id'
        cursor.execute("INSERT INTO user_data (user_id, day, learned_timestamp) VALUES (?, ?, ?)", (user_id, day, today))
        conn.commit()

    conn.close()

# Function to get the username of the logged-in user
def get_username(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    username = cursor.fetchone()[0]

    conn.close()

    return username

def daily_content_page():
    st.title("Learn Shabbos in Just 3 Minutes a Day")

if user_id:
    user_id = user_id[0]
    st.session_state.username = username  # Initialize session_state.username with the username
    st.write("Welcome to the Daily Learning Content!")

    # Ensure selected_day in the session state
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = 1

    # Layout for Previous, Day indicator, and Next buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button('⬅️ Previous'):
            st.session_state.selected_day = max(1, st.session_state.selected_day - 1)

    with col2:
        st.write(f"<h3 style='text-align: center;'>Day {st.session_state.selected_day}</h3>", unsafe_allow_html=True)

    with col3:
        if st.button('Next ➡️'):
            st.session_state.selected_day = min(365, st.session_state.selected_day + 1)

        if 'username' in st.session_state:
    st.error("You need to log in to view this page.")
    return

    user_id = st.session_state.user_id
    username = get_username(user_id)
    
        if st.button("Mark Day as Learned"):
    mark_day_as_learned(username, st.session_state.selected_day)
    st.experimental_rerun()
    
        st.write("You can add your daily content and learning materials here.")
    
        # Content display logic
        day_data = df.loc[df['Day'] == f'Day {st.session_state.selected_day}'].iloc[0]
        title = day_data['Title']
        st.markdown(f"<h2 style='text-align: center; color: darkblue;'>{title}</h2>", unsafe_allow_html=True)
    
        # Check if the day has been learned
        if st.session_state.selected_day in learned_days:
    last_learned_date = learned_days[st.session_state.selected_day]
    last_learned_datetime = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d %H:%M:%S")
    days_ago = (datetime.datetime.now() - last_learned_datetime).days
    st.markdown(f"<h4 style='text-align: center; color: green;'>Learned {days_ago} days ago</h4>", unsafe_allow_html=True)
        else:
    if st.button('Mark Day as Learned', key=f"mark_{st.session_state.selected_day}"):
    mark_day_as_learned(user_id, st.session_state.selected_day)
    st.experimental_rerun()
    
        # Content headings and paragraphs
        for i in range(1, 10):
    heading_key = f'Heading{i}'
    paragraph_key = f'Paragraph{i}'
    if pd.notnull(day_data[heading_key]) and pd.notnull(day_data[paragraph_key]):
    # Add light blue background color to paragraph text
    st.subheader(day_data[heading_key])
    st.markdown(f"<p style='font-size: 20px; background-color: lightblue;'>{day_data[paragraph_key]}</p>", unsafe_allow_html=True)
    
    # Function to return to the home page
    def return_to_home():
        st.button("Return to Home", key="return_to_home")
    