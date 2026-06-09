import streamlit as st
import requests
import google.generativeai as genai
import os
import pandas as pd

# Ρύθμιση Σελίδας
st.set_page_config(page_title="World Cup 2026 AI Tracker", layout="wide", page_icon="⚽")
st.title("🏆 World Cup 2026 Live Dashboard & AI Predictor")

# Λήψη Keys από τα Secrets του Streamlit
gemini_key = st.secrets.get("GEMINI_API_KEY")
football_api_key = st.secrets.get("FOOTBALL_API_KEY")

# Λειτουργία για λήψη δεδομένων από το API-Football
def fetch_data(endpoint, params=None):
    url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
    headers = {
        "X-RapidAPI-Key": football_api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# --- Κεντρικό Μενού ---
tabs = st.tabs(["📊 Βαθμολογίες", "📅 Πρόγραμμα & Live", "🔮 AI Προβλέψεις", "🛑 Κάρτες & Ποινές"])

with tabs[0]:
    st.subheader("Βαθμολογίες Ομίλων")
    st.info("Εδώ θα εμφανίζονται αυτόματα οι πόντοι, τα γκολ και οι θέσεις των ομάδων.")
    # Παράδειγμα κώδικα για εμφάνιση πίνακα
    # data = fetch_data("standings", {"league": "1", "season": "2026"})
    # st.dataframe(data)

with tabs[1]:
    st.subheader("Ζωντανή Ροή Αγώνων")
    st.write("Σκορ σε πραγματικό χρόνο.")

with tabs[2]:
    st.subheader("🔮 AI Score Predictor")
    home_team = st.text_input("Γηπεδούχος (π.χ. Greece):")
    away_team = st.text_input("Φιλοξενούμενος (π.χ. Brazil):")
    
    if st.button("Πρόβλεψη με Gemini AI"):
        if gemini_key:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Κάνε μια ανάλυση και πρόβλεψη σκορ για το ματς {home_team} vs {away_team} στο Μουντιάλ 2026. Πες ποιος θα σκοράρει και αν θα υπάρξουν κάρτες."
            response = model.generate_content(prompt)
            st.markdown(response.text)

with tabs[3]:
    st.subheader("Στατιστικά Πειθαρχίας")
    st.write("Κίτρινες, Κόκκινες κάρτες και Πέναλτι ανά ομάδα.")