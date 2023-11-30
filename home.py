import streamlit as st
import sqlite3
import datetime

# Constants for database file path
DATABASE_FILE = 'database.db'

# Initialize the database if it doesn't exist
def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the user_data table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id INTEGER PRIMARY KEY,
            total_value INTEGER,
            learned_days_count INTEGER,
            udnum TEXT
        )
    ''')

    # Create the login_history table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
            user_id INTEGER,
            login_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Function to get or create a user
def get_or_create_user(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Check if the user already exists
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

# Function to display the login page
def login_page():
    st.title("Sign In")

    username = st.text_input("Enter your username", key="username_input")

    if username:
        user_id = get_or_create_user(username)
        st.session_state['user_id'] = user_id
        st.session_state['last_username'] = username

        # Record the login time in the login_history table
        record_login_history(user_id)

        st.write(f"Welcome back, {username}! 😊")
        st.write("Click below to continue.")
        if st.button("Continue"):
            st.session_state['selected_page'] = 'main'
    elif st.button("Create New Account"):
        st.session_state['selected_page'] = 'create_account'

    if st.button("Return to Home"):
        st.session_state['selected_page'] = 'home'

# Function to record login history
def record_login_history(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO login_history (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

# Function to create a new account
def create_account_page():
    st.title("Create New Account")

    new_username = st.text_input("Choose a username", key="new_username_input")

    if new_username:
        user_id = get_or_create_user(new_username)
        st.session_state['user_id'] = user_id
        st.session_state['last_username'] = new_username

        # Record the login time in the login_history table
        record_login_history(user_id)

        st.write(f"Account created successfully, {new_username}! 😊")
        st.write("Click below to continue.")
        if st.button("Continue"):
            st.session_state['selected_page'] = 'main'

    if st.button("Return to Home"):
        st.session_state['selected_page'] = 'home'

# Define your main page after logging in
def main_page():
    st.title("Main Page")
    st.write("Welcome to the main page after logging in.")
    st.write("You can add content and functionality here.")

# Function to return to the home page
def return_to_home():
    st.button("Return to Home", key="return_to_home")

# Define your Streamlit app
def main():
    st.set_page_config(
        page_title="Learning Platform",
        layout="wide",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None,
            'Hide menu': True,  # This hides the hamburger menu completely
        }
    )

    # Initialize the database
    initialize_db()

    if 'selected_page' not in st.session_state:
        st.session_state['selected_page'] = 'home'

    if st.session_state['selected_page'] == 'home':
        home_page()
    elif st.session_state['selected_page'] == 'login':
        login_page()
    elif st.session_state['selected_page'] == 'create_account':
        create_account_page()
    elif st.session_state['selected_page'] == 'main':
        main_page()

if __name__ == "__main__":
    main()
