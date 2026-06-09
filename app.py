import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (COSMIC THEME & FIXED COLORS) ---
st.set_page_config(page_title="World Cup 2026 Greek Portal", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Τίτλοι & Κείμενα (Λευκά) */
    h1, h2, h3, h4, h5, h6, label, .stMarkdown p, .stSelectbox label { color: white !important; font-weight: 700 !important; }
    
    /* Dashboard Cards */
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stat-val { font-size: 24px; font-weight: 800; color: #06b6d4; font-family: 'Monaco', monospace; }
    .stat-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }

    /* Match Card */
    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .group-tag { font-size: 10px; background: rgba(6, 182, 212, 0.1); color: #22d3ee; padding: 2px 8px; border-radius: 99px; font-weight: bold; }
    .time-tag { font-size: 11px; color: #94a3b8; font-family: monospace; }

    /* Tables (Λευκά Γράμματα) */
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; background-color: #0f172a !important; }

    /* Διορθωμένο Κουμπί Reset (Μαύρα Γράμματα) */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Κουμπί Auto-Play (Λευκά Γράμματα) */
    button[data-testid="stBaseButton-primary"] {
        color: white !important;
        background-color: #ef4444 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ (48 ΟΜΑΔΕΣ - ΕΛΛΗΝΙΚΑ) ---
INITIAL_TEAMS = [
    {"id": "mex", "name": "Μεξικό", "group": "A"}, {"id": "rsa", "name": "Νότια Αφρική", "group": "A"}, {"id": "kor", "name": "Νότια Κορέα", "group": "A"}, {"id": "cze", "name": "Τσεχία", "group": "A"},
    {"id": "can", "name": "Καναδάς", "group": "B"}, {"id": "bih", "name": "Βοσνία", "group": "B"}, {"id": "qat", "name": "Κατάρ", "group": "B"}, {"id": "sui", "name": "Ελβετία", "group": "B"},
    {"id": "bra", "name": "Βραζιλία", "group": "C"}, {"id": "mar", "name": "Μαρόκο", "group": "C"}, {"id": "hai", "name": "Αϊτή", "group": "C"}, {"id": "sco", "name": "Σκωτία", "group": "C"},
    {"id": "usa", "name": "ΗΠΑ", "group": "D"}, {"id": "par", "name": "Παραγουάη", "group": "D"}, {"id": "aus", "name": "Αυστραλία", "group": "D"}, {"id": "tur", "name": "Τουρκία", "group": "D"},
    {"id": "ger", "name": "Γερμανία", "group": "E"}, {"id": "cur", "name": "Κουρασάο", "group": "E"}, {"id": "civ", "name": "Ακτή Ελεφαντοστού", "group": "E"}, {"id": "ecu", "name": "Εκουαδόρ", "group": "E"},
    {"id": "ned", "name": "Ολλανδία", "group": "F"}, {"id": "jpn", "name": "Ιαπωνία", "group": "F"}, {"id": "swe", "name": "Σουηδία", "group": "F"}, {"id": "tun", "name": "Τυνησία", "group": "F"},
    {"id": "bel", "name": "Βέλγιο", "group": "G"}, {"id": "egy", "name": "Αίγυπτος", "group": "G"}, {"id": "irn", "name": "Ιράν", "group": "G"}, {"id": "nzl", "name": "Νέα Ζηλανδία", "group": "G"},
    {"id": "esp", "name": "Ισπανία", "group": "H"}, {"id": "cpv", "name": "Πράσινο Ακρωτήρι", "group": "H"}, {"id": "ksa", "name": "Σαουδική Αραβία", "group": "H"}, {"id": "ury", "name": "Ουρουγουάη", "group": "H"},
    {"id": "fra", "name": "Γαλλία", "group": "I"}, {"id": "sen", "name": "Σενεγάλη", "group": "I"}, {"id": "irq", "name": "Ιράκ", "group": "I"}, {"id": "nor", "name": "Νορβηγία", "group": "I"},
    {"id": "arg", "name": "Αργεντινή", "group": "J"}, {"id": "alg", "name": "Αλγερία", "group": "J"}, {"id": "aut", "name": "Αυστρία", "group": "J"}, {"id": "jor", "name": "Ιορδανία", "group": "J"},
    {"id": "por", "name": "Πορτογαλία", "group": "K"}, {"id": "cog", "name": "Κονγκό", "group": "K"}, {"id": "uzb", "name": "Ουζμπεκιστάν", "group": "K"}, {"id": "col", "name": "Κολομβία", "group": "K"},
    {"id": "eng", "name": "Αγγλία", "group": "L"}, {"id": "cro", "name": "Κροατία", "group": "L"}, {"id": "gha", "name": "Γκάνα", "group": "L"}, {"id": "pan", "name": "Παναμάς", "group": "L"}
]

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# --- 3. SESSION STATE (DATABASE ΜΕ ΗΜΕΡΟΜΗΝΙΕΣ) ---
if 'wc_matches' not in st.session_state:
    matches = []
    # Ορισμός έναρξης: 11 Ιουνίου 2026, 22:00
    start_time = datetime(2026, 6, 11, 22, 0)
    match_count = 0
    
    for gId in GROUPS:
        g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for i, (h, a) in enumerate(pairs):
            # Υπολογισμός ώρας: Κάθε 3 αγώνες αλλάζει μέρα, ώρες 22:00, 01:00, 04:00
            offset_hours = (match_count // 3) * 24 + (match_count % 3) * 3
            m_time = start_time + timedelta(hours=offset_hours)
            
            matches.append({
                "id": f"{gId}_m{i+1}", "group": gId, "home": g_teams[h], "away": g_teams[a],
                "score_h": None, "score_a": None, "finished": False,
                "yellow": 0, "red": 0, "pens": 0, "og": 0,
                "time": m_time.strftime("%d/%m %H:%M")
            })
            match_count += 1
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
st.markdown("<h1>🏆 MUNDIAL 2026 PRO DASHBOARD</h1>", unsafe_allow_html=True)

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
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span class="time-tag">🕒 {m['time']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding: 10px 0;">
                    <div style="width:40%; text-align:center; font-weight:bold; color:white; font-size:14px;">{m['home']['name']}</div>
                    <div style="font-size: 22px; color: #06b6d4; font-weight: 800;">{m['score_h'] if m['score_h'] is not None else '-'} : {m['score_a'] if m['score_a'] is not None else '-'}</div>
                    <div style="width:40%; text-align:center; font-weight:bold; color:white; font-size:14px;">{m['away']['name']}</div>
                </div>
                <div style="font-size:10px; color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:5px;">
                    🟨 {m['yellow']} | 🟥 {m['red']} | 🎯 {m['pens']} | ⚠️ {m['og']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Details"):
                h = st.number_input(f"Goals {m['home']['name']}", 0, 15, m['score_h'] if m['score_h'] is not None else 0, key=f"h_{m['id']}")
                a = st.number_input(f"Goals {m['away']['name']}", 0, 15, m['score_a'] if m['score_a'] is not None else 0, key=f"a_{m['id']}")
                y = st.slider("Yellow Cards", 0, 10, m['yellow'], key=f"y_{m['id']}")
                r = st.checkbox("Red Card", value=bool(m['red']), key=f"r_{m['id']}")
                if st.button("Save", key=f"b_{m['id']}"):
                    m.update({"score_h": h, "score_a": a, "yellow": y, "red": int(r), "finished": True})
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
                res.append({"Team": t['name'], "Pts": pts, "GD": (gf-ga)})
            df = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
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
        except Exception as e: st.error(f"Error: {e}")
    else: st.error("Add GEMINI_API_KEY to secrets.")
