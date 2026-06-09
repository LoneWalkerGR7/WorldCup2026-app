import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os

# --- 1. CONFIG & THEME (Cosmic Slate) ---
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

# --- 2. ΟΙ ΣΩΣΤΟΙ ΟΜΙΛΟΙ (48 ΟΜΑΔΕΣ) ---
INITIAL_TEAMS = [
    # 1ος Όμιλος (A)
    {"id": "mex", "name": "Μεξικό", "flag": "🇲🇽", "group": "A"},
    {"id": "rsa", "name": "Νότια Αφρική", "flag": "🇿🇦", "group": "A"},
    {"id": "kor", "name": "Νότια Κορέα", "flag": "🇰🇷", "group": "A"},
    {"id": "cze", "name": "Τσεχία", "flag": "🇨🇿", "group": "A"},
    # 2ος Όμιλος (B)
    {"id": "can", "name": "Καναδάς", "flag": "🇨🇦", "group": "B"},
    {"id": "bih", "name": "Βοσνία", "flag": "🇧🇦", "group": "B"},
    {"id": "qat", "name": "Κατάρ", "flag": "🇶🇦", "group": "B"},
    {"id": "sui", "name": "Ελβετία", "flag": "🇨🇭", "group": "B"},
    # 3ος Όμιλος (C)
    {"id": "bra", "name": "Βραζιλία", "flag": "🇧🇷", "group": "C"},
    {"id": "mar", "name": "Μαρόκο", "flag": "🇲🇦", "group": "C"},
    {"id": "hai", "name": "Αϊτή", "flag": "🇭🇹", "group": "C"},
    {"id": "sco", "name": "Σκωτία", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "group": "C"},
    # 4ος Όμιλος (D)
    {"id": "usa", "name": "ΗΠΑ", "flag": "🇺🇸", "group": "D"},
    {"id": "par", "name": "Παραγουάη", "flag": "🇵🇾", "group": "D"},
    {"id": "aus", "name": "Αυστραλία", "flag": "🇦🇺", "group": "D"},
    {"id": "tur", "name": "Τουρκία", "flag": "🇹🇷", "group": "D"},
    # 5ος Όμιλος (E)
    {"id": "ger", "name": "Γερμανία", "flag": "🇩🇪", "group": "E"},
    {"id": "cur", "name": "Κουρασάο", "flag": "🇨🇼", "group": "E"},
    {"id": "civ", "name": "Ακτή Ελεφαντοστού", "flag": "🇨🇮", "group": "E"},
    {"id": "ecu", "name": "Εκουαδόρ", "flag": "🇪🇨", "group": "E"},
    # 6ος Όμιλος (F)
    {"id": "ned", "name": "Ολλανδία", "flag": "🇳🇱", "group": "F"},
    {"id": "jpn", "name": "Ιαπωνία", "flag": "🇯🇵", "group": "F"},
    {"id": "swe", "name": "Σουηδία", "flag": "🇸🇪", "group": "F"},
    {"id": "tun", "name": "Τυνησία", "flag": "🇹🇳", "group": "F"},
    # 7ος Όμιλος (G)
    {"id": "bel", "name": "Βέλγιο", "flag": "🇧🇪", "group": "G"},
    {"id": "egy", "name": "Αίγυπτος", "flag": "🇪🇬", "group": "G"},
    {"id": "irn", "name": "Ιράν", "flag": "🇮🇷", "group": "G"},
    {"id": "nzl", "name": "Νέα Ζηλανδία", "flag": "🇳🇿", "group": "G"},
    # 8ος Όμιλος (H)
    {"id": "esp", "name": "Ισπανία", "flag": "🇪🇸", "group": "H"},
    {"id": "cpv", "name": "Πράσινο Ακρωτήρι", "flag": "🇨🇻", "group": "H"},
    {"id": "ksa", "name": "Σαουδική Αραβία", "flag": "🇸🇦", "group": "H"},
    {"id": "ury", "name": "Ουρουγουάη", "flag": "🇺🇾", "group": "H"},
    # 9ος Όμιλος (I)
    {"id": "fra", "name": "Γαλλία", "flag": "🇫🇷", "group": "I"},
    {"id": "sen", "name": "Σενεγάλη", "flag": "🇸🇳", "group": "I"},
    {"id": "irq", "name": "Ιράκ", "flag": "🇮🇶", "group": "I"},
    {"id": "nor", "name": "Νορβηγία", "flag": "🇳🇴", "group": "I"},
    # 10ος Όμιλος (J)
    {"id": "arg", "name": "Αργεντινή", "flag": "🇦🇷", "group": "J"},
    {"id": "alg", "name": "Αλγερία", "flag": "🇩🇿", "group": "J"},
    {"id": "aut", "name": "Αυστρία", "flag": "🇦🇹", "group": "J"},
    {"id": "jor", "name": "Ιορδανία", "flag": "🇯🇴", "group": "J"},
    # 11ος Όμιλος (K)
    {"id": "por", "name": "Πορτογαλία", "flag": "🇵🇹", "group": "K"},
    {"id": "cog", "name": "Κονγκό", "flag": "🇨🇬", "group": "K"},
    {"id": "uzb", "name": "Ουζμπεκιστάν", "flag": "🇺🇿", "group": "K"},
    {"id": "col", "name": "Κολομβία", "flag": "🇨🇴", "group": "K"},
    # 12ος Όμιλος (L)
    {"id": "eng", "name": "Αγγλία", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group": "L"},
    {"id": "cro", "name": "Κροατία", "flag": "🇭🇷", "group": "L"},
    {"id": "gha", "name": "Γκάνα", "flag": "🇬🇭", "group": "L"},
    {"id": "pan", "name": "Παναμάς", "flag": "🇵🇦", "group": "L"}
]

GROUPS_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# --- 3. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    for gId in GROUPS_LIST:
        g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
        # Κάθε ομάδα παίζει με όλες στον όμιλο (6 ματς)
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for i, (h, a) in enumerate(pairs):
            matches.append({
                "id": f"{gId}_m{i+1}", "group": gId,
                "home": g_teams[h], "away": g_teams[a],
                "score_h": None, "score_a": None, "finished": False
            })
    st.session_state.wc_matches = matches

# --- 4. ΛΕΙΤΟΥΡΓΙΕΣ ---
def auto_simulate():
    for m in st.session_state.wc_matches:
        if not m['finished']:
            m['score_h'] = random.randint(0, 4)
            m['score_a'] = random.randint(0, 4)
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
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{total_goals}</div><div class="stat-label">ΣΥΝΟΛΙΚΑ ΓΚΟΛ</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ Auto-Play (Simulate)", on_click=auto_simulate, use_container_width=True)
with c4: st.button("🔄 Reset Tournament", on_click=reset_all, use_container_width=True)

# --- 6. TABS ---
tab_cal, tab_std, tab_ai = st.tabs(["📅 Ημερολόγιο & Αγώνες", "🏆 Live Βαθμολογίες", "🧠 AI Προβλέψεις"])

with tab_cal:
    g_filter = st.selectbox("Επίλεξε Όμιλο:", ["Όλοι οι Όμιλοι"] + [f"{i+1}ος Όμιλος ({g})" for i, g in enumerate(GROUPS_LIST)])
    actual_g = g_filter[-2] if "Όμιλος" in g_filter else "Όλοι"
    
    cols = st.columns(2)
    display_matches = [m for m in st.session_state.wc_matches if actual_g == "Όλοι" or m['group'] == actual_g]
    
    for idx, m in enumerate(display_matches):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between;">
                    <span class="group-tag">ΟΜΙΛΟΣ {m['group']}</span>
                    <span style="color: #10b981; font-weight: bold; font-size: 10px;">{'ΤΕΛΙΚΟ' if m['finished'] else ''}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding: 10px 0;">
                    <div style="width:40%; text-align:center;"><b>{m['home']['flag']} {m['home']['name']}</b></div>
                    <div style="font-size: 22px; color: #06b6d4; font-weight: 800;">
                        {m['score_h'] if m['score_h'] is not None else '-'} : {m['score_a'] if m['score_a'] is not None else '-'}
                    </div>
                    <div style="width:40%; text-align:center;"><b>{m['away']['name']} {m['away']['flag']}</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Εισαγωγή Σκορ"):
                h = st.number_input(f"Γκολ {m['home']['name']}", 0, 15, key=f"h_{m['id']}")
                a = st.number_input(f"Γκολ {m['away']['name']}", 0, 15, key=f"a_{m['id']}")
                if st.button("Αποθήκευση", key=f"b_{m['id']}"):
                    m.update({"score_h": h, "score_a": a, "finished": True})
                    st.rerun()

with tab_std:
    cols = st.columns(3)
    for i, gId in enumerate(GROUPS_LIST):
        with cols[i % 3]:
            st.markdown(f"#### {i+1}ος Όμιλος ({gId})")
            g_teams = [t for t in INITIAL_TEAMS if t['group'] == gId]
            res = []
            for t in g_teams:
                stats = {"Ομάδα": f"{t['flag']} {t['name']}", "Αγ": 0, "Ν": 0, "Ι": 0, "Η": 0, "Γκολ": 0, "ΔΤ": 0, "Β": 0}
                for m in st.session_state.wc_matches:
                    if m['finished'] and (m['home']['id'] == t['id'] or m['away']['id'] == t['id']):
                        stats["Αγ"] += 1
                        is_h = m['home']['id'] == t['id']
                        goals, opp = (m['score_h'], m['score_a']) if is_h else (m['score_a'], m['score_h'])
                        stats["Γκολ"] += goals
                        stats["ΔΤ"] += (goals - opp)
                        if goals > opp: stats["Ν"], stats["Β"] = stats["Ν"]+1, stats["Β"]+3
                        elif goals == opp: stats["Ι"], stats["Β"] = stats["Ι"]+1, stats["Β"]+1
                        else: stats["Η"] += 1
                res.append(stats)
            df = pd.DataFrame(res).sort_values(by=["Β", "ΔΤ"], ascending=False)
            st.table(df[["Ομάδα", "Αγ", "Β", "ΔΤ"]])

with tab_ai:
    st.subheader("🧠 AI Match Predictor (Gemini)")
    team_list = sorted([t['name'] for t in INITIAL_TEAMS])
    t1 = st.selectbox("Γηπεδούχος:", team_list)
    t2 = st.selectbox("Φιλοξενούμενος:", team_list, index=1)
    if st.button("🔮 Λήψη Πρόβλεψης"):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Είσαι αθλητικός αναλυτής. Προέβλεψε το σκορ και κάνε τακτική ανάλυση για το ματς Μουντιάλ 2026: {t1} vs {t2}. Γράψε στα Ελληνικά."
            with st.spinner("Η AI αναλύει τα πλάνα..."):
                response = model.generate_content(prompt)
                st.info(response.text)
        else: st.error("Λείπει το API Key!")
