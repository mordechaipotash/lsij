import streamlit as st
from pages import signin_page  # Update the import statement
from pages import progress_page
from pages import daily_content_page

# The very first command to set page configuration
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

# Placeholder functions - replace with actual database and user management logic
def initialize_db():
    # Initialize your database or perform any setup here
    pass

def get_or_create_user(username):
    # Check if the user exists in the database, and create if not
    # Return the user's ID
    pass

def record_learned_day(user_id, day):
    # Record that the user learned a specific day
    pass

def get_learned_days(user_id):
    # Retrieve the days that the user has learned
    pass

# Main function for the Streamlit app
def main():
    initialize_db()
    
    username = st.sidebar.text_input("Enter your username", key="username_input")
    user_id = st.session_state.get('user_id')
    
    if username:
        if user_id is None or st.session_state.get('last_username') != username:
            user_id = get_or_create_user(username)
            st.session_state['user_id'] = user_id
            st.session_state['last_username'] = username  # Store the last username to detect changes

    signed_in_username = username

    st.sidebar.write(f"Signed in as: {signed_in_username}")

    # Check if the user is signed in
    if signed_in_username:
        st.title("Learning Platform")
        
        # Here you can add widgets and code for your learning page, such as:
        # - A dropdown to select a day
        # - A button to mark the selected day as learned
        # - Displaying learned days for the user
        
        selected_day = st.selectbox("Select a day:", range(1, 31))
        if st.button("Mark Day as Learned"):
            record_learned_day(user_id, selected_day)
        
        learned_days = get_learned_days(user_id)
        st.write(f"Learned Days: {list(learned_days.keys())}")
        
    else:
        st.warning("Please enter a username to sign in.")

if __name__ == "__main__":
    main()
