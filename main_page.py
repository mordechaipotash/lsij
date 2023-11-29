# pages/main_page.py

import streamlit as st
from .signin_page import signin_page
from .progress_page import progress_page
from .daily_content_page import daily_content_page

st.set_page_config(page_title="Learning Platform", layout="wide")

# Hide the Streamlit sidebar and hamburger menu
st.markdown(
    """
    <style>
        /* This CSS hides the sidebar */
        .css-18e3th9 {
            display: none;
        }

        /* This CSS hides the hamburger menu in the top right */
        header .css-1lcbmhc.e1fqkh3o3 {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main_page():
    # Check if the user is signed in, you can use the user profile or authentication logic here

    # Check if the user is signed in (You can use your own authentication logic)
    if 'user_id' not in st.session_state:
        st.error("Please sign in to view progress.")
        return
    
    user_id = st.session_state['user_id']

    # Retrieve the learned days and calculate progress
    learned_days = get_learned_days(user_id)
    progress_stats = calculate_progress(learned_days)

    # Display progress metrics and chart
    st.title("Learning Progress Dashboard")

# This check is necessary to prevent this script from running when imported
if __name__ == "__main__":
    main_page()
