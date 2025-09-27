import streamlit as st
import pandas as pd
import time
import json
import os

PLAYERS_FILE = "Players.json"
GAMES_FOLDER = "games"

# Δημιουργία φακέλου games αν δεν υπάρχει
if not os.path.exists(GAMES_FOLDER):
    os.makedirs(GAMES_FOLDER)

# Φόρτωσε παίκτες
with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
    players_data = json.load(f)

# Αρχικοποίηση session_state για χρόνους και κατάσταση
for p in players_data:
    if p["name"] not in st.session_state:
        st.session_state[p["name"]] = {"time": 0, "running": False, "start_time": None, "selected": False}

st.title("Football Player Timer")

st.subheader("Επιλέξτε ποιοι θα παίξουν:")

# Επιλογή παικτών
for p in players_data:
    checked = st.checkbox(p["name"], value=st.session_state[p["name"]]["selected"], key="cb_"+p["name"])
    st.session_state[p["name"]]["selected"] = checked

st.subheader("Έλεγχος χρόνου:")

# Κουμπιά Start/Pause για κάθε επιλεγμένο παίκτη
for p in players_data:
    if st.session_state[p["name"]]["selected"]:
        cols = st.columns([2,1,1])
        name_col, time_col, btn_col = cols
        # Υπολογισμός χρόνου
        t = st.session_state[p["name"]]["time"]
        if st.session_state[p["name"]]["running"]:
            t += time.time() - st.session_state[p["name"]]["start_time"]
        minutes = int(t // 60)
        seconds = int(t % 60)
        time_col.write(f"{minutes}:{seconds:02d}")
        
        # Start/Pause κουμπί
        if btn_col.button("Start/Pause", key="btn_"+p["name"]):
            if not st.session_state[p["name"]]["running"]:
                st.session_state[p["name"]]["start_time"] = time.time()
                st.session_state[p["name"]]["running"] = True
            else:
                elapsed = time.time() - st.session_state[p["name"]]["start_time"]
                st.session_state[p["name"]]["time"] += elapsed
                st.session_state[p["name"]]["running"] = False

# Save Game
if st.button("Save Game"):
    data = []
    for p in players_data:
        if st.session_state[p["name"]]["selected"]:
            # Αν τρέχει, ενημέρωση χρόνου
            t = st.session_state[p["name"]]["time"]
            if st.session_state[p["name"]]["running"]:
                t += time.time() - st.session_state[p["name"]]["start_time"]
            data.append({"Name": p["name"], "Time (s)": int(t)})
    df = pd.DataFrame(data)
    game_num = len([f for f in os.listdir(GAMES_FOLDER) if f.startswith("game_")]) + 1
    csv_file = os.path.join(GAMES_FOLDER, f"game_{game_num}.csv")
    df.to_csv(csv_file, index=False, encoding="utf-8")
    st.success(f"Saved game as {csv_file}")

# New Game
if st.button("New Game"):
    for p in players_data:
        st.session_state[p["name"]] = {"time":0,"running":False,"start_time":None,"selected":False}
    st.experimental_rerun()
