import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (COSMIC THEME - WHITE TEXT - BLACK RESET) ---
st.set_page_config(page_title="World Cup 2026 Pro Stats", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Λευκά γράμματα παντού */
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown { color: white !important; }
    
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
    .stat-label { font-size: 9px; color: #94a3b8 !important; text-transform: uppercase; }

    /* Match Cards */
    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    /* ΣΤΟΙΧΙΣΗ ΠΙΝΑΚΩΝ ΒΑΘΜΟΛΟΓΙΑΣ */
    div[data-testid="stTable"] {
        background-color: #0f172a;
        border-radius: 10px;
        border: 1px solid #1e293b;
        padding: 5px;
    }
    div[data-testid="stTable"] table {
        color: white !important;
        width: 100% !important;
        font-size: 12px !important;
    }
    
    /* ΚΟΥΜΠΙ RESET ΜΕ ΜΑΥΡΑ ΓΡΑΜΜΑΤΑ */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        font-weight: 800 !important;
        border: 2px solid #ffffff !important;
        text-transform: uppercase;
    }
    
    /* Auto-Play Button */
    button[data-testid="stBaseButton-primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
    }
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

# ΟΡΙΣΜΟΣ ΤΗΣ ΜΕΤΑΒΛΗΤΗΣ GROUPS (Για να μην βγάζει NameError)
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
                "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0,
                "dt": time_m.strftime("%d/%m %H:%M")
            })
            match_id += 1
    st.session_state.wc_matches = matches

# --- 4. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['y_h'], m['y_a'] = random.randint(0, 3), random.randint(0, 3)
            m['r_h'] = 1 if random.random() > 0.95 else 0
            m['r_a'] = 1 if random.random() > 0.95 else 0
            m['p_h'] = 1 if random.random() > 0.9 else 0
            m['p_a'] = 1 if random.random() > 0.9 else 0
            m['og_h'] = 1 if random.random() > 0.98 else 0
            m['og_a'] = 1 if random.random() > 0.98 else 0
            m['fin'] = True
    st.rerun()

def reset():
    if 'wc_matches' in st.session_state:
        del st.session_state['wc_matches']
    st.rerun()

# Συναρτήση για AI (Με Caching για αποφυγή 429)
@st.cache_data(ttl=3600)
def get_ai_prediction(model_id, prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_id)
    return model.generate_content(prompt).text

# --- 5. DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin = [m for m in st.session_state.wc_matches if m['fin']]

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin)}</div><div class="stat-label">Goals</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15!important">{sum(m["y_h"]+m["y_a"] for m in fin)}</div><div class="stat-label">Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444!important">{sum(m["r_h"]+m["r_a"] for m in fin)}</div><div class="stat-label">Red</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee!important">{sum(m["p_h"]+m["p_a"] for m in fin)}</div><div class="stat-label">Pens</div></div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{sum(m["og_h"]+m["og_a"] for m in fin)}</div><div class="stat-label">OG</div></div>', unsafe_allow_html=True)

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ (SIMULATOR)", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset, type="secondary")

# --- 6. TABS ---
t1, t2, t3 = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ ΚΑΙ ΣΤΑΤΙΣΤΙΚΑ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

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
                <div style="display:flex; justify-content: space-around; align-items:center; padding:10px 0;">
                    <div style="width:40%; text-align:center; font-weight:bold; font-size:13px;">{m['h']}</div>
                    <div style="font-size:20px; color:#06b6d4; font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="width:40%; text-align:center; font-weight:bold; font-size:13px;">{m['a']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργασία Stats"):
                colh, cola = st.columns(2)
                sh_i = colh.number_input(f"Goals {m['h']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"sh{m['id']}")
                sa_i = cola.number_input(f"Goals {m['a']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"sa{m['id']}")
                yh_i = colh.slider(f"Yellow {m['h']}", 0, 10, m['y_h'], key=f"yh{m['id']}")
                ya_i = cola.slider(f"Yellow {m['a']}", 0, 10, m['y_a'], key=f"ya{m['id']}")
                rh_i = colh.checkbox(f"Red {m['h']}", value=bool(m['r_h']), key=f"rh{m['id']}")
                ra_i = cola.checkbox(f"Red {m['a']}", value=bool(m['r_a']), key=f"ra{m['id']}")
                ph_i = colh.number_input(f"Pens {m['h']}", 0, 5, m['p_h'], key=f"ph{m['id']}")
                pa_i = cola.number_input(f"Pens {m['a']}", 0, 5, m['p_a'], key=f"pa{m['id']}")
                oh_i = colh.number_input(f"OG {m['h']}", 0, 5, m['og_h'], key=f"oh{m['id']}")
                oa_i = cola.number_input(f"OG {m['a']}", 0, 5, m['og_a'], key=f"oa{m['id']}")
                if st.button("Save Result", key=f"s{m['id']}"):
                    m.update({"sh": sh_i, "sa": sa_i, "y_h": yh_i, "y_a": ya_i, "r_h": int(rh_i), "r_a": int(ra_i), "p_h": ph_i, "p_a": pa_i, "og_h": oh_i, "og_a": oa_i, "fin": True})
                    st.rerun()

with t2:
    cols_std = st.columns(3)
    for i, gId in enumerate(GROUPS):
        with cols_std[i % 3]:
            st.markdown(f"### Group {gId}")
            g_teams = [t['n'] for t in TEAMS if t['g'] == gId]
            res = []
            for t in g_teams:
                pts, gd, y, r, p, og = 0, 0, 0, 0, 0, 0
                for m in st.session_state.wc_matches:
                    if m['fin'] and (m['h'] == t or m['a'] == t):
                        is_h = m['h'] == t
                        h_s, a_s = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
                        y += m['y_h'] if is_h else m['y_a']
                        r += m['r_h'] if is_h else m['r_a']
                        p += m['p_h'] if is_h else m['p_a']
                        og += m['og_h'] if is_h else m['og_a']
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                res.append({"Team": t, "Pts": pts, "GD": gd, "Y": y, "R": r, "P": p, "OG": og})
            df = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
            st.table(df)

with t3:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ...")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        try:
            # Δυναμική επιλογή μοντέλου
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            working_model = next((m for m in model_list if '1.5-flash' in m), model_list[0])
            
            t_names = sorted(list(set([t['n'] for t in TEAMS])))
            c1, c2 = st.columns(2)
            home = c1.selectbox("Home Team", t_names, key="h_p")
            away = c2.selectbox("Away Team", t_names, index=1, key="a_p")
            
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary"):
                with st.spinner("Ο ΚΟΝΤΟΣ διαβάζει τα άστρα..."):
                    prompt = f"Είσαι ένας κορυφαίος αναλυτής. Κάνε μια βαθιά πρόβλεψη για το Μουντιάλ 2026: {home} vs {away} στα Ελληνικά."
                    try:
                        result = get_ai_prediction(working_model, prompt)
                        st.info(result)
                    except Exception as ai_e:
                        if "429" in str(ai_e): st.warning("Quota Limit! Περίμενε 1 λεπτό.")
                        else: st.error(f"AI Error: {ai_e}")
        except Exception as e: st.error(f"Error: {e}")
    else: st.error("Add GEMINI_API_KEY to secrets.")
