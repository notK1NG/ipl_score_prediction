import math
import numpy as np
import pickle
import streamlit as st
import gdown
import os

# SET PAGE WIDE
st.set_page_config(page_title='IPL_Score_Predictor', layout="centered")

# Google Drive file ID (Replace with your actual file ID)
file_id = "1VRZ9mmfzy3hiZq9rNsotEnOiasnS4pg7"
model_path = "ml_model.pkl"

# Download model if not already present
if not os.path.exists(model_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    try:
        gdown.download(url, model_path, quiet=False)
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model download failed. Check the file ID or permissions.")
    except Exception as e:
        st.error(f"Error downloading model: {e}")
        st.stop()

# Load the ML model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Title of the page with CSS
st.markdown("<h1 style='text-align: center; color: white;'> IPL Score Predictor 2022 </h1>", unsafe_allow_html=True)

# Add background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://4.bp.blogspot.com/-F6aZF5PMwBQ/Wrj5h204qxI/AAAAAAAABao/4QLn48RP3x0P8Ry0CcktxilJqRfv1IfcACLcBGAs/s1600/GURU%2BEDITZ%2Bbackground.jpg");
        background-attachment: fixed;
        background-size: cover
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add description
with st.expander("Description"):
    st.info("""A Simple ML Model to predict IPL Scores between teams in an ongoing match. To make sure the model results in accurate score predictions, the minimum number of current overs considered is greater than 5 overs.""")

# Select Batting Team
batting_team = st.selectbox('Select the Batting Team ', (
    'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
))

prediction_array = []
team_mapping = {
    'Chennai Super Kings': [1, 0, 0, 0, 0, 0, 0, 0],
    'Delhi Daredevils': [0, 1, 0, 0, 0, 0, 0, 0],
    'Kings XI Punjab': [0, 0, 1, 0, 0, 0, 0, 0],
    'Kolkata Knight Riders': [0, 0, 0, 1, 0, 0, 0, 0],
    'Mumbai Indians': [0, 0, 0, 0, 1, 0, 0, 0],
    'Rajasthan Royals': [0, 0, 0, 0, 0, 1, 0, 0],
    'Royal Challengers Bangalore': [0, 0, 0, 0, 0, 0, 1, 0],
    'Sunrisers Hyderabad': [0, 0, 0, 0, 0, 0, 0, 1]
}
prediction_array.extend(team_mapping[batting_team])

# Select Bowling Team
bowling_team = st.selectbox('Select the Bowling Team ', (
    'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
))

if bowling_team == batting_team:
    st.error('Bowling and Batting teams should be different')
prediction_array.extend(team_mapping[bowling_team])

col1, col2 = st.columns(2)

# Enter the Current Ongoing Over
with col1:
    overs = st.number_input('Enter the Current Over', min_value=5.1, max_value=19.5, value=5.1, step=0.1)
    if overs - math.floor(overs) > 0.5:
        st.error('Please enter valid over input as one over only contains 6 balls')

# Enter Current Runs
with col2:
    runs = st.number_input('Enter Current Runs', min_value=0, max_value=354, step=1, format='%i')

# Wickets Taken till now
wickets = st.slider('Enter Wickets Fallen till now', 0, 9)

col3, col4 = st.columns(2)

# Runs in last 5 overs
with col3:
    runs_in_prev_5 = st.number_input('Runs scored in the last 5 overs', min_value=0, max_value=runs, step=1, format='%i')

# Wickets in last 5 overs
with col4:
    wickets_in_prev_5 = st.number_input('Wickets taken in the last 5 overs', min_value=0, max_value=wickets, step=1, format='%i')

# Get all the data for prediction
prediction_array.extend([runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5])
prediction_array = np.array([prediction_array])
predict = model.predict(prediction_array)

if st.button('Predict Score'):
    my_prediction = int(round(predict[0]))
    st.success(f'PREDICTED MATCH SCORE: {my_prediction-5} to {my_prediction+5}')
