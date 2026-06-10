import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS ---
st.set_page_config(page_title="World Cup 2026 Pro Stats", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important; }
    .stat-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 15px; text-align: center; }
    .stat-val { font-size: 22px; font-weight: 800; color: #06b6d4 !important; }
    div[data-testid="stTable"] { background-color: #0f172a; border-radius: 10px; border: 1px solid #1e293b; padding: 5px; }
    div[data-testid="stTable"] table { color: white !important; width: 100% !important; }
    button[data-testid="stBaseButton-secondary"] { color: black !important; background-color: #f1f5f9 !important; font-weight: 800 !important; border: 2px solid #ffffff !important; text-transform: uppercase; }
    .match-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 12px; margin-bottom: 10px; }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    button[data-testid="stBaseButton-primary"] { background-color: #ef4444 !important; color: white !important; border: none !important; font-weight: 800 !important; }
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
GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# --- 3. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    start_date = datetime(2026, 6, 11, 22, 0)
    for i, gId in enumerate(GROUPS_L):
        g_teams = [t for t in TEAMS if t['g'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for p_idx, (h, a) in enumerate(pairs):
            m_id = len(matches) + 1
            day_off = i + (p_idx * 3)
            time_m = start_date + timedelta(days=day_off, hours=(m_id % 4)*3)
            matches.append({
                "id": m_id, "group": gId, "h": g_teams[h]['n'], "a": g_teams[a]['n'],
                "sh": None, "sa": None, "fin": False, "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0, "dt": time_m.strftime("%d/%m %H:%M"), "st": "FIFA Stadium"
            })
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['y_h'], m['y_a'] = random.randint(0, 3), random.randint(0, 3)
            m['fin'] = True
    st.rerun()

def reset():
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.cache_data.clear() # Καθαρισμός μνήμης προβλέψεων
    st.rerun()

@st.cache_data(ttl=3600)
def get_prediction_logic(home, away, m_no):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return "Λείπει το API Key."
    genai.configure(api_key=api_key)
    # Απευθείας χρήση του flash χωρίς list_models για οικονομία quota
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Είσαι κορυφαίος αναλυτής. Αγώνας #{m_no}: {home} vs {away} (Μουντιάλ 2026).
    Δώσε: 1. Φόρμα ομάδων. 2. Προϊστορία. 3. Πρόβλεψη σκορ. 4. Πιθανότητες καρτών.
    Γράψε στα Ελληνικά με Markdown.
    """
    response = model.generate_content(prompt)
    return response.text

# --- 5. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m in st.session_state.wc_matches if m['fin']]
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin_m)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ", on_click=auto_play, type="primary")
with c4: st.button("🔄 RESET TOURNAMENT", on_click=reset, type="secondary")

# --- 6. TABS ---
t1, t2, t3 = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

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
                <div style="display:flex; justify-content: space-around; align-items:center;">
                    <b>{m['h']}</b>
                    <span style="font-size:20px; color:#06b6d4;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</span>
                    <b>{m['a']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

with t2:
    cols_s = st.columns(3)
    for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_teams = sorted(list(set([m['h'] for m in st.session_state.wc_matches if m['group'] == gId])))
            res = []
            for t in g_teams:
                pts, gd, y, r = 0, 0, 0, 0
                for m in st.session_state.wc_matches:
                    if m['fin'] and (m['h'] == t or m['a'] == t):
                        is_h = m['h'] == t
                        h_s, a_s = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
                        y += m['y_h'] if is_h else m['y_a']
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                res.append({"Team": t, "Pts": pts, "GD": gd, "Y": y})
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with t3:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ")
    all_teams_list = sorted(list(set([t['n'] for t in TEAMS])))
    c1, c2 = st.columns(2)
    h_t = c1.selectbox("Home Team", all_teams_list, key="sel_h")
    a_t = c2.selectbox("Away Team", all_teams_list, index=1, key="sel_a")
    m_no = st.number_input("Αγώνας #", 1, 104, 1)
    
    if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary"):
        with st.spinner("Ανάλυση..."):
            try:
                # Η κλήση γίνεται μόνο εδώ και είναι cached
                answer = get_prediction_logic(h_t, a_t, m_no)
                st.markdown("---")
                st.markdown(answer)
            except Exception as e:
                if "429" in str(e): st.error("🚨 Όριο Google! Περίμενε 1-2 λεπτά.")
                else: st.error(f"Σφάλμα: {e}")
