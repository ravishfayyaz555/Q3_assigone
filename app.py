import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# Set page configuration
st.set_page_config(
    page_title="Girls Cycling Race Tracker",
    page_icon="🚲",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #fce4ec;
    }
    .stButton>button {
        background-color: #ff4081;
        color: white;
    }
    .title {
        color: #c2185b;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.markdown("<h1 class='title'>🚲 Girls Cycling Race Tracker 🏆</h1>", unsafe_allow_html=True)

# Initialize session state
if 'races' not in st.session_state:
    st.session_state.races = []

# Sidebar for adding new race data
with st.sidebar:
    st.header("Add New Race Data")
    
    race_date = st.date_input("Race Date", datetime.today())
    race_name = st.text_input("Race Name")
    participant_name = st.text_input("Participant Name")
    age_category = st.selectbox("Age Category", ["Junior (8-12)", "Teen (13-16)", "Youth (17-19)"])
    distance = st.number_input("Distance (km)", min_value=0.0, max_value=100.0, step=0.1)
    completion_time = st.time_input("Completion Time")
    position = st.number_input("Final Position", min_value=1, step=1)
    
    if st.button("Add Race Entry"):
        new_race = {
            "date": race_date,
            "race_name": race_name,
            "participant": participant_name,
            "age_category": age_category,
            "distance": distance,
            "completion_time": completion_time.strftime("%H:%M:%S"),
            "position": position
        }
        st.session_state.races.append(new_race)
        st.success("Race entry added successfully!")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Race Statistics")
    if st.session_state.races:
        df = pd.DataFrame(st.session_state.races)
        
        # Race positions visualization
        fig_positions = px.bar(
            df,
            x='participant',
            y='position',
            color='age_category',
            title='Race Positions by Participant',
            labels={'position': 'Position', 'participant': 'Participant'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_positions.update_yaxes(autorange="reversed")  # Reverse y-axis so position 1 is at the top
        st.plotly_chart(fig_positions)

with col2:
    st.subheader("🏃‍♀️ Distance Analysis")
    if st.session_state.races:
        # Distance by age category
        fig_distance = px.box(
            df,
            x='age_category',
            y='distance',
            color='age_category',
            title='Distance Distribution by Age Category',
            labels={'distance': 'Distance (km)', 'age_category': 'Age Category'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_distance)

# Race Results Table
st.subheader("📝 Race Results")
if st.session_state.races:
    st.dataframe(
        pd.DataFrame(st.session_state.races)
        .sort_values(by=['date', 'position'])
        .style.background_gradient(subset=['distance'], cmap='RdYlGn')
    )
else:
    st.info("No race data available. Add race entries using the sidebar!")

# Performance Insights
if st.session_state.races:
    st.subheader("🎯 Performance Insights")
    col3, col4, col5 = st.columns(3)
    
    df = pd.DataFrame(st.session_state.races)
    
    with col3:
        total_participants = len(df['participant'].unique())
        st.metric("Total Participants", total_participants)
        
    with col4:
        total_races = len(df['race_name'].unique())
        st.metric("Total Races", total_races)
        
    with col5:
        avg_distance = round(df['distance'].mean(), 2)
        st.metric("Average Race Distance", f"{avg_distance} km")

# Add motivational quotes
motivational_quotes = [
    "Every champion was once a beginner!",
    "Push your limits, find your strength!",
    "The race is won in the preparation!",
    "Believe in yourself and you're halfway there!"
]

st.markdown("---")
st.markdown(f"### 💫 Daily Inspiration")
st.markdown(f"*{random.choice(motivational_quotes)}*")
