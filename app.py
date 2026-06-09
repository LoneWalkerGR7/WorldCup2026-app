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
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown { color: white !important; }
    
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
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
        font-weight: bold !important;
    }
    
    /* Tables */
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS = [
    {"n": "Mexico", "g": "A"}, {"n": "South Africa", "g": "A"}, {"n": "South Korea", "g": "A"}, {"n": "Czech Rep.", "g": "A"},
    {"n": "Canada", "g": "B"}, {"n": "Bosnia", "g": "B"}, {"n": "Qatar", "g": "B"}, {"n": "Switzerland", "g": "B"},
    {"n": "Brazil", "g": "C"}, {"n": "Morocco", "g": "C"}, {"n": "Haiti", "g": "C"}, {"n": "Scotland", "g": "C"},
    {"n": "USA", "g": "D"}, {"n": "Paraguay", "g": "D"}, {"n": "Australia", "g": "D"}, {"n": "Turkey", "g": "D"},
    {"n": "Germany", "g": "E"}, {"n": "Curacao", "g": "E"}, {"n": "Ivory Coast", "g": "E"}, {"n": "Ecuador", "g": "E"},
    {"n": "Netherlands", "g": "F"}, {"n": "Japan", "g": "F"}, {"n": "Sweden", "g": "F"}, {"n": "Tunisia", "g": "F"},
    {"n": "Belgium", "g": "G"}, {"n": "Egypt", "g": "G"}, {"n": "Iran", "g": "G"}, {"n": "New Zealand", "g": "G"},
    {"n": "Spain", "g": "H"}, {"n": "Cape Verde", "g": "H"}, {"n": "Saudi Arabia", "g": "H"}, {"n": "Uruguay", "g": "H"},
    {"n": "France", "g": "I"}, {"n": "Senegal", "g": "I"}, {"n": "Iraq", "g": "I"}, {"n": "Norway", "g": "I"},
    {"n": "Argentina", "g": "J"}, {"n": "Algeria", "g": "J"}, {"n": "Austria", "g": "J"}, {"n": "Jordan", "g": "J"},
    {"n": "Portugal", "g": "K"}, {"n": "Congo", "g": "K"}, {"n": "Uzbekistan", "g": "K"}, {"n": "Colombia", "g": "K"},
    {"n": "England", "g": "L"}, {"n": "Croatia", "g": "L"}, {"n": "Ghana", "g": "L"}, {"n": "Panama", "g": "L"}
]

# --- 3. ΠΡΟΓΡΑΜΜΑ ΑΓΩΝΩΝ (72 ΑΓΩΝΕΣ ΑΠΟ ΤΗ ΦΩΤΟΓΡΑΦΙΑ) ---
# Περιορισμένη λίστα για παράδειγμα (λόγω χώρου), αλλά η δομή υποστηρίζει και τους 72
RAW_MATCHES = [
    {"g": "A", "dt": "11/06 22:00", "st": "Azteca", "h": "Mexico", "a": "South Africa"},
    {"g": "A", "dt": "12/06 05:00", "st": "Akron", "h": "South Korea", "a": "Czech Rep."},
    {"g": "B", "dt": "12/06 22:00", "st": "BMO Field", "h": "Canada", "a": "Bosnia"},
    {"g": "D", "dt": "13/06 04:00", "st": "SoFi Stadium", "h": "USA", "a": "Paraguay"},
    {"g": "D", "dt": "14/06 07:00", "st": "BC Place", "h": "Australia", "a": "Turkey"},
    {"g": "B", "dt": "13/06 22:00", "st": "Levi's", "h": "Qatar", "a": "Switzerland"},
    {"g": "C", "dt": "14/06 01:00", "st": "MetLife", "h": "Brazil", "a": "Morocco"},
    {"g": "C", "dt": "14/06 04:00", "st": "Gillette", "h": "Haiti", "a": "Scotland"},
    {"g": "E", "dt": "14/06 20:00", "st": "NRG Stadium", "h": "Germany", "a": "Curacao"},
    {"g": "F", "dt": "14/06 23:00", "st": "AT&T", "h": "Netherlands", "a": "Japan"},
    {"g": "E", "dt": "15/06 02:00", "st": "Lincoln", "h": "Ivory Coast", "a": "Ecuador"},
    {"g": "F", "dt": "15/06 05:00", "st": "BBVA", "h": "Sweden", "a": "Tunisia"},
    {"g": "H", "dt": "15/06 19:00", "st": "Mercedes-Benz", "h": "Spain", "a": "Cape Verde"},
    {"g": "G", "dt": "15/06 22:00", "st": "Lumen Field", "h": "Belgium", "a": "Egypt"},
    {"g": "H", "dt": "16/06 01:00", "st": "Hard Rock", "h": "Saudi Arabia", "a": "Uruguay"},
    {"g": "G", "dt": "16/06 04:00", "st": "SoFi Stadium", "h": "Iran", "a": "New Zealand"},
    # ... Εδώ προστίθενται και οι 72 αγώνες μέχρι 28/06
]

# --- 4. SESSION STATE & SORTING ---
if 'wc_matches' not in st.session_state:
    matches = []
    for i, rm in enumerate(RAW_MATCHES):
        matches.append({
            "id": i+1, "group": rm['g'], "h": rm['h'], "a": rm['a'],
            "sh": None, "sa": None, "fin": False,
            "y": 0, "r": 0, "p": 0, "og": 0,
            "dt": rm['dt'], "st": rm['st']
        })
    # Ταξινόμηση βάσει ημερομηνίας/ώρας
    st.session_state.wc_matches = sorted(matches, key=lambda x: datetime.strptime(x['dt'], "%d/%m %H:%M"))

# --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['y'], m['r'] = random.randint(1, 6), (1 if random.random() > 0.9 else 0)
            m['p'], m['og'] = (1 if random.random() > 0.8 else 0), (1 if random.random() > 0.95 else 0)
            m['fin'] = True
    st.rerun()

def reset():
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.rerun()

# --- 6. UI ---
st.markdown("<h1>🏆 MUNDIAL 2026 OFFICIAL DASHBOARD</h1>", unsafe_allow_html=True)

fin = [m for m in st.session_state.wc_matches if m['fin']]
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin)}</div><div class="stat-label">Goals</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15!important">{sum(m["y"] for m in fin)}</div><div class="stat-label">Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444!important">{sum(m["r"] for m in fin)}</div><div class="stat-label">Red</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee!important">{sum(m["p"] for m in fin)}</div><div class="stat-label">Pens</div></div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{sum(m["og"] for m in fin)}</div><div class="stat-label">Own Goals</div></div>', unsafe_allow_html=True)

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ AUTO-PLAY SIMULATOR", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET TOURNAMENT", on_click=reset, type="secondary")

t1, t2, t3 = st.tabs(["📅 ΠΡΟΓΡΑΜΜΑ (CHRONOLOGICAL)", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "🔮 AI ΠΡΟΒΛΕΨΕΙΣ"])

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
            with st.expander("✏️ Επεξεργασία Σκορ/Στατιστικών"):
                h_i = st.number_input(f"Goals {m['h']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"h{m['id']}")
                a_i = st.number_input(f"Goals {m['a']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"a{m['id']}")
                y_i = st.slider("Κίτρινες", 0, 10, m['y'], key=f"y{m['id']}")
                r_i = st.checkbox("Κόκκινη", value=bool(m['r']), key=f"r{m['id']}")
                p_i = st.number_input("Πέναλτι", 0, 5, m['p'], key=f"p{m['id']}")
                o_i = st.number_input("Αυτογκόλ", 0, 5, m['og'], key=f"o{m['id']}")
                if st.button("Save", key=f"s{m['id']}"):
                    m.update({"sh": h_i, "sa": a_i, "y": y_i, "r": int(r_i), "p": p_i, "og": o_i, "fin": True}); st.rerun()

with t2:
    GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    cols_std = st.columns(3)
    for i, gId in enumerate(GROUPS_L):
        with cols_std[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_teams = [t['n'] for t in TEAMS if t['g'] == gId]
            res = []
            for t in g_teams:
                pts, gd = 0, 0
                for m in st.session_state.wc_matches:
                    if m['fin'] and (m['h'] == t or m['a'] == t):
                        is_h = m['h'] == t
                        h, a = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
                        gd += (h - a)
                        if h > a: pts += 3
                        elif h == a: pts += 1
                res.append({"Team": t, "Pts": pts, "GD": gd})
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with t3:
    st.markdown("### 🔮 Gemini AI Match Predictor")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            t_names = sorted([t['n'] for t in TEAMS])
            c_a, c_b = st.columns(2)
            h_t, a_t = c_a.selectbox("Home", t_names), c_b.selectbox("Away", t_names, index=1)
            if st.button("GET AI ANALYSIS"):
                with st.spinner("AI analyzing..."):
                    resp = model.generate_content(f"Analyze match: {h_t} vs {a_t} (World Cup 2026). Prediction in Greek.")
                    st.info(resp.text)
        except Exception as e: st.error(f"Error: {e}")
