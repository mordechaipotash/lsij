import streamlit as st

def initialize_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'last_username' not in st.session_state:
        st.session_state.last_username = None
