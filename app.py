import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. CONFIG & CSS (COSMIC THEME) ---
st.set_page_config(page_title="World Cup 2026 Pro", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    h1, h2, h3, h4, h5, h6, .stMarkdown p { color: white !important; font-weight: 700 !important; }
    .stat-card {
        background: #0f172a; border: 1px solid #1e293b; border-radius: 12px;
        padding: 20px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stat-val { font-size: 24px; font-weight: 800; color: #06b6d4; }
    .stat-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; margin-top: 5px; }
    .match-card {
        background: #0f172a; border: 1px solid #1e293b; border-radius: 16px;
        padding: 15px; margin-bottom: 15px;
    }
    .group-tag { font-size: 10px; background: rgba(6, 182, 212, 0.1); color: #22d3ee; padding: 2px 8px; border-radius: 99px; font-weight: bold; }
    button[data-testid="stBaseButton-secondary"] {
        color: black !important; background-color: #f1f5f9 !important; border: none !important;
    }
    button[data-testid="stBaseButton-primary"] {
        color: white !important; background-color: #ef4444 !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ & ΗΜΕΡΟΜΗΝΙΕΣ ---
TEAMS = [
    {"id": "mex", "name": "Mexico", "group": "A"}, {"id": "rsa", "name": "South Africa", "group": "A"}, {"id": "kor", "name": "South Korea", "group": "A"}, {"id": "cze", "name": "Czech Rep.", "group": "A"},
    {"id": "can", "name": "Canada", "group": "B"}, {"id": "bih", "name": "Bosnia", "group": "B"}, {"id": "qat", "name": "Qatar", "group": "B"}, {"id": "sui", "name": "Switzerland", "group": "B"},
    {"id": "bra", "name": "Brazil", "group": "C"}, {"id": "mar", "name": "Morocco", "group": "C"}, {"id": "hai", "name": "Haiti", "group": "C"}, {"id": "sco", "name": "Scotland", "group": "C"},
    {"id": "usa", "name": "USA", "group": "D"}, {"id": "par", "name": "Paraguay", "group": "D"}, {"id": "aus", "name": "Australia", "group": "D"}, {"id": "tur", "name": "Turkey", "group": "D"},
    {"id": "ger", "name": "Germany", "group": "E"}, {"id": "cur", "name": "Curacao", "group": "E"}, {"id": "civ", "name": "Ivory Coast", "group": "E"}, {"id": "ecu", "name": "Ecuador", "group": "E"},
    {"id": "ned", "name": "Netherlands", "group": "F"}, {"id": "jpn", "name": "Japan", "group": "F"}, {"id": "swe", "name": "Sweden", "group": "F"}, {"id": "tun", "name": "Tunisia", "group": "F"},
    {"id": "bel", "name": "Belgium", "group": "G"}, {"id": "egy", "name": "Egypt", "group": "G"}, {"id": "irn", "name": "Iran", "group": "G"}, {"id": "nzl", "name": "New Zealand", "group": "G"},
    {"id": "esp", "name": "Spain", "group": "H"}, {"id": "cpv", "name": "Cape Verde", "group": "H"}, {"id": "ksa", "name": "Saudi Arabia", "group": "H"}, {"id": "ury", "name": "Uruguay", "group": "H"},
    {"id": "fra", "name": "France", "group": "I"}, {"id": "sen", "name": "Senegal", "group": "I"}, {"id": "irq", "name": "Iraq", "group": "I"}, {"id": "nor", "name": "Norway", "group": "I"},
    {"id": "arg", "name": "Argentina", "group": "J"}, {"id": "alg", "name": "Algeria", "group": "J"}, {"id": "aut", "name": "Austria", "group": "J"}, {"id": "jor", "name": "Jordan", "group": "J"},
    {"id": "por", "name": "Portugal", "group": "K"}, {"id": "cog", "name": "Congo", "group": "K"}, {"id": "uzb", "name": "Uzbekistan", "group": "K"}, {"id": "col", "name": "Colombia", "group": "K"},
    {"id": "eng", "name": "England", "group": "L"}, {"id": "cro", "name": "Croatia", "group": "L"}, {"id": "gha", "name": "Ghana", "group": "L"}, {"id": "pan", "name": "Panama", "group": "L"}
]
GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
STADIUMS = ["MetLife", "Azteca", "BC Place", "SoFi", "Mercedes-Benz", "Hard Rock"]
DATES = [
    "2026-06-11 21:00", "2026-06-12 18:00", "2026-06-12 21:00", "2026-06-13 15:00", "2026-06-13 18:00", "2026-06-13 21:00",
    "2026-06-14 15:00", "2026-06-14 18:00", "2026-06-14 21:00", "2026-06-15 15:00", "2026-06-15 18:00", "2026-06-15 21:00",
    "2026-06-16 15:00", "2026-06-16 18:00", "2026-06-16 21:00", "2026-06-17 15:00", "2026-06-17 18:00", "2026-06-17 21:00",
    "2026-06-18 15:00", "2026-06-18 18:00", "2026-06-18 21:00", "2026-06-19 15:00", "2026-06-19 18:00", "2026-06-19 21:00",
    "2026-06-20 15:00", "2026-06-20 18:00", "2026-06-20 21:00", "2026-06-21 15:00", "2026-06-21 18:00", "2026-06-21 21:00",
    "2026-06-22 18:00", "2026-06-22 21:00", "2026-06-23 18:00", "2026-06-23 21:00", "2026-06-24 18:00", "2026-06-24 21:00",
    "2026-06-25 18:00", "2026-06-25 21:00", "2026-06-26 18:00", "2026-06-26 21:00", "2026-06-27 18:00", "2026-06-27 21:00"
]

# --- 3. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    match_counter = 0
    for gId in GROUPS:
        g_teams = [t for t in TEAMS if t['group'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for i, (h, a) in enumerate(pairs):
            match_date = DATES[match_counter % len(DATES)]
            match_stadium = STADIUMS[match_counter % len(STADIUMS)]
            matches.append({
                "id": f"{gId}_m{i+1}", "group": gId, "home": g_teams[h], "away": g_teams[a],
                "score_h": None, "score_a": None, "finished": False,
                "yellow": 0, "red": 0, "pens": 0, "og": 0,
                "date": match_date, "stadium": match_stadium
            })
            match_counter += 1
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_simulate():
    for m in st.session_state.wc_matches:
        if not m['finished']:
            m.update({'score_h': random.randint(0,4), 'score_a': random.randint(0,4), 'yellow': random.randint(0,6), 'finished': True})
    st.rerun()

def reset_all():
    del st.session_state['wc_matches']
    st.rerun()

# --- 5. UI ---
st.title("🏆 MUNDIAL 2026 PRO DASHBOARD")

finished = [m for m in st.session_state.wc_matches if m['finished']]
totals = {
    'goals': sum(m['score_h'] + m['score_a'] for m in finished),
    'y': sum(m['yellow'] for m in finished), 'r': sum(m['red'] for m in finished),
    'p': sum(m['pens'] for m in finished), 'og': sum(m['og'] for m in finished)
}

c = st.columns(6)
c[0].markdown(f'<div class="stat-card"><div class="stat-val">{len(finished)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
c[1].markdown(f'<div class="stat-card"><div class="stat-val">{totals["goals"]}</div><div class="stat-label">Goals</div></div>', unsafe_allow_html=True)
c[2].markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15">{totals["y"]}</div><div class="stat-label">Yellow</div></div>', unsafe_allow_html=True)
c[3].markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444">{totals["r"]}</div><div class="stat-label">Red</div></div>', unsafe_allow_html=True)
c[4].markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee">{totals["p"]}</div><div class="stat-label">Penalties</div></div>', unsafe_allow_html=True)
c[5].markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c">{totals["og"]}</div><div class="stat-label">Own Goals</div></div>', unsafe_allow_html=True)

b1, b2 = st.columns([2, 1]);
b1.button("⚡ AUTO-PLAY TOURNAMENT SIMULATOR", on_click=auto_simulate, type="primary")
b2.button("🔄 RESET ALL", on_click=reset_all, type="secondary")

tab1, tab2, tab3 = st.tabs(["📅 CALENDAR", "📊 STANDINGS", "🧠 AI PREDICTIONS"])

with tab1:
    g_filter = st.selectbox("Filter by Group:", ["All"] + GROUPS)
    display_matches = sorted(
        [m for m in st.session_state.wc_matches if g_filter == "All" or m['group'] == g_filter],
        key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M')
    )
    cols = st.columns(3)
    for idx, m in enumerate(display_matches):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">📅 {m['date']}</span>
                </div>
                <div style="display:flex; align-items:center; padding: 10px 0;">
                    <div style="width:40%; text-align:right; font-weight:bold;">{m['home']['name']}</div>
                    <div style="font-size: 24px; color: #06b6d4; margin: 0 10px;">{m['score_h'] or '-'} : {m['score_a'] or '-'}</div>
                    <div style="width:40%; text-align:left; font-weight:bold;">{m['away']['name']}</div>
                </div>
                <div style="font-size:10px; color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:5px;">
                    🏟️ {m['stadium']} | 🟨 {m['yellow']} | 🟥 {m['red']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Score & Stats"):
                h, a = st.columns(2)
                h_val = h.number_input(f"Goals {m['home']['name']}", 0, 15, key=f"h_{m['id']}")
                a_val = a.number_input(f"Goals {m['away']['name']}", 0, 15, key=f"a_{m['id']}")
                y_val = st.slider("Yellow Cards", 0, 10, m['yellow'], key=f"y_{m['id']}")
                r_val = st.checkbox("Red Card", value=bool(m['red']), key=f"r_{m['id']}")
                if st.button("Save", key=f"b_{m['id']}"):
                    m.update({"score_h": h_val, "score_a": a_val, "yellow": y_val, "red": int(r_val), "finished": True})
                    st.rerun()

with tab2:
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS):
        with cols[i % 3]:
            st.markdown(f"### Group {gId}")
            g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
            res = []
            for t in g_teams:
                stats = {"Team": t['name'], "Pts": 0, "GD": 0, "GF": 0}
                for m in st.session_state.wc_matches:
                    if m['finished'] and (m['home']['id'] == t['id'] or m['away']['id'] == t['id']):
                        is_h = m['home']['id'] == t['id']
                        th, ta = (m['score_h'], m['score_a']) if is_h else (m['score_a'], m['score_h'])
                        stats["GF"] += th; stats["GD"] += (th - ta)
                        if th > ta: stats["Pts"] += 3
                        elif th == ta: stats["Pts"] += 1
                res.append(stats)
            df = pd.DataFrame(res).sort_values(by=["Pts", "GD", "GF"], ascending=False)
            st.table(df)

with tab3:
    st.markdown("### 🔮 Gemini AI Expert Analyst")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            t_list = sorted([t['name'] for t in INITIAL_TEAMS])
            c1, c2 = st.columns(2)
            home = c1.selectbox("Home Team", t_list)
            away = c2.selectbox("Away Team", t_list, index=1)
            
            if st.button("GENERATE PRO PREDICTION"):
                with st.spinner("AI is analyzing..."):
                    response = model.generate_content(f"Analyze World Cup 2026 match: {home} vs {away}. Prediction score and card probability in Greek.")
                    st.info(response.text)
        except Exception as e: st.error(f"Error: {e}")
    else: st.error("Add GEMINI_API_KEY to secrets.")
