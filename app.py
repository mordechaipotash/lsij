import streamlit as st
from signin import signin_page, get_or_create_user
from learn import daily_content_page
from progress import progress_page
import sqlite3

# Constants for database file path
DATABASE_FILE = 'database.db'

# Set up the SQLite database
def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create the tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id INTEGER PRIMARY KEY,
            total_value INTEGER,
            learned_days_count INTEGER,
            udnum TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
            user_id INTEGER,
            login_time DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()

def main():
    # Initialize the database
    initialize_db()

    # Set the page title and layout
    st.title("Learn Shabbos in Just 3 Minutes a Day")

    # Use a selectbox to navigate between pages
    selected_page = st.selectbox("Select a Page", ["Sign In", "Learn", "My Progress"])

    # Display the selected page
    if selected_page == "Sign In":
        signin_page()
    elif selected_page == "Learn":
        daily_content_page()
    elif selected_page == "My Progress":
        progress_page()

if __name__ == "__main__":
    main()
