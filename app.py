import streamlit as st
import time
import json
from io import BytesIO
from streamlit_autorefresh import st_autorefresh

# --- Page config ---
st.set_page_config(page_title="Football Timer", layout="wide", page_icon="⚽")

# --- Στυλ ---
st.markdown("""
<style>
div.stButton > button {
    height: 60px; width: 100%; font-size: 20px;
    background-color: #00bfa6; color: white; border-radius: 10px;
}
.stDownloadButton>button {
    background-color: #ff6b6b; color: white; border-radius: 10px; font-size: 20px; height: 60px;
}
body { background-color: #f0f8ff; color: #0d1b2a; font-family: Arial, sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- Auto-refresh κάθε 1 δευτερόλεπτο ---
st_autorefresh(interval=1000, key="refresh")

# --- Load players ---
players_file = "Players.json"
try:
    with open(players_file, "r", encoding="utf-8") as f:
        players = json.load(f)
except FileNotFoundError:
    st.error("Δεν βρέθηκε το Players.json")
    st.stop()

st.title("⚽ Football Timer - Real Time 🕒")

game_name = st.text_input("Όνομα Αγώνα", "game_1")
selected_players = st.multiselect("Επίλεξε ποιοι παίζουν", players)

# --- Session state initialization ---
for p in selected_players:
    if f"{p}_running" not in st.session_state:
        st.session_state[f"{p}_running"] = False
    if f"{p}_start_time" not in st.session_state:
        st.s
