import streamlit as st

# Function to render Sign-in page
def render_sign_in_page():
    st.title('Sign-in')

    # Display content for the Sign-in page
    st.write('This is the Sign-in page content.')

    # Button to return to the main page
    if st.button('Back to Main'):
        st.session_state.current_page = 'Main Page'
