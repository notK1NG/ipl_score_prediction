import math
import numpy as np
import pickle
import streamlit as st
import os
import requests

# Set Streamlit Page Configuration
st.set_page_config(page_title="IPL_Score_Predictor", layout="centered")

# Google Drive File ID for `ml_model.pkl`
file_id = "1ddgUCDcKRBIp-HZA7qwMpNDOXYjWEIzl"  # Replace with actual file ID
model_path = "ml_model.pkl"

# Construct the direct download URL
url = f"https://drive.google.com/uc?export=download&id={file_id}"

# Download model using requests if not already present
if not os.path.exists(model_path):
    st.info("Downloading model, please wait...")
    response = requests.get(url, stream=True)
    with open(model_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

# Load the ML Model
try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Failed to load model: {e}")

# Page Title
st.markdown("<h1 style='text-align: center; color: white;'> IPL Score Predictor 2022 </h1>", unsafe_allow_html=True)

# Add Background Image
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

# Add Description
with st.expander("Description"):
    st.info("""A Simple ML Model to predict IPL Scores between teams in an ongoing match. To ensure reliability, the minimum number of overs considered is greater than 5.""")

# Select Batting Team
batting_team = st.selectbox("Select the Batting Team", (
    "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab",
    "Kolkata Knight Riders", "Mumbai Indians", "Rajasthan Royals",
    "Royal Challengers Bangalore", "Sunrisers Hyderabad"
))

# Encode Batting Team
team_encoding = {
    "Chennai Super Kings": [1, 0, 0, 0, 0, 0, 0, 0],
    "Delhi Daredevils": [0, 1, 0, 0, 0, 0, 0, 0],
    "Kings XI Punjab": [0, 0, 1, 0, 0, 0, 0, 0],
    "Kolkata Knight Riders": [0, 0, 0, 1, 0, 0, 0, 0],
    "Mumbai Indians": [0, 0, 0, 0, 1, 0, 0, 0],
    "Rajasthan Royals": [0, 0, 0, 0, 0, 1, 0, 0],
    "Royal Challengers Bangalore": [0, 0, 0, 0, 0, 0, 1, 0],
    "Sunrisers Hyderabad": [0, 0, 0, 0, 0, 0, 0, 1]
}

prediction_array = team_encoding[batting_team]

# Select Bowling Team
bowling_team = st.selectbox("Select the Bowling Team", (
    "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab",
    "Kolkata Knight Riders", "Mumbai Indians", "Rajasthan Royals",
    "Royal Challengers Bangalore", "Sunrisers Hyderabad"
))

if bowling_team == batting_team:
    st.error("Bowling and Batting teams should be different")

# Encode Bowling Team
prediction_array += team_encoding[bowling_team]

# Input Fields
col1, col2 = st.columns(2)

with col1:
    overs = st.number_input("Enter the Current Over", min_value=5.1, max_value=19.5, value=5.1, step=0.1)
    if overs - math.floor(overs) > 0.5:
        st.error("Please enter a valid over (max 6 balls per over)")

with col2:
    runs = st.number_input("Enter Current Runs", min_value=0, max_value=354, step=1, format="%i")

wickets = st.slider("Enter Wickets Fallen", 0, 9)

col3, col4 = st.columns(2)

with col3:
    runs_in_prev_5 = st.number_input("Runs in Last 5 Overs", min_value=0, max_value=runs, step=1, format="%i")

with col4:
    wickets_in_prev_5 = st.number_input("Wickets in Last 5 Overs", min_value=0, max_value=wickets, step=1, format="%i")

# Prepare Data for Prediction
prediction_array += [runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]
prediction_array = np.array([prediction_array])

# Predict Score
if st.button("Predict Score"):
    try:
        predict = model.predict(prediction_array)
        my_prediction = int(round(predict[0]))
        st.success(f"PREDICTED MATCH SCORE: {my_prediction - 5} to {my_prediction + 5}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
