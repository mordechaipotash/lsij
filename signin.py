import streamlit as st
import sqlite3
import datetime
import app_state  # Import the app_state module

# Constants for database file path
DATABASE_FILE = 'database.db'

# Function to get user information
def get_user_info(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT username, total_value, learned_days_count, udnum FROM users INNER JOIN user_data ON users.user_id = user_data.user_id WHERE users.user_id = ?", (user_id,))
    user_info = cursor.fetchone()

    conn.close()

    return user_info

# Function to get the last learned date for a user
def get_last_learned_date(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(DATE(login_time)) FROM login_history WHERE user_id = ?", (user_id,))
    last_learned_date = cursor.fetchone()[0]

    conn.close()

    return last_learned_date

# Function to calculate days since the last learned date
def days_since_last_learned(last_learned_date):
    if last_learned_date:
        today = datetime.date.today()
        last_learned = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d").date()
        delta = today - last_learned
        return delta.days
    return None

# Initialize the session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Sign In'

# Function to display the sign-in page
def signin_page():
    st.title("Sign In")

    if st.session_state.current_page == 'Sign In':
        username = st.text_input("Enter your username", key="username_input")

        if st.button("Sign In"):
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            # Check if the user credentials are correct
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()

            if user_id:
                user_id = user_id[0]
                st.session_state.user_id = user_id
                st.session_state.username = username  # Initialize the username in session state

                # Record the login time in the login_history table
                cursor.execute("INSERT INTO login_history (user_id) VALUES (?)", (user_id,))
                conn.commit()
                conn.close()

                # Retrieve the most recent day learned from user_data table
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()

                cursor.execute("SELECT MAX(day) FROM user_data WHERE user_id = ?", (user_id,))
                max_day = cursor.fetchone()[0]
                conn.close()

                if max_day:
                    st.write(f"Welcome back, {username}! 😊")
                    st.write(f"You are on day {max_day} of learning.")
                    button_label = "Continue Learning"
                else:
                    st.write(f"Welcome, {username}! 😊")
                    st.write("You are starting your learning journey on day 1.")
                    button_label = "Start Learning"

                st.write("Click below to begin or continue learning.")
                if st.button(button_label):
                    st.session_state.current_page = 'Learn'
            else:
                st.error("Invalid username. Please try again.")
