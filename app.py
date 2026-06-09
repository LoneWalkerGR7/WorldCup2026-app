import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. CONFIG & CSS (COSMIC SLATE) ---
st.set_page_config(page_title="Mundial 2026 Official Portal", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown { color: white !important; }
    
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stat-val { font-size: 24px; font-weight: 800; color: #06b6d4 !important; }
    
    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .st-venue { font-size: 10px; color: #94a3b8 !important; margin-top: 5px; font-style: italic; }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: white !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
INITIAL_TEAMS = [
    {"id": "mex", "name": "Μεξικό", "flag": "🇲🇽", "group": "A"}, {"id": "rsa", "name": "Νότια Αφρική", "flag": "🇿🇦", "group": "A"}, {"id": "kor", "name": "Νότια Κορέα", "flag": "🇰🇷", "group": "A"}, {"id": "cze", "name": "Τσεχία", "flag": "🇨🇿", "group": "A"},
    {"id": "can", "name": "Καναδάς", "flag": "🇨🇦", "group": "B"}, {"id": "bih", "name": "Βοσνία", "flag": "🇧🇦", "group": "B"}, {"id": "qat", "name": "Κατάρ", "flag": "🇶🇦", "group": "B"}, {"id": "sui", "name": "Ελβετία", "flag": "🇨🇭", "group": "B"},
    {"id": "bra", "name": "Βραζιλία", "flag": "🇧🇷", "group": "C"}, {"id": "mar", "name": "Μαρόκο", "flag": "🇲🇦", "group": "C"}, {"id": "hai", "name": "Αϊτή", "flag": "🇭🇹", "group": "C"}, {"id": "sco", "name": "Σκωτία", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "group": "C"},
    {"id": "usa", "name": "ΗΠΑ", "flag": "🇺🇸", "group": "D"}, {"id": "par", "name": "Παραγουάη", "flag": "🇵🇾", "group": "D"}, {"id": "aus", "name": "Αυστραλία", "flag": "🇦🇺", "group": "D"}, {"id": "tur", "name": "Τουρκία", "flag": "🇹🇷", "group": "D"},
    {"id": "ger", "name": "Γερμανία", "flag": "🇩🇪", "group": "E"}, {"id": "cur", "name": "Κουρασάο", "flag": "🇨🇼", "group": "E"}, {"id": "civ", "name": "Ακτή Ελεφαντοστού", "flag": "🇨🇮", "group": "E"}, {"id": "ecu", "name": "Εκουαδόρ", "flag": "🇪🇨", "group": "E"},
    {"id": "ned", "name": "Ολλανδία", "flag": "🇳🇱", "group": "F"}, {"id": "jpn", "name": "Ιαπωνία", "flag": "🇯🇵", "group": "F"}, {"id": "swe", "name": "Σουηδία", "flag": "🇸🇪", "group": "F"}, {"id": "tun", "name": "Τυνησία", "flag": "🇹🇳", "group": "F"},
    {"id": "bel", "name": "Βέλγιο", "flag": "🇧🇪", "group": "G"}, {"id": "egy", "name": "Αίγυπτος", "flag": "🇪🇬", "group": "G"}, {"id": "irn", "name": "Ιράν", "flag": "🇮🇷", "group": "G"}, {"id": "nzl", "name": "Νέα Ζηλανδία", "flag": "🇳🇿", "group": "G"},
    {"id": "esp", "name": "Ισπανία", "flag": "🇪🇸", "group": "H"}, {"id": "cpv", "name": "Πράσινο Ακρωτήρι", "flag": "🇨🇻", "group": "H"}, {"id": "ksa", "name": "Σαουδική Αραβία", "flag": "🇸🇦", "group": "H"}, {"id": "ury", "name": "Ουρουγουάη", "flag": "🇺🇾", "group": "H"},
    {"id": "fra", "name": "Γαλλία", "flag": "🇫🇷", "group": "I"}, {"id": "sen", "name": "Σενεγάλη", "flag": "🇸🇳", "group": "I"}, {"id": "irq", "name": "Ιράκ", "flag": "🇮🇶", "group": "I"}, {"id": "nor", "name": "Νορβηγία", "flag": "🇳🇴", "group": "I"},
    {"id": "arg", "name": "Αργεντινή", "flag": "🇦🇷", "group": "J"}, {"id": "alg", "name": "Αλγερία", "flag": "🇩🇿", "group": "J"}, {"id": "aut", "name": "Αυστρία", "flag": "🇦🇹", "group": "J"}, {"id": "jor", "name": "Ιορδανία", "flag": "🇯🇴", "group": "J"},
    {"id": "por", "name": "Πορτογαλία", "flag": "🇵🇹", "group": "K"}, {"id": "cog", "name": "Κονγκό", "flag": "🇨🇬", "group": "K"}, {"id": "uzb", "name": "Ουζμπεκιστάν", "flag": "🇺🇿", "group": "K"}, {"id": "col", "name": "Κολομβία", "flag": "🇨🇴", "group": "K"},
    {"id": "eng", "name": "Αγγλία", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group": "L"}, {"id": "cro", "name": "Κροατία", "flag": "🇭🇷", "group": "L"}, {"id": "gha", "name": "Γκάνα", "flag": "🇬🇭", "group": "L"}, {"id": "pan", "name": "Παναμάς", "flag": "🇵🇦", "group": "L"}
]

# --- 3. ΑΥΘΕΝΤΙΚΟ ΠΡΟΓΡΑΜΜΑ (ΑΠΟ ΕΙΚΟΝΑ) ---
RAW_MATCHES = [
    {"id": 1, "group": "A", "date": "11/06 22:00", "stadium": "Estadio Azteca (Mexico City)", "h": "Μεξικό", "a": "Νότια Αφρική"},
    {"id": 2, "group": "A", "date": "12/06 05:00", "stadium": "Estadio Akron (Guadalajara)", "h": "Νότια Κορέα", "a": "Τσεχία"},
    {"id": 3, "group": "B", "date": "12/06 22:00", "stadium": "BMO Field (Toronto)", "h": "Καναδάς", "a": "Βοσνία"},
    {"id": 4, "group": "D", "date": "13/06 04:00", "stadium": "SoFi Stadium (Inglewood)", "h": "ΗΠΑ", "a": "Παραγουάη"},
    {"id": 5, "group": "D", "date": "14/06 07:00", "stadium": "BC Place (Vancouver)", "h": "Αυστραλία", "a": "Τουρκία"},
    {"id": 6, "group": "B", "date": "13/06 22:00", "stadium": "Levi's Stadium (Santa Clara)", "h": "Κατάρ", "a": "Ελβετία"},
    {"id": 7, "group": "C", "date": "14/06 01:00", "stadium": "MetLife Stadium (East Rutherford)", "h": "Βραζιλία", "a": "Μαρόκο"},
    {"id": 8, "group": "C", "date": "14/06 04:00", "stadium": "Gillette Stadium (Foxborough)", "h": "Αϊτή", "a": "Σκωτία"},
    {"id": 9, "group": "E", "date": "14/06 20:00", "stadium": "NRG Stadium (Houston)", "h": "Γερμανία", "a": "Κουρασάο"},
    {"id": 10, "group": "F", "date": "14/06 23:00", "stadium": "AT&T Stadium (Arlington)", "h": "Ολλανδία", "a": "Ιαπωνία"},
    # Προσθέστε περισσότερα εδώ αν χρειαστεί, για τώρα καλύπτουμε τη βάση.
]

# --- 4. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    # Χρησιμοποιούμε τα δεδομένα της εικόνας
    for rm in RAW_MATCHES:
        h_team = next(t for t in INITIAL_TEAMS if t['name'] == rm['h'])
        a_team = next(t for t in INITIAL_TEAMS if t['name'] == rm['a'])
        matches.append({
            "id": rm['id'], "group": rm['group'], "date": rm['date'], 
            "stadium": rm['stadium'], "home": h_team, "away": a_team,
            "score_h": None, "score_a": None, "finished": False,
            "yellow": 0, "red": 0, "pens": 0, "og": 0
        })
    st.session_state.wc_matches = matches

# --- 5. FUNCTIONS ---
def auto_simulate():
    for m in st.session_state.wc_matches:
        if not m['finished']:
            m['score_h'], m['score_a'] = random.randint(0, 4), random.randint(0, 4)
            m['yellow'], m['red'] = random.randint(0, 5), (1 if random.random() > 0.9 else 0)
            m['finished'] = True
    st.rerun()

def reset():
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.rerun()

# --- 6. UI ---
st.title("🏆 MUNDIAL 2026 OFFICIAL PORTAL")

finished = [m for m in st.session_state.wc_matches if m['finished']]
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(finished)}/{len(st.session_state.wc_matches)}</div><div class="stat-label">Matches Played</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["score_h"]+m["score_a"] for m in finished)}</div><div class="stat-label">Total Goals</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ AUTO-PLAY SIMULATOR", on_click=auto_simulate, type="primary")
with c4: st.button("🔄 RESET ALL", on_click=reset, type="secondary")

t1, t2, t3 = st.tabs(["📅 ΠΡΟΓΡΑΜΜΑ ΑΓΩΝΩΝ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "🔮 AI ΠΡΟΒΛΕΨΕΙΣ"])

with t1:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:11px; color:#94a3b8;">🕒 {m['date']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding:12px 0;">
                    <div style="text-align:center; width:40%; font-weight:bold; font-size:14px;">{m['home']['name']}</div>
                    <div style="font-size:22px; color:#06b6d4; font-weight:800;">{m['score_h'] if m['score_h'] is not None else '-'} : {m['score_a'] if m['score_a'] is not None else '-'}</div>
                    <div style="text-align:center; width:40%; font-weight:bold; font-size:14px;">{m['away']['name']}</div>
                </div>
                <div class="st-venue">📍 {m['stadium']}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Εισαγωγή Σκορ"):
                h = st.number_input(f"Goals {m['home']['name']}", 0, 15, key=f"h{m['id']}")
                a = st.number_input(f"Goals {m['away']['name']}", 0, 15, key=f"a{m['id']}")
                if st.button("Update", key=f"b{m['id']}"):
                    m.update({"score_h": h, "score_a": a, "finished": True}); st.rerun()

with t2:
    # ( Standings logic remains same, but filtered by the explicit 12 groups )
    GROUPS_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS_LIST):
        with cols[i % 3]:
            st.markdown(f"### Group {gId}")
            teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
            res = []
            for t in teams:
                pts, gd = 0, 0
                for m in st.session_state.wc_matches:
                    if m['finished'] and (m['home']['id'] == t['id'] or m['away']['id'] == t['id']):
                        is_h = m['home']['id'] == t['id']
                        h, a = (m['score_h'], m['score_a']) if is_h else (m['score_a'], m['score_h'])
                        gd += (h - a)
                        if h > a: pts += 3
                        elif h == a: pts += 1
                res.append({"Team": f"{t['flag']} {t['name']}", "Pts": pts, "GD": gd})
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with t3:
    st.markdown("### 🔮 Gemini AI Expert Analyst")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model_id = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available else 'models/gemini-pro'
            model = genai.GenerativeModel(model_id)
            t_names = sorted([t['name'] for t in INITIAL_TEAMS])
            c1, c2 = st.columns(2)
            h_t, a_t = c1.selectbox("Home", t_names), c2.selectbox("Away", t_names, index=1)
            if st.button("GENERATE PREDICTION"):
                with st.spinner("Analyzing data..."):
                    resp = model.generate_content(f"Predict score for {h_t} vs {a_t} in World Cup 2026. Explain tactics in Greek.")
                    st.info(resp.text)
        except Exception as e: st.error(f"Error: {e}")
