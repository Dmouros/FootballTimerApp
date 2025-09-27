import streamlit as st
import time
import json
import os
from io import BytesIO

st.set_page_config(page_title="Football Timer", layout="wide")

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

# Επιλογή παικτών
selected_players = st.multiselect("Επίλεξε ποιοι παίζουν", players)

# Δημιουργία session state για χρονόμετρα
for p in selected_players:
    if f"{p}_running" not in st.session_state:
        st.session_state[f"{p}_running"] = False
    if f"{p}_start_time" not in st.session_state:
        st.session_state[f"{p}_start_time"] = 0
    if f"{p}_elapsed" not in st.session_state:
        st.session_state[f"{p}_elapsed"] = 0

st.write("---")

# Ζωντανή ενημέρωση χρόνου
def display_player(p):
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.write(p)
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
        current = st.session_state[f"{p}_elapsed"]
        if st.session_state[f"{p}_running"]:
            current += time.time() - st.session_state[f"{p}_start_time"]
        st.write(f"{int(current)} sec")

# Εμφάνιση παικτών
for p in selected_players:
    display_player(p)

# Αποθήκευση σε JSON και download
if st.button("Αποθήκευση και Κατέβασμα Αγώνα"):
    results = {}
    for p in selected_players:
        elapsed = st.session_state[f"{p}_elapsed"]
        if st.session_state[f"{p}_running"]:
            elapsed += time.time() - st.session_state[f"{p}_start_time"]
        results[p] = int(elapsed)
    # Δημιουργία αρχείου JSON για download
    json_bytes = BytesIO(json.dumps(results, ensure_ascii=False, indent=2).encode('utf-8'))
    st.download_button(label="Κατέβασε τον αγώνα", data=json_bytes, file_name=f"{game_name}.json", mime="application/json")
