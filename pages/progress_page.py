import streamlit as st
import sqlite3
import pandas as pd
import datetime
import plotly.express as px

# Hide the Streamlit sidebar and hamburger menu
st.markdown(
    """
    <style>
        /* CSS to hide the sidebar and hamburger menu */
        .css-18e3th9, header .css-1lcbmhc.e1fqkh3o3 {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Constants
DATABASE_FILE = 'learning_platform.db'

def get_learned_days(user_id):
    """
    Retrieve the days on which a user has learned, along with the timestamps.
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT day, MAX(timestamp) FROM learning_records WHERE user_id = ? GROUP BY day", (user_id,))
        learned_records = c.fetchall()
    return {day: timestamp for day, timestamp in learned_records}

def calculate_progress(learned_days):
    """
    Calculate various progress metrics based on the days the user has learned.
    """
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    days_learned_this_week = sum(1 for day, timestamp in learned_days.items() if pd.to_datetime(timestamp) >= start_of_week)
    total_days_to_learn = 420  # Adjust this to match your total learning plan
    days_to_go = total_days_to_learn - len(learned_days)
    days_learned_this_month = sum(1 for day, timestamp in learned_days.items() if pd.to_datetime(timestamp) >= start_of_month)

    last_week_start = start_of_week - datetime.timedelta(days=7)
    days_learned_last_week = sum(1 for day, timestamp in learned_days.items() if start_of_week > pd.to_datetime(timestamp) >= last_week_start)
    percentage_change = ((days_learned_this_week - days_learned_last_week) / days_learned_last_week) * 100 if days_learned_last_week != 0 else 0

    return days_learned_this_week, total_days_to_learn, days_to_go, days_learned_this_month, percentage_change

def format_days_ago(last_learned_date):
    if last_learned_date:
        last_learned_datetime = datetime.datetime.strptime(last_learned_date, "%Y-%m-%d %H:%M:%S")
        days_ago = (datetime.datetime.now() - last_learned_datetime).days
        return f"Learned {days_ago} days ago"
    return ""

def progress_page():
    if 'user_id' not in st.session_state:
        st.error("Please sign in to view progress.")
        return
    
    user_id = st.session_state['user_id']

    learned_days = get_learned_days(user_id)
    progress_stats = calculate_progress(learned_days)

    st.title("Learning Progress Dashboard")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='metric-container'><h3 class='metric-label'>Total Days Learned</h3><h1 class='metric-value'>{len(learned_days)}</h1></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='metric-container'><h3 class='metric-label'>Days to Go</h3><h1 class='metric-value'>{progress_stats[2]}</h1></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div class='metric-container'><h3 class='metric-label'>Days Learned This Week</h3><h1 class='metric-value'>{progress_stats[0]}</h1></div>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown(f"<div class='metric-container'><h3 class='metric-label'>Days Learned This Month</h3><h1 class='metric-value'>{progress_stats[3]}</h1></div>", unsafe_allow_html=True)

    with col5:
        st.markdown(f"<div class='metric-container'><h3 class='metric-label'>Percentage Change From Last Week</h3><h1 class='metric-value'>{progress_stats[4]:.2f}%</h1></div>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: #1f77b4;'>Learned Days</h3>", unsafe_allow_html=True)
    st.markdown(f"<ul style='color: #1f77b4;'>", unsafe_allow_html=True)

    for day, timestamp in learned_days.items():
        formatted_date = format_days_ago(timestamp)
        st.markdown(f"<li style='font-size: 18px;'>Day {day}: {formatted_date}</li>", unsafe_allow_html=True)

    st.markdown(f"</ul>", unsafe_allow_html=True)

    # Create a pie chart for days learned vs. days to go
    fig = px.pie(
        names=["Days Learned", "Days to Go"],
        values=[len(learned_days), progress_stats[2]],
        title="Learning Progress",
        hole=0.4,
        color_discrete_sequence=["#1f77b4", "#d62728"]
    )

    fig.update_layout(
        font=dict(size=16),
        margin=dict(l=0, r=0, b=0, t=50),
        legend=dict(
            title=None,
            font=dict(size=18),
        ),
    )

    st.plotly_chart(fig)

    # Custom CSS to style the metrics grid
    st.markdown(
        """
        <style>
            /* CSS for the metrics grid */
            .metric-container {
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            }
            .metric-label {
                color: #1f77b4;
                font-size: 18px;
                margin: 0;
            }
            .metric-value {
                color: #1f77b4;
                font-size: 36px;
                margin: 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# For standalone testing
if __name__ == "__main__":
    st.session_state['user_id'] = 1  # Example user_id for testing
    progress_page()
