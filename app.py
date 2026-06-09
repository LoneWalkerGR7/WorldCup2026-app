import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="Mundial 2026 Portal", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .header-container {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        padding: 2rem;
        border-bottom: 1px solid #1e293b;
        border-radius: 0 0 20px 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }
    .stat-val { font-size: 2rem; font-weight: 800; color: #06b6d4; }
    .stat-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }
    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .group-tag { font-size: 10px; background: rgba(6, 182, 212, 0.1); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.2); padding: 2px 8px; border-radius: 99px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΤΕΛΙΚΟΙ ΟΜΙΛΟΙ (ΚΑΘΑΡΟΙ ΧΑΡΑΚΤΗΡΕΣ) ---
INITIAL_TEAMS = [
    # Group A
    {"id": "mex", "name": "Mexico", "group": "A"},
    {"id": "rsa", "name": "South Africa", "group": "A"},
    {"id": "kor", "name": "South Korea", "group": "A"},
    {"id": "cze", "name": "Czech Republic", "group": "A"},
    # Group B
    {"id": "can", "name": "Canada", "group": "B"},
    {"id": "bih", "name": "Bosnia", "group": "B"},
    {"id": "qat", "name": "Qatar", "group": "B"},
    {"id": "sui", "name": "Switzerland", "group": "B"},
    # Group C
    {"id": "bra", "name": "Brazil", "group": "C"},
    {"id": "mar", "name": "Morocco", "group": "C"},
    {"id": "hai", "name": "Haiti", "group": "C"},
    {"id": "sco", "name": "Scotland", "group": "C"},
    # Group D
    {"id": "usa", "name": "USA", "group": "D"},
    {"id": "par", "name": "Paraguay", "group": "D"},
    {"id": "aus", "name": "Australia", "group": "D"},
    {"id": "tur", "name": "Turkey", "group": "D"},
    # Group E
    {"id": "ger", "name": "Germany", "group": "E"},
    {"id": "cur", "name": "Curacao", "group": "E"},
    {"id": "civ", "name": "Ivory Coast", "group": "E"},
    {"id": "ecu", "name": "Ecuador", "group": "E"},
    # Group F
    {"id": "ned", "name": "Netherlands", "group": "F"},
    {"id": "jpn", "name": "Japan", "group": "F"},
    {"id": "swe", "name": "Sweden", "group": "F"},
    {"id": "tun", "name": "Tunisia", "group": "F"},
    # Group G
    {"id": "bel", "name": "Belgium", "group": "G"},
    {"id": "egy", "name": "Egypt", "group": "G"},
    {"id": "irn", "name": "Iran", "group": "G"},
    {"id": "nzl", "name": "New Zealand", "group": "G"},
    # Group H
    {"id": "esp", "name": "Spain", "group": "H"},
    {"id": "cpv", "name": "Cape Verde", "group": "H"},
    {"id": "ksa", "name": "Saudi Arabia", "group": "H"},
    {"id": "ury", "name": "Uruguay", "group": "H"},
    # Group I
    {"id": "fra", "name": "France", "group": "I"},
    {"id": "sen", "name": "Senegal", "group": "I"},
    {"id": "irq", "name": "Iraq", "group": "I"},
    {"id": "nor", "name": "Norway", "group": "I"},
    # Group J
    {"id": "arg", "name": "Argentina", "group": "J"},
    {"id": "alg", "name": "Algeria", "group": "J"},
    {"id": "aut", "name": "Austria", "group": "J"},
    {"id": "jor", "name": "Jordan", "group": "J"},
    # Group K
    {"id": "por", "name": "Portugal", "group": "K"},
    {"id": "cog", "name": "Congo", "group": "K"},
    {"id": "uzb", "name": "Uzbekistan", "group": "K"},
    {"id": "col", "name": "Colombia", "group": "K"},
    # Group L
    {"id": "eng", "name": "England", "group": "L"},
    {"id": "cro", "name": "Croatia", "group": "L"},
    {"id": "gha", "name": "Ghana", "group": "L"},
    {"id": "pan", "name": "Panama", "group": "L"}
]

GROUPS_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# --- 3. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    for gId in GROUPS_LIST:
        g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for i, (h, a) in enumerate(pairs):
            matches.append({
                "id": f"{gId}_m{i+1}", "group": gId,
                "home": g_teams[h], "away": g_teams[a],
                "score_h": None, "score_a": None, "finished": False
            })
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_simulate():
    for m in st.session_state.wc_matches:
        if not m['finished']:
            m['score_h'] = random.randint(0, 4)
            m['score_a'] = random.randint(0, 4)
            m['finished'] = True
    st.rerun()

def reset_all():
    if 'wc_matches' in st.session_state:
        del st.session_state['wc_matches']
    st.rerun()

# --- 5. HEADER ---
st.markdown("""
    <div class="header-container">
        <span style="color: #06b6d4; font-weight: bold;">WORLD CUP 2026 PORTAL</span>
        <h1 style="color: white; margin-top: 10px;">Mundial 2026 Calendar & AI Predictions</h1>
    </div>
    """, unsafe_allow_html=True)

finished = [m for m in st.session_state.wc_matches if m['finished']]
total_goals = sum(m['score_h'] + m['score_a'] for m in finished)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(finished)}/72</div><div class="stat-label">MATCHES</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{total_goals}</div><div class="stat-label">GOALS</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ Auto-Play", on_click=auto_simulate, use_container_width=True)
with c4: st.button("🔄 Reset", on_click=reset_all, use_container_width=True)

# --- 6. TABS ---
tab_cal, tab_std, tab_ai = st.tabs(["📅 Calendar", "🏆 Standings", "🧠 AI Predictions"])

with tab_cal:
    g_filter = st.selectbox("Select Group:", ["All Groups"] + [f"Group {g}" for g in GROUPS_LIST])
    actual_g = g_filter[-1] if "Group " in g_filter else "All"
    
    cols = st.columns(2)
    display_matches = [m for m in st.session_state.wc_matches if actual_g == "All" or m['group'] == actual_g]
    
    for idx, m in enumerate(display_matches):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; align-items:center;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="color: #10b981; font-weight: bold; font-size: 10px;">{'FINISHED' if m['finished'] else ''}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding: 10px 0;">
                    <div style="width:40%; text-align:center;"><b>{m['home']['name']}</b></div>
                    <div style="font-size: 22px; color: #06b6d4; font-weight: 800;">
                        {m['score_h'] if m['score_h'] is not None else '-'} : {m['score_a'] if m['score_a'] is not None else '-'}
                    </div>
                    <div style="width:40%; text-align:center;"><b>{m['away']['name']}</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Score"):
                h = st.number_input(f"Goals {m['home']['name']}", 0, 15, key=f"h_{m['id']}")
                a = st.number_input(f"Goals {m['away']['name']}", 0, 15, key=f"a_{m['id']}")
                if st.button("Save Result", key=f"b_{m['id']}"):
                    m.update({"score_h": h, "score_a": a, "finished": True})
                    st.rerun()

with tab_std:
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS_LIST):
        with cols[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
            res = []
            for t in g_teams:
                pts, gf, ga = 0, 0, 0
                for m in st.session_state.wc_matches:
                    if m['finished'] and (m['home']['id'] == t['id'] or m['away']['id'] == t['id']):
                        is_h = m['home']['id'] == t['id']
                        th, ta = (m['score_h'], m['score_a']) if is_h else (m['score_a'], m['score_h'])
                        gf += th; ga += ta
                        if th > ta: pts += 3
                        elif th == ta: pts += 1
                res.append({"Team": t['name'], "Pts": pts, "GD": (gf-ga)})
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with tab_ai:
    st.subheader("AI Predictor")
    t_names = sorted([t['name'] for t in INITIAL_TEAMS])
    c1, c2 = st.columns(2)
    t1 = c1.selectbox("Home Team:", t_names)
    t2 = c2.selectbox("Away Team:", t_names, index=1)
    if st.button("Get AI Prediction"):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            with st.spinner("AI is thinking..."):
                resp = model.generate_content(f"Predict World Cup 2026 match: {t1} vs {t2}. Give score and scorers in Greek.")
                st.info(resp.text)
        else: st.error("API Key missing!")
