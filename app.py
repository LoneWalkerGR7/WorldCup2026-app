import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (COSMIC THEME - WHITE TEXT - BLACK RESET) ---
st.set_page_config(page_title="World Cup 2026 Ultimate Portal", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Λευκά γράμματα παντού (Τίτλοι, Labels, Markdown) */
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important; }
    
    /* Dashboard Stats Cards */
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
    .st-venue { font-size: 9px; color: #94a3b8 !important; font-style: italic; margin-top: 5px; }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    
    /* ΣΤΟΙΧΙΣΗ ΠΙΝΑΚΩΝ ΒΑΘΜΟΛΟΓΙΑΣ */
    div[data-testid="stTable"] {
        background-color: #0f172a;
        border-radius: 10px;
        border: 1px solid #1e293b;
        padding: 5px;
    }
    div[data-testid="stTable"] table { color: white !important; width: 100% !important; font-size: 12px !important; }
    
    /* RESET BUTTON: ΜΑΥΡΑ ΓΡΑΜΜΑΤΑ ΣΕ ΛΕΥΚΟ ΦΟΝΤΟ */
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        font-weight: 800 !important;
        border: 2px solid #ffffff !important;
        text-transform: uppercase;
    }
    
    /* PRIMARY BUTTONS (AUTO-PLAY, AI) */
    button[data-testid="stBaseButton-primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ (Mapping από το JSON) ---
TEAMS_MAP = {
    "1": {"n": "Mexico", "img": "https://flagcdn.com/w80/mx.png", "g": "A"},
    "2": {"n": "South Africa", "img": "https://flagcdn.com/w80/za.png", "g": "A"},
    "3": {"n": "South Korea", "img": "https://flagcdn.com/w80/kr.png", "g": "A"},
    "4": {"n": "Czechia", "img": "https://flagcdn.com/w80/cz.png", "g": "A"},
    "5": {"n": "Canada", "img": "https://flagcdn.com/w80/ca.png", "g": "B"},
    "6": {"n": "Bosnia", "img": "https://flagcdn.com/w80/ba.png", "g": "B"},
    "7": {"n": "Qatar", "img": "https://flagcdn.com/w80/qa.png", "g": "B"},
    "8": {"n": "Switzerland", "img": "https://flagcdn.com/w80/ch.png", "g": "B"},
    "9": {"n": "Brazil", "img": "https://flagcdn.com/w80/br.png", "g": "C"},
    "10": {"n": "Morocco", "img": "https://flagcdn.com/w80/ma.png", "g": "C"},
    "11": {"n": "Haiti", "img": "https://flagcdn.com/w80/ht.png", "g": "C"},
    "12": {"n": "Scotland", "img": "https://flagcdn.com/w80/gb-sct.png", "g": "C"},
    "13": {"n": "USA", "img": "https://flagcdn.com/w80/us.png", "g": "D"},
    "14": {"n": "Paraguay", "img": "https://flagcdn.com/w80/py.png", "g": "D"},
    "15": {"n": "Australia", "img": "https://flagcdn.com/w80/au.png", "g": "D"},
    "16": {"n": "Turkey", "img": "https://flagcdn.com/w80/tr.png", "g": "D"},
    "17": {"n": "Germany", "img": "https://flagcdn.com/w80/de.png", "g": "E"},
    "18": {"n": "Curacao", "img": "https://flagcdn.com/w80/cw.png", "g": "E"},
    "19": {"n": "Ivory Coast", "img": "https://flagcdn.com/w80/ci.png", "g": "E"},
    "20": {"n": "Ecuador", "img": "https://flagcdn.com/w80/ec.png", "g": "E"},
    "21": {"n": "Netherlands", "img": "https://flagcdn.com/w80/nl.png", "g": "F"},
    "22": {"n": "Japan", "img": "https://flagcdn.com/w80/jp.png", "g": "F"},
    "23": {"n": "Sweden", "img": "https://flagcdn.com/w80/se.png", "g": "F"},
    "24": {"n": "Tunisia", "img": "https://flagcdn.com/w80/tn.png", "g": "F"},
    "25": {"n": "Belgium", "img": "https://flagcdn.com/w80/be.png", "g": "G"},
    "26": {"n": "Egypt", "img": "https://flagcdn.com/w80/eg.png", "g": "G"},
    "27": {"n": "Iran", "img": "https://flagcdn.com/w80/ir.png", "g": "G"},
    "28": {"n": "New Zealand", "img": "https://flagcdn.com/w80/nz.png", "g": "G"},
    "29": {"n": "Spain", "img": "https://flagcdn.com/w80/es.png", "g": "H"},
    "30": {"n": "Cape Verde", "img": "https://flagcdn.com/w80/cv.png", "g": "H"},
    "31": {"n": "Saudi Arabia", "img": "https://flagcdn.com/w80/sa.png", "g": "H"},
    "32": {"n": "Uruguay", "img": "https://flagcdn.com/w80/uy.png", "g": "H"},
    "33": {"n": "France", "img": "https://flagcdn.com/w80/fr.png", "g": "I"},
    "34": {"n": "Senegal", "img": "https://flagcdn.com/w80/sn.png", "g": "I"},
    "35": {"n": "Iraq", "img": "https://flagcdn.com/w80/iq.png", "g": "I"},
    "36": {"n": "Norway", "img": "https://flagcdn.com/w80/no.png", "g": "I"},
    "37": {"n": "Argentina", "img": "https://flagcdn.com/w80/ar.png", "g": "J"},
    "38": {"n": "Algeria", "img": "https://flagcdn.com/w80/dz.png", "g": "J"},
    "39": {"n": "Austria", "img": "https://flagcdn.com/w80/at.png", "g": "J"},
    "40": {"n": "Jordan", "img": "https://flagcdn.com/w80/jo.png", "g": "J"},
    "41": {"n": "Portugal", "img": "https://flagcdn.com/w80/pt.png", "g": "K"},
    "42": {"n": "DR Congo", "img": "https://flagcdn.com/w80/cd.png", "g": "K"},
    "43": {"n": "Uzbekistan", "img": "https://flagcdn.com/w80/uz.png", "g": "K"},
    "44": {"n": "Colombia", "img": "https://flagcdn.com/w80/co.png", "g": "K"},
    "45": {"n": "England", "img": "https://flagcdn.com/w80/gb-eng.png", "g": "L"},
    "46": {"n": "Croatia", "img": "https://flagcdn.com/w80/hr.png", "g": "L"},
    "47": {"n": "Ghana", "img": "https://flagcdn.com/w80/gh.png", "g": "L"},
    "48": {"n": "Panama", "img": "https://flagcdn.com/w80/pa.png", "g": "L"}
}

# --- 3. ΠΡΟΓΡΑΜΜΑ (ΑΠΟ ΤΗ ΦΩΤΟΓΡΑΦΙΑ ΣΟΥ) ---
RAW_MATCHES = [
    ["A", "11/06 22:00", "Estadio Azteca", "1", "2"],
    ["A", "12/06 05:00", "Estadio Akron", "3", "4"],
    ["B", "12/06 22:00", "BMO Field", "5", "6"],
    ["D", "13/06 04:00", "SoFi Stadium", "13", "14"],
    ["D", "14/06 07:00", "BC Place", "15", "16"],
    ["B", "13/06 22:00", "Levi's Stadium", "7", "8"],
    ["C", "14/06 01:00", "MetLife Stadium", "9", "10"],
    ["C", "14/06 04:00", "Gillette Stadium", "11", "12"],
    ["E", "14/06 20:00", "NRG Stadium", "17", "18"],
    ["F", "14/06 23:00", "AT&T Stadium", "21", "22"],
    ["E", "15/06 02:00", "Lincoln Field", "19", "20"],
    ["F", "15/06 05:00", "Estadio BBVA", "23", "24"],
    ["H", "15/06 19:00", "Mercedes-Benz", "29", "30"],
    ["G", "15/06 22:00", "Lumen Field", "25", "26"],
    ["H", "16/06 01:00", "Hard Rock", "31", "32"],
    ["G", "16/06 04:00", "SoFi Stadium", "27", "28"],
    # ... Η δομή υποστηρίζει και τους 72 ...
]

# --- 4. SESSION STATE INITIALIZATION ---
if 'wc_matches' not in st.session_state:
    matches = []
    for i, m_data in enumerate(RAW_MATCHES):
        matches.append({
            "id": i+1, "group": m_data[0], "dt": m_data[1], "st": m_data[2],
            "h_id": m_data[3], "a_id": m_data[4], "sh": None, "sa": None, "fin": False,
            "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0,
            "referee": "TBD"
        })
    st.session_state.wc_matches = matches

# --- 5. FUNCTIONS ---
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
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=3600)
def Μετράω_τα_κουκιά(model_id, prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_id)
    return model.generate_content(prompt).text

# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m in st.session_state.wc_matches if m['fin']]
total_y = sum(m['y_h'] + m['y_a'] for m in fin_m)
total_r = sum(m['r_h'] + m['r_a'] for m in fin_m)
total_p = sum(m['p_h'] + m['p_a'] for m in fin_m)
total_og = sum(m['og_h'] + m['og_a'] for m in fin_m)

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin_m if m["sh"] is not None)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15!important">{total_y}</div><div class="stat-label">🟨Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444!important">{total_r}</div><div class="stat-label">🟥Red</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee!important">{total_p}</div><div class="stat-label">🎯Pens</div></div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{total_og}</div><div class="stat-label">⚠️OG</div></div>', unsafe_allow_html=True)

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ (SIMULATOR)", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset, type="secondary")

# --- 7. TABS ---
t1, t2, t3, t4 = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

with t1:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        h = TEAMS_MAP[m['h_id']]
        a = TEAMS_MAP[m['a_id']]
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center; padding:10px 0;">
                    <div style="text-align:center; width:40%; font-weight:bold;"><img src="{h['img']}" width="25"><br>{h['n']}</div>
                    <div style="font-size:20px; color:#06b6d4; font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="text-align:center; width:40%; font-weight:bold;"><img src="{a['img']}" width="25"><br>{a['n']}</div>
                </div>
                <div style="font-size:9px; color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:4px;">
                    🏁 Διαιτητής: {m['referee']} | 📍 {m['st']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columns(2)
                sh_v = ch.number_input(f"Goals {h['n']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {a['n']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"sa{m['id']}")
                yh_v = ch.slider(f"Yellow {h['n']}", 0, 10, m['y_h'], key=f"yh{m['id']}")
                ya_v = ca.slider(f"Yellow {a['n']}", 0, 10, m['y_a'], key=f"ya{m['id']}")
                rh_v = ch.checkbox(f"Red {h['n']}", value=bool(m['r_h']), key=f"rh{m['id']}")
                ra_v = ca.checkbox(f"Red {a['n']}", value=bool(m['r_a']), key=f"ra{m['id']}")
                ref_v = st.text_input("Διαιτητής", m['referee'], key=f"ref{m['id']}")
                if st.button("Save", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v, "sa": sa_v, "fin": True, "y_h": yh_v, "y_a": ya_v, "r_h": int(rh_v), "r_a": int(ra_v), "referee": ref_v})
                    st.rerun()

with t2:
    GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    cols_s = st.columns(3)
    for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_team_ids = [tid for tid, d in TEAMS_MAP.items() if d['g'] == gId]
            res = []
            for tid in g_team_ids:
                team = TEAMS_MAP[tid]
                pts, gd, y, r, p, og = 0, 0, 0, 0, 0, 0
                for m in st.session_state.wc_matches:
                    if m['fin'] and (m['h_id'] == tid or m['a_id'] == tid):
                        is_h = m['h_id'] == tid
                        h_s, a_s = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
                        y += m['y_h'] if is_h else m['y_a']
                        r += m['r_h'] if is_h else m['r_a']
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                res.append({"Team": team['n'], "Pts": pts, "GD": gd, "Y": y, "R": r})
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with t3:
    all_n = sorted([d['n'] for d in TEAMS_MAP.values()])
    sel_t = st.selectbox("Επίλεξε Ομάδα:", all_n)
    t_matches = [m for m in st.session_state.wc_matches if (TEAMS_MAP[m['h_id']]['n'] == sel_t or TEAMS_MAP[m['a_id']]['n'] == sel_t)]
    cols_team = st.columns(3)
    for idx, m in enumerate(t_matches):
        with cols_team[idx % 3]:
            res_col = "#10b981" if m['fin'] else "#1e293b"
            st.markdown(f"""<div class="match-card" style="border-top:4px solid {res_col}">
            <b>Αγώνας {idx+1}</b><br>{TEAMS_MAP[m['h_id']]['n']} {m['sh'] if m['sh'] is not None else ''} - {m['sa'] if m['sa'] is not None else ''} {TEAMS_MAP[m['a_id']]['n']}
            </div>""", unsafe_allow_html=True)

with t4:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            working_model = 'gemini-1.5-flash' # Απευθείας Flash για αποφυγή 404
            c1, c2 = st.columns(2)
            home = c1.selectbox("Home Team", all_n, key="h_ai")
            away = c2.selectbox("Away Team", all_n, index=1, key="a_ai")
            m_no = st.number_input("Αγώνας #", 1, 104, 1)
            
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary"):
                with st.spinner("Ο ΚΟΝΤΟΣ αναλύει..."):
                    prompt = f"Analyze match #{m_no}: {home} vs {away} (World Cup 2026). Give deep tactical analysis and score in Greek."
                    try:
                        ans = Μετράω_τα_κουκιά(working_model, prompt)
                        st.markdown("---")
                        st.markdown(ans)
                    except Exception as e: st.error("Quota Limit! Περίμενε 2 λεπτά.")
        except Exception as e: st.error(f"Error: {e}")
