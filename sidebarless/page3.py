import streamlit as st

# Function to render Day 3 page
def render_day3_page():
    st.title('Day 3')
    st.write('Content for Day 3 goes here.')

    # Button to return to the main page
    if st.button('Back to Main'):
        st.session_state.current_page = 'Main Page'
