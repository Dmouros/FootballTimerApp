import streamlit as st
import time
import json
import os

st.set_page_config(page_title="Football Timer", layout="wide")

# Φάκελος για αποθήκευση αγώνων
if not os.path.exists("games"):
    os.makedirs("games")

# Φόρτωση παικτών
players_file = "Players.json"
if os.path.exists(players_file):
    with open(players_file, "r", encoding="utf-8") as f:
        players = json.load(f)
else:
    st.error("Δεν βρέθηκε το Players.json")
    st.stop()

st.title("Football Timer")

# Επιλογή αγώνα
game_name = st.text_input("Όνομα Αγώνα (π.χ. game_1)", "game_1")
game_file = f"games/{game_name}.json"

# Φόρτωση προηγούμενων χρόνων αν υπάρχει
if os.path.exists(game_file):
    with open(game_file, "r", encoding="utf-8") as f:
        player_times = json.load(f)
else:
    player_times = {p: 0 for p in players}

# Επιλογή παικτών για τον αγώνα
selected_players = st.multiselect("Επίλεξε ποιοι παίζουν", players)

# Δημιουργία session state για χρονόμετρα
for p in selected_players:
    if f"{p}_running" not in st.session_state:
        st.session_state[f"{p}_running"] = False
    if f"{p}_start_time" not in st.session_state:
        st.session_state[f"{p}_start_time"] = 0

# Διάταξη για κάθε παίχτη
for p in selected_players:
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.write(p)
    with col2:
        if st.session_state[f"{p}_running"]:
            if st.button(f"Pause {p}", key=f"pause_{p}"):
                st.session_state[f"{p}_running"] = False
                player_times[p] += time.time() - st.session_state[f"{p}_start_time"]
        else:
            if st.button(f"Start {p}", key=f"start_{p}"):
                st.session_state[f"{p}_running"] = True
                st.session_state[f"{p}_start_time"] = time.time()
    with col3:
        # Υπολογισμός τρέχοντος χρόνου
        current_time = player_times[p]
        if st.session_state[f"{p}_running"]:
            current_time += time.time() - st.session_state[f"{p}_start_time"]
        st.write(f"{int(current_time)} sec")

# Αποθήκευση χρόνων σε αρχείο JSON
if st.button("Αποθήκευση αποτελεσμάτων"):
    with open(game_file, "w", encoding="utf-8") as f:
        json.dump(player_times, f, ensure_ascii=False, indent=2)
    st.success(f"Αποθηκεύτηκαν οι χρόνοι στον αγώνα {game_name}")
