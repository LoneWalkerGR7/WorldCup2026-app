import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="Mundial 2026 Greek Portal", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
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
    .stat-val { font-size: 2rem; font-weight: 800; color: #06b6d4; font-family: monospace; }
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

# --- 2. ΔΕΔΟΜΕΝΑ ---
INITIAL_TEAMS = [
    {"id": "rsa", "name": "Νότια Αφρική", "flag": "🇿🇦", "group": "A"},
    {"id": "mex", "name": "Μεξικό", "flag": "🇲🇽", "group": "A"},
    {"id": "cze", "name": "Τσεχία", "flag": "🇨🇿", "group": "A"},
    {"id": "kor", "name": "Νότια Κορέα", "flag": "🇰🇷", "group": "A"},
    {"id": "eng", "name": "Αγγλία", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group": "B"},
    {"id": "sen", "name": "Σενεγάλη", "flag": "🇸🇳", "group": "B"},
    {"id": "irn", "name": "Ιράν", "flag": "🇮🇷", "group": "B"},
    {"id": "ukr", "name": "Ουκρανία", "flag": "🇺🇦", "group": "B"},
    {"id": "arg", "name": "Αργεντινή", "flag": "🇦🇷", "group": "C"},
    {"id": "pol", "name": "Πολωνία", "flag": "🇵🇱", "group": "C"},
    {"id": "ksa", "name": "Σαουδική Αραβία", "flag": "🇸🇦", "group": "C"},
    {"id": "per", "name": "Περού", "flag": "🇵🇪", "group": "C"},
    {"id": "fra", "name": "Γαλλία", "flag": "🇫🇷", "group": "D"},
    {"id": "aus", "name": "Αυστραλία", "flag": "🇦🇺", "group": "D"},
    {"id": "den", "name": "Δανία", "flag": "🇩🇰", "group": "D"},
    {"id": "tun", "name": "Τυνησία", "flag": "🇹🇳", "group": "D"},
    {"id": "esp", "name": "Ισπανία", "flag": "🇪🇸", "group": "E"},
    {"id": "crc", "name": "Κόστα Ρίκα", "flag": "🇨🇷", "group": "E"},
    {"id": "jpn", "name": "Ιαπωνία", "flag": "🇯🇵", "group": "E"},
    {"id": "hun", "name": "Ουγγαρία", "flag": "🇭🇺", "group": "E"},
    {"id": "bel", "name": "Βέλγιο", "flag": "🇧🇪", "group": "F"},
    {"id": "cro", "name": "Κροατία", "flag": "🇭🇷", "group": "F"},
    {"id": "mar", "name": "Μαρόκο", "flag": "🇲🇦", "group": "F"},
    {"id": "cmr", "name": "Καμερούν", "flag": "🇨🇲", "group": "F"},
    {"id": "bra", "name": "Βραζιλία", "flag": "🇧🇷", "group": "G"},
    {"id": "srb", "name": "Σερβία", "flag": "🇷🇸", "group": "G"},
    {"id": "sui", "name": "Ελβετία", "flag": "🇨🇭", "group": "G"},
    {"id": "kor_g", "name": "Νότια Κορέα", "flag": "🇰🇷", "group": "G"},
    {"id": "por", "name": "Πορτογαλία", "flag": "🇵🇹", "group": "H"},
    {"id": "gha", "name": "Γκάνα", "flag": "🇬🇭", "group": "H"},
    {"id": "ury", "name": "Ουρουγουάη", "flag": "🇺🇾", "group": "H"},
    {"id": "nzl", "name": "Νέα Ζηλανδία", "flag": "🇳🇿", "group": "H"},
    {"id": "ita", "name": "Ιταλία", "flag": "🇮🇹", "group": "I"},
    {"id": "swe", "name": "Σουηδία", "flag": "🇸🇪", "group": "I"},
    {"id": "col", "name": "Κολομβία", "flag": "🇨🇴", "group": "I"},
    {"id": "nga", "name": "Νιγηρία", "flag": "🇳🇬", "group": "I"},
    {"id": "ned", "name": "Ολλανδία", "flag": "🇳🇱", "group": "J"},
    {"id": "ecu", "name": "Ισημερινός", "flag": "🇪🇨", "group": "J"},
    {"id": "chi", "name": "Χιλή", "flag": "🇨🇱", "group": "J"},
    {"id": "alg", "name": "Αλγερία", "flag": "🇩🇿", "group": "J"},
    {"id": "ger", "name": "Γερμανία", "flag": "🇩🇪", "group": "K"},
    {"id": "aut", "name": "Αυστρία", "flag": "🇦🇹", "group": "K"},
    {"id": "tur", "name": "Τουρκία", "flag": "🇹🇷", "group": "K"},
    {"id": "egy", "name": "Αίγυπτος", "flag": "🇪🇬", "group": "K"},
    {"id": "wal", "name": "Ουαλία", "flag": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "group": "L"},
    {"id": "par", "name": "Παραγουάη", "flag": "🇵🇾", "group": "L"},
    {"id": "irl", "name": "Ιρλανδία", "flag": "🇮🇪", "group": "L"},
    {"id": "civ", "name": "Ακτή Ελεφαντοστού", "flag": "🇨🇮", "group": "L"}
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
                "score_h": None, "score_a": None, "finished": False,
                "stats": {"yellow": 0, "red": 0, "penalties": 0}
            })
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_simulate():
    for m in st.session_state.wc_matches:
        if not m['finished']:
            m['score_h'] = random.randint(0, 4)
            m['score_a'] = random.randint(0, 4)
            m['stats']['yellow'] = random.randint(1, 6)
            m['finished'] = True
    st.rerun()

def reset_all():
    del st.session_state['wc_matches']
    st.rerun()

# --- 5. HEADER ---
st.markdown("""
    <div class="header-container">
        <span style="color: #06b6d4; font-weight: bold;">FIFA WORLD CUP 2026™ GREEK PORTAL</span>
        <h1 style="color: white; margin-top: 10px;">Ημερολόγιο & AI Προβλέψεις Μουντιάλ 2026</h1>
    </div>
    """, unsafe_allow_html=True)

finished = [m for m in st.session_state.wc_matches if m['finished']]
total_goals = sum(m['score_h'] + m['score_a'] for m in finished)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(finished)}/72</div><div class="stat-label">ΑΓΩΝΕΣ</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{total_goals}</div><div class="stat-label">ΓΚΟΛ</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ Auto-Play", on_click=auto_simulate, use_container_width=True)
with c4: st.button("🔄 Reset", on_click=reset_all, use_container_width=True)

# --- 6. TABS ---
tab_cal, tab_std, tab_ai = st.tabs(["📅 Ημερολόγιο", "🏆 Βαθμολογίες", "🧠 AI Προβλέψεις"])

with tab_cal:
    g_filter = st.selectbox("Φίλτρο Ομίλου:", ["Όλοι"] + GROUPS_LIST)
    cols = st.columns(2)
    display_matches = [m for m in st.session_state.wc_matches if g_filter == "Όλοι" or m['group'] == g_filter]
    for idx, m in enumerate(display_matches):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between;">
                    <span class="group-tag">ΟΜΙΛΟΣ {m['group']}</span>
                    <span style="color: #10b981; font-size: 10px; font-weight: bold;">{'ΤΕΛΙΚΟ' if m['finished'] else ''}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding: 10px 0;">
                    <b>{m['home']['flag']} {m['home']['name']}</b>
                    <span style="font-size: 20px; color: #06b6d4;">{m['score_h'] if m['score_h'] is not None else '-'} : {m['score_a'] if m['score_a'] is not None else '-'}</span>
                    <b>{m['away']['name']} {m['away']['flag']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Εισαγωγή Σκορ"):
                h = st.number_input(f"Γκολ {m['home']['name']}", 0, 10, key=f"h_{m['id']}")
                a = st.number_input(f"Γκολ {m['away']['name']}", 0, 10, key=f"a_{m['id']}")
                if st.button("Αποθήκευση", key=f"b_{m['id']}"):
                    m.update({"score_h": h, "score_a": a, "finished": True})
                    st.rerun()

with tab_std:
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS_LIST):
        with cols[i % 3]:
            st.markdown(f"#### Όμιλος {gId}")
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
                res.append({"Ομάδα": f"{t['flag']} {t['name']}", "Β": pts, "Γκολ": f"{gf}:{ga}"})
            st.table(pd.DataFrame(res).sort_values("Β", ascending=False))

with tab_ai:
    st.subheader("AI Predictor")
    t1 = st.selectbox("Ομάδα 1:", [t['name'] for t in INITIAL_TEAMS])
    t2 = st.selectbox("Ομάδα 2:", [t['name'] for t in INITIAL_TEAMS], index=1)
    if st.button("Πρόβλεψη"):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Πρόβλεψε το σκορ: {t1} vs {t2} (Μουντιάλ 2026).")
            st.info(response.text)
