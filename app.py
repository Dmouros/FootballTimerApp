import streamlit as st
import time
import json
from io import BytesIO

st.set_page_config(page_title="Football Timer", layout="wide")

# Φόρτωση παικτών
players_file = "Players.json"
try:
    with open(players_file, "r", encoding="utf-8") as f:
        players = json.load(f)
except FileNotFoundError:
    st.error("Δεν βρέθηκε το Players.json")
    st.stop()

st.title("Football Timer - Real Time")

# Επιλογή αγώνα
game_name = st.text_input("Όνομα Αγώνα (π.χ. game_1)", "game_1")

# Επιλογή παικτών
selected_players = st.multiselect("Επίλεξε ποιοι παίζουν", players)

# Session state για κάθε παίχτη
for p in selected_players:
    if f"{p}_running" not in st.session_state:
        st.session_state[f"{p}_running"] = False
    if f"{p}_start_time" not in st.session_state:
        st.session_state[f"{p}_start_time"] = 0
    if f"{p}_elapsed" not in st.session_state:
        st.session_state[f"{p}_elapsed"] = 0
    if f"{p}_placeholder" not in st.session_state:
        st.session_state[f"{p}_placeholder"] = None

st.write("---")

# Εμφάνιση παικτών με live χρόνο
for p in selected_players:
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.markdown(f"**{p}**")
    with col2:
        if st.session_state[f"{p}_running"]:
            if st.button(f"Pause {p}", key=f"pause_{p}"):
                st.session_state[f"{p}_running"] = False
                st.session_state[f"{p}_elapsed"] += time.time() - st.session_state[f"{p}_start_time"]
        else:
            if st.button(f"Start {p}", key=f"start_{p}"):
                st.session_state[f"{p}_running"] = True
                st.session_state[f"{p}_start_time"] = time.time()
    with col3:
        # Δημιουργία placeholder για live χρόνο
        if st.session_state[f"{p}_placeholder"] is None:
            st.session_state[f"{p}_placeholder"] = st.empty()

# **Real-time update loop**
for i in range(100000):  # μεγάλο όριο, θα τρέχει ουσιαστικά συνέχεια
    for p in selected_players:
        current = st.session_state[f"{p}_elapsed"]
        if st.session_state[f"{p}_running"]:
            current += time.time() - st.session_state[f"{p}_start_time"]
        st.session_state[f"{p}_placeholder"].markdown(f"**{int(current)} sec**")
    time.sleep(1)
