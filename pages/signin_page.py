import streamlit as st
import sqlite3
import datetime

DATABASE_FILE = 'learning_platform.db'

def get_or_create_user(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        user_id = existing_user[0]
    else:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        user_id = cursor.lastrowid
        conn.commit()
    
    conn.close()
    
    return user_id

def get_user_info(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user_info = cursor.fetchone()
    
    conn.close()

    
    return user_info[0] if user_info else None

# Function to get the last learned day for a user
def get_last_learned_date(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    c.execute("SELECT MAX(DATE(timestamp)) FROM learning_records WHERE user_id = ?", (user_id,))
    last_learned_date = c.fetchone()[0]
    
    conn.close()
    
    return last_learned_date

def days_since_last_learned(last_learned_date):
    if last_learned_date:
        today = st.session_state['current_date']
        last_learned = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d").date()  # Convert to datetime.date
        delta = today - last_learned
        return delta.days
    return None

def sign_in_page():
    st.title("Sign In")

    username = st.text_input("Enter your username", key="username_input")
    
    if 'new_user' not in st.session_state:
        st.session_state.new_user = True

    if username:
        user_id = get_or_create_user(username)
        st.session_state['user_id'] = user_id
        st.session_state['last_username'] = username
        st.session_state['current_date'] = datetime.date.today()

        # Check if the user is returning or new
        last_learned_day = get_last_learned_date(user_id)  # Retrieve last_learned_day
        if last_learned_day:
            last_learned_date = get_last_learned_date(user_id)
            days_ago = days_since_last_learned(last_learned_date)
            st.write(f"Welcome back, {username}! 😊")
            st.write(f"The last time you learned was {days_ago} days ago on Day {last_learned_day}.")
            st.write("Click below to continue from where you left off.")
            if st.button("Continue Learning"):
                st.session_state['selected_day'] = last_learned_day
                st.session_state.new_user = False
        else:
            st.write(f"Hi, {username}, welcome to the Learn Shabbos in Just 3 Minutes a Day App!")
            st.write("Click below to start learning from Day 1.")
            if st.button("Start Learning"):
                st.session_state['selected_day'] = 1
                st.session_state.new_user = False

if __name__ == "__main__":
    st.session_state['user_id'] = None
    sign_in_page()