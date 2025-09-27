import streamlit as st
import time
import json
from io import BytesIO

st.set_page_config(page_title="Football Timer", layout="wide", page_icon="⚽")

# Στυλ
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

# Load players
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

# Session state
for p in selected_players:
    if f"{p}_running" not in st.session_state:
        st.session_state[f"{p}_running"] = False
    if f"{p}_start_time" not in st.session_state:
        st.session_state[f"{p}_start_time"] = 0
    if f"{p}_elapsed" not in st.session_state:
        st.session_state[f"{p}_elapsed"] = 0
    if f"{p}_placeholder" not in st.session_state:
        st.session_state[f"{p}_placeholder"] = st.empty()

# Format time
def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} sec"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins} min {secs} sec"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours} h {mins} min {secs} sec"

# Εμφάνιση παικτών
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
        if st.session_state[f"{p}_placeholder"] is None:
            st.session_state[f"{p}_placeholder"] = st.empty()

st.write("---")

# Κουμπί download **έξω από το loop**
if st.button("Αποθήκευση και Κατέβασμα Αγώνα"):
    results = {}
    for p in selected_players:
        elapsed = st.session_state[f"{p}_elapsed"]
        if st.session_state[f"{p}_running"]:
            elapsed += time.time() - st.session_state[f"{p}_start_time"]
        results[p] = int(elapsed)
    json_bytes = BytesIO(json.dumps(results, ensure_ascii=False, indent=2).encode('utf-8'))
    st.download_button(
        label="Κατέβασε τον αγώνα",
        data=json_bytes,
        file_name=f"{game_name}.json",
        mime="application/json"
    )

# --- Real-time loop για τους χρόνους ---
while True:
    for p in selected_players:
        current = st.session_state[f"{p}_elapsed"]
        if st.session_state[f"{p}_running"]:
            current += time.time() - st.session_state[f"{p}_start_time"]
        st.session_state[f"{p}_placeholder"].markdown(f"**{format_time(current)}**")
    time.sleep(1)
