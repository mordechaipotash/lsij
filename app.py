import streamlit as st
import pandas as pd
import sqlite3
import datetime

# Initialize Streamlit page configuration
st.set_page_config(page_title="Learning Platform", layout="wide")
st.markdown(
    """
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    }
    p {
        font-size: 20px;
        color: #121212;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Define constants
DATABASE_FILE = 'learning_platform.db'
CSV_FILE = 'old_ls3.csv'

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    # Create the users table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT)''')
    
    # Create the learning_records table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS learning_records
                 (user_id INTEGER, day INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(user_id, day))''')
    
    conn.commit()
    conn.close()

# Function to create or retrieve a user
def get_or_create_user(username):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    # Check if the user already exists
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()
    
    if existing_user:
        user_id = existing_user[0]
    else:
        # Insert the new user
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        user_id = c.lastrowid
        conn.commit()
    
    conn.close()
    
    return user_id

# Function to record a learned day for a user
def record_learned_day(user_id, day):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    c.execute("INSERT INTO learning_records (user_id, day) VALUES (?, ?)", (user_id, day))
    conn.commit()
    conn.close()

# Function to get the learned days with timestamps for a user
def get_learned_days(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    c.execute("SELECT day, MAX(timestamp) FROM learning_records WHERE user_id = ? GROUP BY day", (user_id,))
    learned_records = c.fetchall()
    learned_days = {day: timestamp for day, timestamp in learned_records}
    
    conn.close()
    
    return learned_days

# Function to get the user information
def get_user_info(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user_info = c.fetchone()
    
    conn.close()
    
    return user_info[0] if user_info else None

# Function to calculate the days since last learned
def days_since_last_learned(last_learned_date):
    if last_learned_date:
        today = datetime.datetime.now()
        last_learned = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d %H:%M:%S")
        delta = today - last_learned
        return delta.days
    return None

# Function to display the main content of the day
def display_content_for_day(selected_day, learned_days, df, user_id):
    selected_day = int(''.join(filter(str.isdigit, str(selected_day))))
    
    if selected_day < 1 or selected_day > len(df):
        st.error("Invalid day selection.")
        return

    day_data = df[df['Day'] == f'Day {selected_day}']

    if day_data.empty:
        st.error("No data available for this day.")
        return

    day_data = day_data.iloc[0]

    
    if selected_day in learned_days:
        days_ago = days_since_last_learned(learned_days[selected_day])
        st.markdown(f"<h2 style='text-align: center; color: darkblue;'>{day_data['Title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: green;'>Last Learned {days_ago} days ago</h4>", unsafe_allow_html=True)
    else:
        mark_button = st.button('Mark Day as Learned', key="mark_button", on_click=mark_day_as_learned, args=(learned_days, selected_day, user_id))
        if mark_button:
            mark_day_as_learned(learned_days, selected_day, user_id)
    
    for i in range(1, 10):
        heading_key = f'Heading{i}'
        paragraph_key = f'Paragraph{i}'
        if pd.notnull(day_data[heading_key]) and pd.notnull(day_data[paragraph_key]):
            # Use st.subheader for headings
            st.subheader(day_data[heading_key])
            st.markdown(day_data[paragraph_key], unsafe_allow_html=True)  # Keep paragraph text as-is


# Function to mark a day as learned
def mark_day_as_learned(learned_days, selected_day, user_id):
    if selected_day not in learned_days:
        record_learned_day(user_id, selected_day)

# Function to calculate progress
def calculate_progress(learned_days):
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    days_learned_this_week = sum(1 for day, timestamp in learned_days.items() if pd.to_datetime(timestamp) >= start_of_week)
    total_days_to_learn = 420  # Change this to the total number of days you want to learn
    days_to_go = total_days_to_learn - len(learned_days)
    days_learned_this_month = sum(1 for day, timestamp in learned_days.items() if pd.to_datetime(timestamp) >= start_of_month)

    # Calculate percentage change between this week and last week
    last_week_start = start_of_week - datetime.timedelta(days=7)
    days_learned_last_week = sum(1 for day, timestamp in learned_days.items() if start_of_week > pd.to_datetime(timestamp) >= last_week_start)
    percentage_change = ((days_learned_this_week - days_learned_last_week) / days_learned_last_week) * 100 if days_learned_last_week != 0 else 0

    return days_learned_this_week, total_days_to_learn, days_to_go, days_learned_this_month, percentage_change

# Main function for your Streamlit app
def main():
    initialize_db()
    
    username = st.text_input("Enter your username", key="username_input")
    user_id = st.session_state.get('user_id')
    
    if username:
        if user_id is None or st.session_state.get('last_username') != username:
            user_id = get_or_create_user(username)
            st.session_state['user_id'] = user_id
            st.session_state['last_username'] = username  # Store the last username to detect changes

    signed_in_username = get_user_info(user_id)
    if signed_in_username:
        st.write(f"Signed in as: {signed_in_username}")

    # Load the data from the CSV file
    df = pd.read_csv(CSV_FILE)

    # Get the learned days with timestamps for the user
    learned_days_with_timestamp = get_learned_days(user_id)

    # Calculate progress
    days_learned_this_week, total_days_to_learn, days_to_go, days_learned_this_month, percentage_change = calculate_progress(learned_days_with_timestamp)

    # Create a custom CSS class for styling the progress bar
    st.markdown(
        """
        <style>
        .progress-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
            margin-bottom: 20px;
        }
        .progress-bar {
            flex: 1;
            height: 20px;
            border-radius: 5px;
        }
        .progress-label {
            margin-right: 10px;
        }
        .progress-icon {
            font-size: 24px;
            margin-right: 10px;
        }
        .percentage-change {
            font-size: 20px;
            color: {"green" if percentage_change >= 0 else "red"};
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display the progress bar
    st.markdown(
        f"""
        <div class="progress-container">
            <div class="progress-label">
                <span class="progress-icon"></span>Total Days Learned: {len(learned_days_with_timestamp)}/{total_days_to_learn}
            </div>
            <div class="progress-label">
                <span class="progress-icon"></span>Total Days to Go: {days_to_go}
            </div>
        </div>
        <div class="progress-container">
            <div class="progress-label">
                <span class="progress-icon">📆</span>Days Learned This Month: {days_learned_this_month}
            </div>
            <div class="progress-label">
                <span class="percentage-change">{percentage_change:.2f}% {"" if percentage_change >= 0 else "▼"}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Get the most recent timestamp from learned days
    most_recent_timestamp = max(learned_days_with_timestamp.values(), default=None)

    # Get the day(s) with the most recent timestamp
    most_recent_learned_days = [day for day, timestamp in learned_days_with_timestamp.items() if timestamp == most_recent_timestamp]

    # Get the earliest day that the user has not learned
    earliest_not_learned_day = 1
    while earliest_not_learned_day in learned_days_with_timestamp:
        earliest_not_learned_day += 1

    # Initialize selected_day with the most recent learned day or the earliest not learned day
    selected_day = st.session_state.get('selected_day')
    if selected_day is None:
        selected_day = most_recent_learned_days[0] if most_recent_learned_days else earliest_not_learned_day
        st.session_state['selected_day'] = selected_day

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        prev_button = st.button('⬅️ Prev', key="prev_button")
        if prev_button:
            st.session_state['selected_day'] -= 1
            if st.session_state['selected_day'] < 1:
                st.session_state['selected_day'] = len(df)

    with col2:
        selected_day = st.session_state['selected_day']
        st.markdown(f"<h1 style='text-align: center;'>Day {selected_day}</h1>", unsafe_allow_html=True)

    with col3:
        next_button = st.button('Next ➡️', key="next_button")
        if next_button:
            st.session_state['selected_day'] += 1
            if st.session_state['selected_day'] > len(df):
                st.session_state['selected_day'] = 1

    st.write("\n\n")  # Add spacing between buttons and day display

    display_content_for_day(selected_day, learned_days_with_timestamp, df, user_id)

if __name__ == "__main__":
    main()