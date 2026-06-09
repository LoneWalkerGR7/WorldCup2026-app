import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (COSMIC THEME - WHITE TEXT) ---
st.set_page_config(page_title="World Cup 2026 Pro Portal", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Κατάσπρα γράμματα παντού (Τίτλοι, Labels, Πίνακες) */
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { 
        color: white !important; 
        font-weight: 600 !important; 
    }
    
    /* Dashboard Stats */
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stat-val { font-size: 22px; font-weight: 800; color: #06b6d4 !important; }

    /* Match Cards */
    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    
    /* Reset Button: BLACK TEXT */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        font-weight: 800 !important;
        border: none !important;
    }
    
    /* Auto-Play Button */
    button[data-testid="stBaseButton-primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
    }

    /* Tables White Text Fix */
    div[data-testid="stTable"] table { color: white !important; }
    div[data-testid="stTable"] thead tr th { color: #06b6d4 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS = [
    {"n": "Μεξικό", "g": "A"}, {"n": "Νότια Αφρική", "g": "A"}, {"n": "Νότια Κορέα", "g": "A"}, {"n": "Τσεχία", "g": "A"},
    {"n": "Καναδάς", "g": "B"}, {"n": "Βοσνία", "g": "B"}, {"n": "Κατάρ", "g": "B"}, {"n": "Ελβετία", "g": "B"},
    {"n": "Βραζιλία", "g": "C"}, {"n": "Μαρόκο", "g": "C"}, {"n": "Αϊτή", "g": "C"}, {"n": "Σκωτία", "g": "C"},
    {"n": "ΗΠΑ", "g": "D"}, {"n": "Παραγουάη", "g": "D"}, {"n": "Αυστραλία", "g": "D"}, {"n": "Τουρκία", "g": "D"},
    {"n": "Γερμανία", "g": "E"}, {"n": "Κουρασάο", "g": "E"}, {"n": "Ακτή Ελεφαντοστού", "g": "E"}, {"n": "Εκουαδόρ", "g": "E"},
    {"n": "Ολλανδία", "g": "F"}, {"n": "Ιαπωνία", "g": "F"}, {"n": "Σουηδία", "g": "F"}, {"n": "Τυνησία", "g": "F"},
    {"n": "Βέλγιο", "g": "G"}, {"n": "Αίγυπτος", "g": "G"}, {"n": "Ιράν", "g": "G"}, {"n": "Νέα Ζηλανδία", "g": "G"},
    {"n": "Ισπανία", "g": "H"}, {"n": "Πράσινο Ακρωτήρι", "g": "H"}, {"n": "Σαουδική Αραβία", "g": "H"}, {"n": "Ουρουγουάη", "g": "H"},
    {"n": "Γαλλία", "g": "I"}, {"n": "Σενεγάλη", "g": "I"}, {"n": "Ιράκ", "g": "I"}, {"n": "Νορβηγία", "g": "I"},
    {"n": "Αργεντινή", "g": "J"}, {"n": "Αλγερία", "g": "J"}, {"n": "Αυστρία", "g": "J"}, {"n": "Ιορδανία", "g": "J"},
    {"n": "Πορτογαλία", "g": "K"}, {"n": "Κονγκό", "g": "K"}, {"n": "Ουζμπεκιστάν", "g": "K"}, {"n": "Κολομβία", "g": "K"},
    {"n": "Αγγλία", "g": "L"}, {"n": "Κροατία", "g": "L"}, {"n": "Γκάνα", "g": "L"}, {"n": "Παναμάς", "g": "L"}
]

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# --- 3. SESSION STATE (72 MATCHES) ---
if 'wc_matches' not in st.session_state:
    matches = []
    start_date = datetime(2026, 6, 11, 22, 0)
    match_id = 1
    for gId in GROUPS:
        g_teams = [t for t in TEAMS if t['g'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for p_idx, (h, a) in enumerate(pairs):
            day_off = GROUPS.index(gId) + (p_idx * 3)
            time_m = start_date + timedelta(days=day_off, hours=(match_id % 4)*3)
            matches.append({
                "id": match_id, "group": gId, "h": g_teams[h]['n'], "a": g_teams[a]['n'],
                "sh": None, "sa": None, "fin": False,
                "y": 0, "r": 0, "p": 0, "og": 0, "dt": time_m.strftime("%d/%m %H:%M")
            })
            match_id += 1
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['y'], m['r'] = random.randint(1, 6), (1 if random.random() > 0.9 else 0)
            m['p'], m['og'] = (1 if random.random() > 0.85 else 0), (1 if random.random() > 0.96 else 0)
            m['fin'] = True
    st.rerun()

def reset():
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.rerun()

# --- 5. DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO DASHBOARD</h1>", unsafe_allow_html=True)
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
with b1: st.button("⚡ AUTO-PLAY TOURNAMENT SIMULATOR", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL", on_click=reset, type="secondary")

# --- 6. TABS ---
t1, t2, t3 = st.tabs(["📅 CALENDAR", "📊 STANDINGS", "🔮 AI PREDICTIONS"])

with t1:
    display = st.session_state.wc_matches
    cols = st.columns(3)
    for idx, m in enumerate(display):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center;">
                    <div style="width:40%; text-align:center; font-weight:bold;">{m['h']}</div>
                    <div style="font-size:20px; color:#06b6d4; font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="width:40%; text-align:center; font-weight:bold;">{m['a']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Score"):
                h_i = st.number_input(f"Goals {m['h']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"h{m['id']}")
                a_i = st.number_input(f"Goals {m['a']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"a{m['id']}")
                if st.button("Save", key=f"s{m['id']}"):
                    m.update({"sh": h_i, "sa": a_i, "fin": True}); st.rerun()

with t2:
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS):
        with cols[i % 3]:
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
    st.markdown("### 🔮 Gemini AI Expert Analyst")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            # ΔΙΟΡΘΩΣΗ: Χρησιμοποιούμε απευθείας το 1.5-flash για αποφυγή 404
            model = genai.GenerativeModel('gemini-1.5-flash')
            t_names = sorted([t['n'] for t in TEAMS])
            c1, c2 = st.columns(2)
            h_t, a_t = c1.selectbox("Home", t_names), c2.selectbox("Away", t_names, index=1)
            if st.button("GENERATE PRO PREDICTION"):
                with st.spinner("AI analyzing..."):
                    resp = model.generate_content(f"Analyze match: {h_t} vs {a_t} (World Cup 2026). Prediction score in Greek.")
                    st.info(resp.text)
        except Exception as e: st.error(f"Error: {e}")
    else: st.error("No API Key found.")
