import streamlit as st
import requests
import google.generativeai as genai
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# --- 1. SETTINGS & CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ LOOK ---
st.set_page_config(page_title="World Cup 2026 Pro Dashboard", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
    /* Αλλαγή φόντου και γραμματοσειράς */
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Στυλ για τις κάρτες (Match Cards) */
    .match-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #007bff;
    }
    
    /* Στυλ για τον Predictor */
    .prediction-box {
        background-color: #e3f2fd;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #90caf9;
        color: #0d47a1;
    }
    
    /* Τίτλοι */
    h1 {
        color: #1e1e1e;
        text-align: center;
        font-weight: 800;
        padding-bottom: 20px;
    }
    
    /* Ωραία Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        background-color: white;
        border-radius: 10px 10px 0 0;
        gap: 1px;
        padding: 10px 20px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. KEYS & REFRESH
st_autorefresh(interval=120000, key="datarefresh")
gemini_key = st.secrets["GEMINI_API_KEY"]
football_key = st.secrets["FOOTBALL_API_KEY"]

def call_api(endpoint, params=None):
    url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
    headers = {"X-RapidAPI-Key": football_key, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    except: return None

# --- HEADER ---
st.markdown("<h1>🏆 WORLD CUP 2026 LIVE HUB</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🎮 LIVE SCORES", "📊 STANDINGS", "🔮 AI PREDICTOR"])

with tab1:
    st.markdown("### 📅 Recent & Live Matches")
    # Εδώ θα τραβάμε τα Live
    data = call_api("fixtures", {"league": "1", "season": "2026"})
    if data and data.get('response'):
        # Χρησιμοποιούμε columns για να φαίνονται σαν κάρτες
        for game in data['response'][:6]:
            with st.container():
                home = game['teams']['home']
                away = game['teams']['away']
                goals_h = game['goals']['home'] if game['goals']['home'] is not None else 0
                goals_a = game['goals']['away'] if game['goals']['away'] is not None else 0
                
                st.markdown(f"""
                <div class="match-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="text-align: center; flex: 1;">
                            <img src="{home['logo']}" width="40"><br><b>{home['name']}</b>
                        </div>
                        <div style="flex: 1; text-align: center; font-size: 24px; font-weight: bold;">
                            {goals_h} - {goals_a}
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <img src="{away['logo']}" width="40"><br><b>{away['name']}</b>
                        </div>
                    </div>
                    <div style="text-align: center; color: gray; font-size: 12px; margin-top: 10px;">
                        {game['fixture']['status']['long']} | {game['fixture']['venue']['name']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.subheader("Group Standings")
    standings_data = call_api("standings", {"league": "1", "season": "2026"})
    if standings_data and standings_data.get('response'):
        all_groups = standings_data['response'][0]['league']['standings']
        # Δημιουργούμε 3 στήλες για να βλέπουμε 3 ομίλους ανά σειρά
        cols = st.columns(3)
        for i, group in enumerate(all_groups):
            with cols[i % 3]:
                st.markdown(f"**{group[0]['group']}**")
                df = pd.DataFrame([
                    {"#": t['rank'], "Team": t['team']['name'], "P": t['points']} for t in group
                ])
                st.dataframe(df, hide_index=True, use_container_width=True)

with tab3:
    st.markdown("### 🔮 Magical AI Prediction")
    c1, c2 = st.columns(2)
    t1 = c1.text_input("Home Team", "Argentina")
    t2 = c2.text_input("Away Team", "France")
    
    if st.button("Generate Expert Prediction ✨"):
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Detailed football analysis and score prediction for {t1} vs {t2} in World Cup 2026. Use stats and form."
        
        with st.spinner("Analyzing data..."):
            response = model.generate_content(prompt)
            st.markdown(f"""<div class="prediction-box">{response.text}</div>""", unsafe_allow_html=True)
