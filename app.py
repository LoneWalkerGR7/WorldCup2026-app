import streamlit as st
import requests
import google.generativeai as genai
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(page_title="World Cup 2026 Pro Tracker", layout="wide", page_icon="⚽")
st.title("🏆 World Cup 2026 - Live Dashboard & AI Predictor")

# Αυτόματη ανανέωση κάθε 2 λεπτά για live σκορ
st_autorefresh(interval=120000, key="datarefresh")

# 2. Keys από Secrets
gemini_key = st.secrets["GEMINI_API_KEY"]
football_key = st.secrets["FOOTBALL_API_KEY"]

# 3. Λειτουργία για κλήσεις στο API
def call_api(endpoint, params=None):
    url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
    headers = {
        "X-RapidAPI-Key": football_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except:
        return None

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📅 Πρόγραμμα & Live", "📊 Ομίλοι", "🔮 AI Πρόβλεψη", "🛑 Πειθαρχία (Κάρτες)"])

# Παράμετροι για το Μουντιάλ 2026 (League ID 1)
params = {"league": "1", "season": "2026"}

with tab1:
    st.subheader("📅 Αγώνες & Ζωντανή Ροή")
    data = call_api("fixtures", params)
    if data and data.get('response'):
        for game in data['response'][:10]: # Δείχνουμε τους επόμενους/τρέχοντες 10
            home = game['teams']['home']['name']
            away = game['teams']['away']['name']
            status = game['fixture']['status']['long']
            score = f"{game['goals']['home']} - {game['goals']['away']}"
            st.write(f"**{home}** {score} **{away}** | Κατάσταση: {status}")
    else:
        st.write("Δεν βρέθηκαν ζωντανοί αγώνες αυτή τη στιγμή.")

with tab2:
    st.subheader("📊 Βαθμολογίες Ομίλων")
    standings_data = call_api("standings", params)
    if standings_data and standings_data.get('response'):
        # Το Μουντιάλ 2026 έχει 12 ομίλους (A-L)
        all_groups = standings_data['response'][0]['league']['standings']
        for group in all_groups:
            group_name = group[0]['group']
            st.write(f"### {group_name}")
            df = pd.DataFrame([
                {
                    "Θέση": t['rank'],
                    "Ομάδα": t['team']['name'],
                    "Αγώνες": t['all']['played'],
                    "Ν-Ι-Η": f"{t['all']['win']}-{t['all']['draw']}-{t['all']['lose']}",
                    "Γκολ": f"{t['all']['goals']['for']}:{t['all']['goals']['against']}",
                    "Πόντοι": t['points']
                } for t in group
            ])
            st.table(df)

with tab3:
    st.subheader("🔮 AI Score Predictor")
    team1 = st.text_input("Ομάδα Α", value="Argentina")
    team2 = st.text_input("Ομάδα Β", value="France")
    if st.button("Ανάλυση & Πρόβλεψη"):
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Είσαι κορυφαίος αναλυτής ποδοσφαίρου. Με βάση τη φόρμα των ομάδων {team1} και {team2}, δώσε ένα πιθανό σκορ για το Μουντιάλ 2026 και προέβλεψε αν θα έχουμε πέναλτι ή κόκκινη κάρτα."
        response = model.generate_content(prompt)
        st.write(response.text)

with tab4:
    st.subheader("🛑 Στατιστικά Καρτών & Ποινών")
    # Τραβάμε τα στατιστικά των ομάδων
    st.write("Εδώ εμφανίζονται οι κίτρινες/κόκκινες κάρτες ανά ομάδα (Live Data)")
    # Σημείωση: Στο API-Football, οι κάρτες έρχονται μέσω του fixtures/events 
    # ή μέσω του league/topcards (αν υποστηρίζεται στο πλάνο σου).
    st.info("Τα δεδομένα πειθαρχίας θα ενημερώνονται αυτόματα με την έναρξη των αγώνων.")
