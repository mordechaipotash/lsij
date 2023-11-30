import streamlit as st

# Function to render Day 2 page
def render_day2_page():
    st.title('Day 2')
    st.write('Content for Day 2 goes here.')

    # Button to return to the main page
    if st.button('Back to Main'):
        st.session_state.current_page = 'Main Page'
