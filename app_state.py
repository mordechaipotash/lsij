import sqlite3

# Constants for database file path
DATABASE_FILE = 'database.db'

# Function to get the learned days count for a user
def get_learned_days_count(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT learned_days_count FROM user_data WHERE user_id = ?", (user_id,))
    learned_days_count = cursor.fetchone()[0]

    conn.close()

    return learned_days_count
# Function to initialize the session state
def initialize():
    # Add your initialization logic here
    pass