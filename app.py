import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os

# --- 1. CONFIG & CSS (ΠΛΗΡΗΣ ΔΙΟΡΘΩΣΗ) ---
st.set_page_config(page_title="World Cup 2026 Pro", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    /* Φόντο Εφαρμογής */
    .stApp { background-color: #020617; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Τίτλοι Ομίλων (Καθαρό Λευκό) */
    h1, h2, h3, h4, h5, h6, .stMarkdown p { color: white !important; font-weight: 700 !important; }
    
    /* Dashboard Stats Cards */
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stat-val { font-size: 24px; font-weight: 800; color: #06b6d4; font-family: 'Monaco', monospace; }
    .stat-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }

    /* Match Box Design */
    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .group-tag { font-size: 10px; background: rgba(6, 182, 212, 0.1); color: #22d3ee; padding: 2px 8px; border-radius: 99px; font-weight: bold; }
    
    /* Πίνακες Βαθμολογίας (Λευκά Γράμματα) */
    [data-testid="stTable"] { color: white !important; }
    table { color: white !important; }
    
    /* ΔΙΟΡΘΩΣΗ: Κουμπί Reset All (Μαύρα Γράμματα) */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    /* Κουμπί Auto-Play */
    button[data-testid="stBaseButton-primary"] {
        color: white !important;
        background-color: #ef4444 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ (48 ΟΜΑΔΕΣ) ---
INITIAL_TEAMS = [
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

# --- 3. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    for gId in GROUPS:
        g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for i, (h, a) in enumerate(pairs):
            matches.append({
                "id": f"{gId}_m{i+1}", "group": gId, "home": g_teams[h], "away": g_teams[a],
                "score_h": None, "score_a": None, "finished": False,
                "yellow": 0, "red": 0, "pens": 0, "og": 0
            })
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_simulate():
    for m in st.session_state.wc_matches:
        if not m['finished']:
            m['score_h'], m['score_a'] = random.randint(0, 4), random.randint(0, 4)
            m['yellow'] = random.randint(1, 6)
            m['red'] = 1 if random.random() > 0.9 else 0
            m['pens'] = random.randint(0, 1) if random.random() > 0.8 else 0
            m['og'] = 1 if random.random() > 0.95 else 0
            m['finished'] = True
    st.rerun()

def reset_all():
    if 'wc_matches' in st.session_state:
        del st.session_state['wc_matches']
    st.rerun()

# --- 5. HEADER & DASHBOARD ---
st.title("🏆 MUNDIAL 2026 PRO DASHBOARD")

finished = [m for m in st.session_state.wc_matches if m['finished']]
total_goals = sum(m['score_h'] + m['score_a'] for m in finished)
total_y = sum(m['yellow'] for m in finished)
total_r = sum(m['red'] for m in finished)
total_p = sum(m['pens'] for m in finished)
total_og = sum(m['og'] for m in finished)

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(finished)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{total_goals}</div><div class="stat-label">Goals</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15">{total_y}</div><div class="stat-label">Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444">{total_r}</div><div class="stat-label">Red</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee">{total_p}</div><div class="stat-label">Penalties</div></div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c">{total_og}</div><div class="stat-label">Own Goals</div></div>', unsafe_allow_html=True)

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ AUTO-PLAY TOURNAMENT SIMULATOR", on_click=auto_simulate, type="primary")
with b2: st.button("🔄 RESET ALL", on_click=reset_all, type="secondary")

# --- 6. TABS ---
tab1, tab2, tab3 = st.tabs(["📅 CALENDAR & LIVE STATS", "📊 GROUP STANDINGS", "🧠 AI PREDICTIONS"])

with tab1:
    g_filter = st.selectbox("Filter by Group:", ["All"] + GROUPS)
    display_matches = [m for m in st.session_state.wc_matches if g_filter == "All" or m['group'] == g_filter]
    cols = st.columns(3)
    for idx, m in enumerate(display_matches):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:10px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="color: #10b981; font-weight: bold; font-size: 10px;">{'FINISHED' if m['finished'] else ''}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center;">
                    <div style="width:40%; text-align:center; font-weight:bold; color:white;">{m['home']['name']}</div>
                    <div style="font-size: 24px; color: #06b6d4; font-weight: 800;">{m['score_h'] if m['score_h'] is not None else '-'} : {m['score_a'] if m['score_a'] is not None else '-'}</div>
                    <div style="width:40%; text-align:center; font-weight:bold; color:white;">{m['away']['name']}</div>
                </div>
                <div style="font-size:10px; color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; margin-top:10px; padding-top:5px;">
                    🟨 {m['yellow']} | 🟥 {m['red']} | 🎯 {m['pens']} | ⚠️ {m['og']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Details"):
                h = st.number_input(f"Goals {m['home']['name']}", 0, 15, m['score_h'] if m['score_h'] is not None else 0, key=f"h_{m['id']}")
                a = st.number_input(f"Goals {m['away']['name']}", 0, 15, m['score_a'] if m['score_a'] is not None else 0, key=f"a_{m['id']}")
                y = st.slider("Yellow Cards", 0, 10, m['yellow'], key=f"y_{m['id']}")
                r = st.checkbox("Red Card", value=bool(m['red']), key=f"r_{m['id']}")
                p = st.number_input("Penalties", 0, 5, m['pens'], key=f"p_{m['id']}")
                o = st.number_input("Own Goals", 0, 5, m['og'], key=f"o_{m['id']}")
                if st.button("Save", key=f"b_{m['id']}"):
                    m.update({"score_h": h, "score_a": a, "yellow": y, "red": int(r), "pens": p, "og": o, "finished": True})
                    st.rerun()

with tab2:
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS):
        with cols[i % 3]:
            st.markdown(f"### Group {gId}")
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
                res.append({"Team": t['name'], "Pts": pts, "GD": (gf-ga), "GF": gf})
            df = pd.DataFrame(res).sort_values(by=["Pts", "GD", "GF"], ascending=False)
            st.table(df)

with tab3:
    st.markdown("### 🔮 Gemini AI Expert Analyst")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model_id = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else 'models/gemini-pro'
            model = genai.GenerativeModel(model_id)
            
            t_list = sorted([t['name'] for t in INITIAL_TEAMS])
            c1, c2 = st.columns(2)
            home = c1.selectbox("Home Team", t_list)
            away = c2.selectbox("Away Team", t_list, index=1)
            
            if st.button("GENERATE PRO PREDICTION"):
                with st.spinner("AI is analyzing tactics..."):
                    response = model.generate_content(f"Analyze World Cup 2026 match: {home} vs {away}. Prediction score and card probability in Greek.")
                    st.info(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else: st.error("Add GEMINI_API_KEY to secrets.")
