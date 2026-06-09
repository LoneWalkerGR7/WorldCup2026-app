import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (ΛΕΥΚΑ ΓΡΑΜΜΑΤΑ & BLACK RESET) ---
st.set_page_config(page_title="World Cup 2026 Pro", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Λευκά γράμματα παντού */
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important; }
    
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
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    
    /* Reset Button: BLACK TEXT */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: white !important;
        font-weight: 800 !important;
        border: none !important;
    }
    
    /* Tables White Text */
    div[data-testid="stTable"] table { color: white !important; }
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
GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# --- 3. SESSION STATE (72 MATCHES) ---
if 'wc_matches' not in st.session_state:
    matches = []
    start_date = datetime(2026, 6, 11, 22, 0)
    for g_idx, gId in enumerate(GROUPS):
        g_teams = [t for t in TEAMS if t['g'] == gId]
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for p_idx, (h, a) in enumerate(pairs):
            day_off = g_idx + (p_idx * 3)
            time_m = start_date + timedelta(days=day_off, hours=(p_idx % 4)*3)
            matches.append({
                "id": f"{gId}{p_idx}", "group": gId, "h": g_teams[h]['n'], "a": g_teams[a]['n'],
                "sh": None, "sa": None, "fin": False, "y": 0, "r": 0, "dt": time_m.strftime("%d/%m %H:%M")
            })
    st.session_state.wc_matches = sorted(matches, key=lambda x: datetime.strptime(x['dt'], "%d/%m %H:%M"))

# --- 4. ΛΕΙΤΟΥΡΓΙΕΣ ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['y'], m['r'] = random.randint(0, 5), (1 if random.random() > 0.9 else 0)
            m['fin'] = True
    st.rerun()

def reset():
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.rerun()

# --- 5. DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO DASHBOARD</h1>", unsafe_allow_html=True)
fin = [m for m in st.session_state.wc_matches if m['fin']]
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin)}</div><div class="stat-label">Goals</div></div>', unsafe_allow_html=True)
with c3: st.button("⚡ AUTO-PLAY SIMULATOR", on_click=auto_play, type="primary")
with c4: st.button("🔄 RESET ALL", on_click=reset, type="secondary")

t1, t2, t3 = st.tabs(["📅 ΠΡΟΓΡΑΜΜΑ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "🔮 AI ΠΡΟΒΛΕΨΕΙΣ"])

with t1:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding:10px 0;">
                    <b>{m['h']}</b>
                    <span style="font-size:20px; color:#06b6d4;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</span>
                    <b>{m['a']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

with t2:
    cols_std = st.columns(3)
    for i, gId in enumerate(GROUPS):
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
            # --- ΕΞΥΠΝΗ ΕΠΙΛΟΓΗ ΜΟΝΤΕΛΟΥ ΓΙΑ ΑΠΟΦΥΓΗ 404 ---
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Ψάχνουμε το flash, αν δεν υπάρχει παίρνουμε το πρώτο διαθέσιμο
            working_model = next((m for m in model_list if '1.5-flash' in m), model_list[0])
            
            model = genai.GenerativeModel(working_model)
            st.caption(f"Ενεργό Μοντέλο: {working_model}")

            t_list = sorted([t['n'] for t in TEAMS])
            c_a, c_b = st.columns(2)
            h_t = c_a.selectbox("Home", t_list, key="h_sel")
            a_t = c_b.selectbox("Away", t_list, index=1, key="a_sel")
            
            if st.button("GET AI ANALYSIS", type="primary"):
                with st.spinner("AI is analyzing..."):
                    resp = model.generate_content(f"Analyze World Cup 2026 match: {h_t} vs {a_t}. Probable score and tactics in Greek.")
                    st.markdown("---")
                    st.info(resp.text)
        except Exception as e:
            st.error(f"Σφάλμα AI: {e}")
    else: st.error("No API Key.")
