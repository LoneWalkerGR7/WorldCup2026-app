import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. CONFIG & CSS (COSMIC THEME - WHITE TEXT - BLACK RESET) ---
st.set_page_config(page_title="World Cup 2026 Official", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important; }
    
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stat-val { font-size: 22px; font-weight: 800; color: #06b6d4 !important; }

    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .st-venue { font-size: 9px; color: #94a3b8 !important; font-style: italic; margin-top: 5px; }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    
    /* Reset Button: Black text */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: white !important;
        font-weight: 800 !important;
        border: none !important;
    }
    
    /* Tables White Text */
    div[data-testid="stTable"] table { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS = [
    {"n": "Mexico", "g": "A"}, {"n": "South Africa", "g": "A"}, {"n": "South Korea", "g": "A"}, {"n": "Czechia", "g": "A"},
    {"n": "Canada", "g": "B"}, {"n": "Bosnia and Herzegovina", "g": "B"}, {"n": "Qatar", "g": "B"}, {"n": "Switzerland", "g": "B"},
    {"n": "Brazil", "g": "C"}, {"n": "Morocco", "g": "C"}, {"n": "Haiti", "g": "C"}, {"n": "Scotland", "g": "C"},
    {"n": "USA", "g": "D"}, {"n": "Paraguay", "g": "D"}, {"n": "Australia", "g": "D"}, {"n": "Turkey", "g": "D"},
    {"n": "Germany", "g": "E"}, {"n": "Curacao", "g": "E"}, {"n": "Ivory Coast", "g": "E"}, {"n": "Ecuador", "g": "E"},
    {"n": "Netherlands", "g": "F"}, {"n": "Japan", "g": "F"}, {"n": "Sweden", "g": "F"}, {"n": "Tunisia", "g": "F"},
    {"n": "Belgium", "g": "G"}, {"n": "Egypt", "g": "G"}, {"n": "Iran", "g": "G"}, {"n": "New Zealand", "g": "G"},
    {"n": "Spain", "g": "H"}, {"n": "Cape Verde", "g": "H"}, {"n": "Saudi Arabia", "g": "H"}, {"n": "Uruguay", "g": "H"},
    {"n": "France", "g": "I"}, {"n": "Senegal", "g": "I"}, {"n": "Iraq", "g": "I"}, {"n": "Norway", "g": "I"},
    {"n": "Argentina", "g": "J"}, {"n": "Algeria", "g": "J"}, {"n": "Austria", "g": "J"}, {"n": "Jordan", "g": "J"},
    {"n": "Portugal", "g": "K"}, {"n": "DR Congo", "g": "K"}, {"n": "Uzbekistan", "g": "K"}, {"n": "Colombia", "g": "K"},
    {"n": "England", "g": "L"}, {"n": "Croatia", "g": "L"}, {"n": "Ghana", "g": "L"}, {"n": "Panama", "g": "L"}
]

# --- 3. ΤΟ ΠΛΗΡΕΣ ΠΡΟΓΡΑΜΜΑ (72 ΑΓΩΝΕΣ) ---
RAW_MATCHES_LIST = [
    ["A", "11/06 22:00", "Estadio Azteca", "Mexico", "South Africa"],
    ["A", "12/06 05:00", "Estadio Akron", "South Korea", "Czechia"],
    ["B", "12/06 22:00", "BMO Field", "Canada", "Bosnia and Herzegovina"],
    ["D", "13/06 04:00", "SoFi Stadium", "USA", "Paraguay"],
    ["D", "14/06 07:00", "BC Place", "Australia", "Turkey"],
    ["B", "13/06 22:00", "Levi's Stadium", "Qatar", "Switzerland"],
    ["C", "14/06 01:00", "MetLife Stadium", "Brazil", "Morocco"],
    ["C", "14/06 04:00", "Gillette Stadium", "Haiti", "Scotland"],
    ["E", "14/06 20:00", "NRG Stadium", "Germany", "Curacao"],
    ["F", "14/06 23:00", "AT&T Stadium", "Netherlands", "Japan"],
    ["E", "15/06 02:00", "Lincoln Financial Field", "Ivory Coast", "Ecuador"],
    ["F", "15/06 05:00", "Estadio BBVA", "Sweden", "Tunisia"],
    ["H", "15/06 19:00", "Mercedes-Benz Stadium", "Spain", "Cape Verde"],
    ["G", "15/06 22:00", "Lumen Field", "Belgium", "Egypt"],
    ["H", "16/06 01:00", "Hard Rock Stadium", "Saudi Arabia", "Uruguay"],
    ["G", "16/06 04:00", "SoFi Stadium", "Iran", "New Zealand"],
    ["J", "17/06 07:00", "Levi's Stadium", "Austria", "Jordan"],
    ["I", "16/06 10:00", "MetLife Stadium", "France", "Senegal"],
    ["I", "17/06 01:00", "Gillette Stadium", "Iraq", "Norway"],
    ["J", "17/06 04:00", "Arrowhead Stadium", "Argentina", "Algeria"],
    ["K", "17/06 08:00", "NRG Stadium", "Portugal", "DR Congo"],
    ["L", "17/06 11:00", "AT&T Stadium", "England", "Croatia"],
    ["L", "18/06 02:00", "BMO Field", "Ghana", "Panama"],
    ["K", "18/06 05:00", "Estadio Azteca", "Uzbekistan", "Colombia"],
    ["A", "18/06 07:00", "Mercedes-Benz Stadium", "Czechia", "South Africa"],
    ["B", "18/06 10:00", "SoFi Stadium", "Switzerland", "Bosnia and Herzegovina"],
    ["B", "19/06 01:00", "BC Place", "Canada", "Qatar"],
    ["A", "19/06 04:00", "Estadio Akron", "Mexico", "South Korea"],
    ["D", "20/06 06:00", "Levi's Stadium", "Turkey", "Paraguay"],
    ["D", "19/06 10:00", "Lumen Field", "USA", "Australia"],
    ["C", "20/06 01:00", "Gillette Stadium", "Scotland", "Morocco"],
    ["C", "20/06 03:30", "Lincoln Financial Field", "Brazil", "Haiti"],
    ["F", "21/06 07:00", "Estadio BBVA", "Tunisia", "Japan"],
    ["F", "20/06 08:00", "NRG Stadium", "Netherlands", "Sweden"],
    ["E", "20/06 11:00", "BMO Field", "Germany", "Ivory Coast"],
    ["E", "21/06 03:00", "Arrowhead Stadium", "Ecuador", "Curacao"],
    ["H", "21/06 07:00", "Mercedes-Benz Stadium", "Spain", "Saudi Arabia"],
    ["G", "21/06 10:00", "SoFi Stadium", "Belgium", "Iran"],
    ["H", "22/06 01:00", "Hard Rock Stadium", "Uruguay", "Cape Verde"],
    ["G", "22/06 04:00", "BC Place", "New Zealand", "Egypt"],
    ["J", "22/06 08:00", "AT&T Stadium", "Argentina", "Austria"],
    ["I", "23/06 12:00", "Lincoln Financial Field", "France", "Iraq"],
    ["I", "23/06 03:00", "MetLife Stadium", "Norway", "Senegal"],
    ["J", "23/06 06:00", "Levi's Stadium", "Jordan", "Algeria"],
    ["K", "23/06 08:00", "NRG Stadium", "Portugal", "Uzbekistan"],
    ["L", "23/06 11:00", "Gillette Stadium", "England", "Ghana"],
    ["L", "24/06 02:00", "BMO Field", "Panama", "Croatia"],
    ["K", "24/06 05:00", "Estadio Akron", "Colombia", "DR Congo"],
    ["B", "24/06 10:00", "BC Place", "Switzerland", "Canada"],
    ["B", "24/06 10:00", "Lumen Field", "Bosnia and Herzegovina", "Qatar"],
    ["C", "25/06 01:00", "Hard Rock Stadium", "Scotland", "Brazil"],
    ["C", "25/06 01:00", "Mercedes-Benz Stadium", "Morocco", "Haiti"],
    ["A", "25/06 04:00", "Estadio Azteca", "Czechia", "Mexico"],
    ["A", "25/06 04:00", "Estadio BBVA", "South Africa", "South Korea"],
    ["E", "25/06 11:00", "MetLife Stadium", "Ecuador", "Germany"],
    ["E", "25/06 11:00", "Lincoln Financial Field", "Curacao", "Ivory Coast"],
    ["F", "26/06 02:00", "AT&T Stadium", "Japan", "Sweden"],
    ["F", "26/06 02:00", "Arrowhead Stadium", "Tunisia", "Netherlands"],
    ["D", "26/06 05:00", "SoFi Stadium", "Turkey", "USA"],
    ["D", "26/06 05:00", "Levi's Stadium", "Paraguay", "Australia"],
    ["I", "26/06 10:00", "Gillette Stadium", "Norway", "France"],
    ["I", "26/06 10:00", "BMO Field", "Senegal", "Iraq"],
    ["H", "27/06 03:00", "Estadio Akron", "Uruguay", "Spain"],
    ["H", "27/06 03:00", "NRG Stadium", "Cape Verde", "Saudi Arabia"],
    ["G", "27/06 06:00", "Lumen Field", "Egypt", "Iran"],
    ["G", "27/06 06:00", "BC Place", "New Zealand", "Belgium"],
    ["L", "28/06 12:00", "MetLife Stadium", "Panama", "England"],
    ["L", "28/06 12:00", "Lincoln Financial Field", "Croatia", "Ghana"],
    ["K", "28/06 02:30", "Hard Rock Stadium", "Colombia", "Portugal"],
    ["K", "28/06 02:30", "Mercedes-Benz Stadium", "DR Congo", "Uzbekistan"],
    ["J", "28/06 05:00", "Arrowhead Stadium", "Algeria", "Austria"],
    ["J", "28/06 05:00", "AT&T Stadium", "Jordan", "Argentina"]
]

# --- 4. SESSION STATE INITIALIZATION ---
if 'wc_matches' not in st.session_state:
    matches = []
    for i, m_data in enumerate(RAW_MATCHES_LIST):
        matches.append({
            "id": i+1, "group": m_data[0], "dt": m_data[1], "st": m_data[2],
            "h": m_data[3], "a": m_data[4], "sh": None, "sa": None, "fin": False,
            "y": 0, "r": 0, "p": 0, "og": 0
        })
    st.session_state.wc_matches = matches

# --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['y'], m['r'] = random.randint(1, 6), (1 if random.random() > 0.9 else 0)
            m['p'], m['og'] = (1 if random.random() > 0.85 else 0), (1 if random.random() > 0.96 else 0)
            m['fin'] = True
    st.rerun()

def reset_tourney():
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.rerun()

# --- 6. UI ---
st.markdown("<h1>🏆 MUNDIAL 2026 OFFICIAL PORTAL</h1>", unsafe_allow_html=True)

fin_m = [m for m in st.session_state.wc_matches if m['fin']]
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin_m)}</div><div class="stat-label">Goals</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ AUTO-PLAY SIMULATOR", on_click=auto_play, type="primary")
with c4: st.button("🔄 RESET TOURNAMENT", on_click=reset_tourney, type="secondary")

t1, t2, t3 = st.tabs(["📅 CALENDAR & STATS", "📊 STANDINGS", "🔮 AI PREDICTIONS"])

with t1:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding:10px 0;">
                    <div style="width:40%; text-align:center; font-weight:bold;">{m['h']}</div>
                    <div style="font-size:22px; color:#06b6d4; font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="width:40%; text-align:center; font-weight:bold;">{m['a']}</div>
                </div>
                <div class="st-venue">📍 {m['st']} | 🟨 {m['y']} 🟥 {m['r']} 🎯 {m['p']}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Edit Results"):
                h_val = st.number_input(f"Goals {m['h']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"h{m['id']}")
                a_val = st.number_input(f"Goals {m['a']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"a{m['id']}")
                if st.button("Save", key=f"btn{m['id']}"):
                    m.update({"sh": h_val, "sa": a_val, "fin": True}); st.rerun()

with t2:
    GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    cols_s = st.columns(3)
    for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_teams = [t['n'] for t in TEAMS if t['g'] == gId]
            res = []
            for t in g_teams:
                pts, gd = 0, 0
                for m in st.session_state.wc_matches:
                    if m['fin'] and (m['h'] == t or m['a'] == t):
                        is_h = m['h'] == t
                        h_s, a_s = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                res.append({"Team": t, "Pts": pts, "GD": gd})
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with t3:
    st.markdown("### 🔮 Gemini AI Expert Analyst")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            # Dynamic Model Selection for 404 Prevention
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            working_model = next((m for m in model_list if '1.5-flash' in m), model_list[0])
            model = genai.GenerativeModel(working_model)
            
            t_names = sorted([t['n'] for t in TEAMS])
            c1, c2 = st.columns(2)
            home_t = c1.selectbox("Home", t_names, key="sel_h")
            away_t = c2.selectbox("Away", t_names, index=1, key="sel_a")
            if st.button("GENERATE PRO PREDICTION", type="primary"):
                with st.spinner("AI analyzing tactics..."):
                    resp = model.generate_content(f"Analyze World Cup 2026: {home_t} vs {away_t}. Probable score in Greek.")
                    st.info(resp.text)
        except Exception as e: st.error(f"Error: {e}")
