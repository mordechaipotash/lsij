import streamlit as st

# Function to render the "Learn a Day" page
def learn_page():
    st.title('Learn a Day')

    # Content for the "Learn a Day" page
    st.write('Welcome to the "Learn a Day" page!')
    st.write('This is where you can learn something new every day.')

    # Button to return to the main page
    if st.button('Back to Sign-in'):
        st.session_state.current_page = 'Sign In'  # Make sure to match the page name to your app's structure
