import streamlit as st
import sqlite3
import datetime
import app_state

# Constants for database file path
DATABASE_FILE = 'database.db'

# Function to get user information
def get_user_info(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT username, udnum FROM users INNER JOIN user_data ON users.user_id = user_data.user_id WHERE users.user_id = ?", (user_id,))
    user_info = cursor.fetchone()

    conn.close()

    return user_info

# Function to get learned days for a user
def get_learned_days(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT DATE(login_time)) FROM login_history WHERE user_id = ?", (user_id,))
    learned_days_count = cursor.fetchone()[0]

    conn.close()

    return learned_days_count

# Function to calculate days since the last learned date
def days_since_last_learned(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(DATE(login_time)) FROM login_history WHERE user_id = ?", (user_id,))
    last_learned_date = cursor.fetchone()[0]

    conn.close()

    if last_learned_date:
        today = datetime.date.today()
        last_learned = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d").date()
        delta = today - last_learned
        return delta.days
    return None

# Function to display the progress page
def progress_page():
    st.title("My Progress")

    user_id = app_state.app_state.user_id
    user_info = get_user_info(user_id)

    if user_info:
        username, total_value, learned_days_count, udnum = user_info
        st.write(f"Welcome, {username}!")

        st.write(f"Total Value: {total_value}")
        st.write(f"Learned Days Count: {learned_days_count}")
        st.write(f"User Data Number: {udnum}")

        learned_days = get_learned_days(user_id)
        last_learned_day = days_since_last_learned(user_id)

        if learned_days is not None:
            st.write(f"Total Learned Days: {learned_days}")
            st.write(f"Days Since Last Learned: {last_learned_day}")
        else:
            st.warning("No learned days found.")

        st.write("You can add progress-related content and functionality here.")
    else:
        st.warning("User information not found.")

# Function to return to the home page
def return_to_home():
    st.button("Return to Home", key="return_to_home")
