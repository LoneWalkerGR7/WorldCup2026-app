import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (COSMIC THEME) ---
st.set_page_config(page_title="World Cup 2026 Pro Stats", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important; }
    
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stat-val { font-size: 22px; font-weight: 800; color: #06b6d4 !important; }
    .stat-label { font-size: 9px; color: #94a3b8 !important; text-transform: uppercase; }

    div[data-testid="stTable"] { background-color: #0f172a; border-radius: 10px; border: 1px solid #1e293b; padding: 5px; }
    div[data-testid="stTable"] table { color: white !important; width: 100% !important; font-size: 12px !important; }
    
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        font-weight: 800 !important;
        border: 2px solid #ffffff !important;
        text-transform: uppercase;
    }

    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .st-venue { font-size: 9px; color: #94a3b8 !important; font-style: italic; margin-top: 5px; }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
    
    button[data-testid="stBaseButton-primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
    }

    .score-box { padding: 10px; border-radius: 8px; text-align: center; margin: 5px; font-weight: bold; border: 1px solid #1e293b; min-width: 65px; }
    .score-out { background-color: #064e3b; color: #10b981 !important; border: 1px solid #10b981; }
    .score-delayed { background-color: #450a0a; color: #ef4444 !important; border: 1px solid #ef4444; opacity: 0.6; }
    
    .turnaround-card {
        background: #1e293b;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
        border-left: 4px solid #06b6d4;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS_MAP = {
    "1": {"n": "Mexico", "img": "https://flagcdn.com/w80/mx.png", "g": "A"}, "2": {"n": "South Africa", "img": "https://flagcdn.com/w80/za.png", "g": "A"},
    "3": {"n": "South Korea", "img": "https://flagcdn.com/w80/kr.png", "g": "A"}, "4": {"n": "Czechia", "img": "https://flagcdn.com/w80/cz.png", "g": "A"},
    "5": {"n": "Canada", "img": "https://flagcdn.com/w80/ca.png", "g": "B"}, "6": {"n": "Bosnia", "img": "https://flagcdn.com/w80/ba.png", "g": "B"},
    "7": {"n": "Qatar", "img": "https://flagcdn.com/w80/qa.png", "g": "B"}, "8": {"n": "Switzerland", "img": "https://flagcdn.com/w80/ch.png", "g": "B"},
    "9": {"n": "Brazil", "img": "https://flagcdn.com/w80/br.png", "g": "C"}, "10": {"n": "Morocco", "img": "https://flagcdn.com/w80/ma.png", "g": "C"},
    "11": {"n": "Haiti", "img": "https://flagcdn.com/w80/ht.png", "g": "C"}, "12": {"n": "Scotland", "img": "https://flagcdn.com/w80/gb-sct.png", "g": "C"},
    "13": {"n": "USA", "img": "https://flagcdn.com/w80/us.png", "g": "D"}, "14": {"n": "Paraguay", "img": "https://flagcdn.com/w80/py.png", "g": "D"},
    "15": {"n": "Australia", "img": "https://flagcdn.com/w80/au.png", "g": "D"}, "16": {"n": "Turkey", "img": "https://flagcdn.com/w80/tr.png", "g": "D"},
    "17": {"n": "Germany", "img": "https://flagcdn.com/w80/de.png", "g": "E"}, "18": {"n": "Curacao", "img": "https://flagcdn.com/w80/cw.png", "g": "E"},
    "19": {"n": "Ivory Coast", "img": "https://flagcdn.com/w80/ci.png", "g": "E"}, "20": {"n": "Ecuador", "img": "https://flagcdn.com/w80/ec.png", "g": "E"},
    "21": {"n": "Netherlands", "img": "https://flagcdn.com/w80/nl.png", "g": "F"}, "22": {"n": "Japan", "img": "https://flagcdn.com/w80/jp.png", "g": "F"},
    "23": {"n": "Sweden", "img": "https://flagcdn.com/w80/se.png", "g": "F"}, "24": {"n": "Tunisia", "img": "https://flagcdn.com/w80/tn.png", "g": "F"},
    "25": {"n": "Belgium", "img": "https://flagcdn.com/w80/be.png", "g": "G"}, "26": {"n": "Egypt", "img": "https://flagcdn.com/w80/eg.png", "g": "G"},
    "27": {"n": "Iran", "img": "https://flagcdn.com/w80/ir.png", "g": "G"}, "28": {"n": "New Zealand", "img": "https://flagcdn.com/w80/nz.png", "g": "G"},
    "29": {"n": "Spain", "img": "https://flagcdn.com/w80/es.png", "g": "H"}, "30": {"n": "Cape Verde", "img": "https://flagcdn.com/w80/cv.png", "g": "H"},
    "31": {"n": "Saudi Arabia", "img": "https://flagcdn.com/w80/sa.png", "g": "H"}, "32": {"n": "Uruguay", "img": "https://flagcdn.com/w80/uy.png", "g": "H"},
    "33": {"n": "France", "img": "https://flagcdn.com/w80/fr.png", "g": "I"}, "34": {"n": "Senegal", "img": "https://flagcdn.com/w80/sn.png", "g": "I"},
    "35": {"n": "Iraq", "img": "https://flagcdn.com/w80/iq.png", "g": "I"}, "36": {"n": "Norway", "img": "https://flagcdn.com/w80/no.png", "g": "I"},
    "37": {"n": "Argentina", "img": "https://flagcdn.com/w80/ar.png", "g": "J"}, "38": {"n": "Algeria", "img": "https://flagcdn.com/w80/dz.png", "g": "J"},
    "39": {"n": "Austria", "img": "https://flagcdn.com/w80/at.png", "g": "J"}, "40": {"n": "Jordan", "img": "https://flagcdn.com/w80/jo.png", "g": "J"},
    "41": {"n": "Portugal", "img": "https://flagcdn.com/w80/pt.png", "g": "K"}, "42": {"n": "DR Congo", "img": "https://flagcdn.com/w80/cd.png", "g": "K"},
    "43": {"n": "Uzbekistan", "img": "https://flagcdn.com/w80/uz.png", "g": "K"}, "44": {"n": "Colombia", "img": "https://flagcdn.com/w80/co.png", "g": "K"},
    "45": {"n": "England", "img": "https://flagcdn.com/w80/gb-eng.png", "g": "L"}, "46": {"n": "Croatia", "img": "https://flagcdn.com/w80/hr.png", "g": "L"},
    "47": {"n": "Ghana", "img": "https://flagcdn.com/w80/gh.png", "g": "L"}, "48": {"n": "Panama", "img": "https://flagcdn.com/w80/pa.png", "g": "L"}
}

RAW_MATCHES = [
    ["A", "11/06 22:00", "Estadio Azteca", "1", "2"], ["A", "12/06 05:00", "Estadio Akron", "3", "4"],
    ["B", "12/06 22:00", "BMO Field", "5", "6"], ["D", "13/06 04:00", "SoFi Stadium", "13", "14"],
    ["D", "14/06 07:00", "BC Place", "15", "16"], ["B", "13/06 22:00", "Levi's Stadium", "7", "8"],
    ["C", "14/06 01:00", "MetLife Stadium", "9", "10"], ["C", "14/06 04:00", "Gillette Stadium", "11", "12"],
    ["E", "14/06 20:00", "NRG Stadium", "17", "18"], ["F", "14/06 23:00", "AT&T Stadium", "21", "22"],
    ["E", "15/06 02:00", "Lincoln Field", "19", "20"], ["F", "15/06 05:00", "Estadio BBVA", "23", "24"],
    ["H", "15/06 19:00", "Mercedes-Benz", "29", "30"], ["G", "15/06 22:00", "Lumen Field", "25", "26"],
    ["H", "16/06 01:00", "Hard Rock", "31", "32"], ["G", "16/06 04:00", "SoFi Stadium", "27", "28"],
    ["J", "17/06 07:00", "Levi's Stadium", "39", "40"], ["I", "16/06 10:00", "MetLife", "33", "34"],
    ["I", "17/06 01:00", "Gillette", "35", "36"], ["J", "17/06 04:00", "Arrowhead", "37", "38"],
    ["K", "17/06 08:00", "NRG Stadium", "41", "42"], ["L", "17/06 11:00", "AT&T Stadium", "45", "46"],
    ["L", "18/06 02:00", "BMO Field", "47", "48"], ["K", "18/06 05:00", "Estadio Azteca", "43", "44"],
    ["A", "18/06 07:00", "Mercedes-Benz", "4", "2"], ["B", "18/06 10:00", "SoFi Stadium", "8", "6"],
    ["B", "19/06 01:00", "BC Place", "5", "7"], ["A", "19/06 04:00", "Estadio Akron", "1", "3"],
    ["D", "20/06 06:00", "Levi's Stadium", "16", "14"], ["D", "19/06 10:00", "Lumen Field", "13", "15"],
    ["C", "20/06 01:00", "Gillette", "12", "10"], ["C", "20/06 03:30", "Lincoln Field", "9", "11"],
    ["F", "21/06 07:00", "Estadio BBVA", "24", "22"], ["F", "20/06 08:00", "NRG Stadium", "21", "23"],
    ["E", "20/06 11:00", "BMO Field", "17", "19"], ["E", "21/06 03:00", "Arrowhead", "20", "18"],
    ["H", "21/06 07:00", "Mercedes-Benz", "29", "31"], ["G", "21/06 10:00", "SoFi Stadium", "25", "27"],
    ["H", "22/06 01:00", "Hard Rock", "32", "30"], ["G", "22/06 04:00", "BC Place", "28", "26"],
    ["J", "22/06 08:00", "AT&T Stadium", "37", "39"], ["I", "23/06 12:00", "Lincoln Field", "33", "35"],
    ["I", "23/06 03:00", "MetLife", "36", "34"], ["J", "23/06 06:00", "Levi's Stadium", "40", "38"],
    ["K", "23/06 08:00", "NRG Stadium", "41", "43"], ["L", "23/06 11:00", "Gillette", "45", "47"],
    ["L", "24/06 02:00", "BMO Field", "48", "46"], ["K", "24/06 05:00", "Estadio Akron", "44", "42"],
    ["B", "24/06 10:00", "BC Place", "8", "5"], ["B", "24/06 10:00", "Lumen Field", "6", "7"],
    ["C", "25/06 01:00", "Hard Rock Stadium", "12", "9"], ["C", "25/06 01:00", "Mercedes-Benz", "10", "11"],
    ["A", "25/06 04:00", "Estadio Azteca", "4", "1"], ["A", "25/06 04:00", "Estadio BBVA", "2", "3"],
    ["E", "25/06 11:00", "MetLife", "20", "17"], ["E", "25/06 11:00", "Lincoln Field", "18", "19"],
    ["F", "26/06 02:00", "AT&T Stadium", "22", "23"], ["F", "26/06 02:00", "Arrowhead", "24", "21"],
    ["D", "26/06 05:00", "SoFi Stadium", "16", "13"], ["D", "26/06 05:00", "Levi's Stadium", "14", "15"],
    ["I", "26/06 10:00", "Gillette", "36", "33"], ["I", "26/06 10:00", "BMO Field", "34", "35"],
    ["H", "27/06 03:00", "Estadio Akron", "32", "29"], ["H", "27/06 03:00", "NRG Stadium", "30", "31"],
    ["G", "27/06 06:00", "Lumen Field", "26", "27"], ["G", "27/06 06:00", "BC Place", "28", "25"],
    ["L", "28/06 12:00", "MetLife", "48", "45"], ["L", "28/06 12:00", "Lincoln Field", "46", "47"],
    ["K", "28/06 02:30", "Hard Rock Stadium", "44", "41"], ["K", "28/06 02:30", "Mercedes-Benz", "42", "43"],
    ["J", "28/06 05:00", "Arrowhead", "38", "39"], ["J", "28/06 05:00", "AT&T Stadium", "40", "37"]
]

# --- 4. SESSION STATE ---
def init_session():
    matches = []
    for i, m_data in enumerate(RAW_MATCHES):
        matches.append({
            "id": i+1, "group": m_data[0], "dt": m_data[1], "st": m_data[2],
            "h_id": m_data[3], "a_id": m_data[4], "sh": None, "sa": None, "fin": False,
            "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0,
            "ref": "TBD", "turn": "Καμία", "htft": "TBD"
        })
    st.session_state.wc_matches = matches

if 'wc_matches' not in st.session_state:
    init_session()

# --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 5), random.randint(0, 5)
            m['y_h'], m['y_a'] = random.randint(0, 3), random.randint(0, 3)
            m['r_h'] = random.randint(0, 1) if random.random() > 0.9 else 0
            m['r_a'] = random.randint(0, 1) if random.random() > 0.9 else 0
            if m['sh'] > m['sa'] and random.random() > 0.85: m['turn'] = "Home SCORE First and LOSE"
            elif m['sa'] > m['sh'] and random.random() > 0.85: m['turn'] = "Away SCORE First and LOSE"
            res = "X"
            if m['sh'] > m['sa']: res = "1"
            elif m['sa'] > m['sh']: res = "2"
            m['htft'] = f"{random.choice(['1','X','2'])}/{res}"
            m['fin'] = True
    st.rerun()

def reset():
    init_session()
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=3600)
def get_ai_prediction(model_id, prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_id)
    return model.generate_content(prompt).text

# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m in st.session_state.wc_matches if m['fin']]
total_y = sum(m.get('y_h',0) + m.get('y_a',0) for m in fin_m)
total_r = sum(m.get('r_h',0) + m.get('r_a',0) for m in fin_m)
total_p = sum(m.get('p_h',0) + m.get('p_a',0) for m in fin_m)
total_og = sum(m.get('og_h',0) + m.get('og_a',0) for m in fin_m)

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

tabs = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "📊 ΑΝΑΛΥΣΗ ΣΚΟΡ", "🔄 ΑΝΑΤΡΟΠΕΣ", "🌓 ΗΜΙΧΡΟΝΑ / ΤΕΛΙΚΑ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

with tabs[0]:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        h = TEAMS_MAP.get(m['h_id'], {"n": "N/A", "img": ""})
        a = TEAMS_MAP.get(m['a_id'], {"n": "N/A", "img": ""})
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center;">
                    <div style="text-align:center; width:40%; font-weight:bold;"><img src="{h['img']}" width="25"><br>{h['n']}</div>
                    <div style="font-size:20px; color:#06b6d4; font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="text-align:center; width:40%;"><img src="{a['img']}" width="25"><br>{a['n']}</div>
                </div>
                <div style="font-size:9px; color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:4px;">
                    🟨 {m.get('y_h',0)}:{m.get('y_a',0)} | 🟥 {m.get('r_h',0)}:{m.get('r_a',0)} | 🎯 {m.get('p_h',0)}:{m.get('p_a',0)} | ⚠️ {m.get('og_h',0)}:{m.get('og_a',0)}
                </div>
                <div style="font-size:9px; color:#94a3b8; text-align:center; padding-top:2px;">
                    🏁 Ref: {m.get('ref','TBD')} | 📍 {m['st']} | 🔄 {m.get('turn','Καμία')} | 🌓 {m.get('htft','TBD')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columns(2)
                sh_v = ch.number_input(f"Goals {h['n']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {a['n']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"sa{m['id']}")
                yh_v = ch.slider(f"Yellow {h['n']}", 0, 10, m.get('y_h',0), key=f"yh{m['id']}")
                ya_v = ca.slider(f"Yellow {a['n']}", 0, 10, m.get('y_a',0), key=f"ya{m['id']}")
                rh_v = ch.number_input(f"Red {h['n']}", 0, 5, m.get('r_h',0), key=f"rh{m['id']}")
                ra_v = ca.number_input(f"Red {a['n']}", 0, 5, m.get('r_a',0), key=f"ra{m['id']}")
                ph_v = ch.number_input(f"Pens {h['n']}", 0, 5, m.get('p_h',0), key=f"ph{m['id']}")
                pa_v = ca.number_input(f"Pens {a['n']}", 0, 5, m.get('p_a',0), key=f"pa{m['id']}")
                oh_v = ch.number_input(f"OG {h['n']}", 0, 5, m.get('og_h',0), key=f"oh{m['id']}")
                oa_v = ca.number_input(f"OG {a['n']}", 0, 5, m.get('og_a',0), key=f"oa{m['id']}")
                ref_v = st.text_input("Referee", m.get('ref','TBD'), key=f"ref_in{m['id']}")
                turn_v = st.selectbox("Ανατροπή", ["Καμία", "Home SCORE First and LOSE", "Away SCORE First and LOSE", "1/2", "2/1"], index=0, key=f"turn_{m['id']}")
                htft_v = st.selectbox("Ημίχρονο/Τελικό", ["TBD", "1/1", "1/X", "1/2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"], index=0, key=f"htft_{m['id']}")
                if st.button("Save Result", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v, "sa": sa_v, "fin": True, "y_h": yh_v, "y_a": ya_v, "r_h": rh_v, "r_a": ra_v, "p_h": ph_v, "p_a": pa_v, "og_h": oh_v, "og_a": oa_v, "ref": ref_v, "turn": turn_v, "htft": htft_v})
                    st.rerun()

with tabs[1]:
    cols_s = st.columns(3)
    GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
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
                        y += m.get('y_h',0) if is_h else m.get('y_a',0)
                        r += m.get('r_h',0) if is_h else m.get('r_a',0)
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                res.append({"Flag": team['img'], "Team": team['n'], "Pts": pts, "GD": gd, "Y": y, "R": r})
            df = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
            st.data_editor(df, column_config={"Flag": st.column_config.ImageColumn("🏳️")}, hide_index=True, key=f"table_{gId}")

with tabs[2]:
    all_names = sorted([d['n'] for d in TEAMS_MAP.values()])
    sel_t = st.selectbox("Επιλέξτε Ομάδα:", all_names)
    team_id = next(k for k,v in TEAMS_MAP.items() if v['n'] == sel_t)
    t_matches = [m for m in st.session_state.wc_matches if (m['h_id'] == team_id or m['a_id'] == team_id)]
    t_pts, t_gf, t_ga, t_y, t_r = 0, 0, 0, 0, 0
    for m in t_matches:
        if m['fin']:
            is_h = m['h_id'] == team_id
            g, c = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
            t_gf += g; t_ga += c
            t_y += m.get('y_h',0) if is_h else m.get('y_a',0)
            if g > c: t_pts += 3
            elif g == c: t_pts += 1
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Points", t_pts); c_s2.metric("Goals", f"{t_gf}-{t_ga}"); c_s3.metric("Cards (Y)", t_y)
    cols_team = st.columns(3)
    for idx, m in enumerate(t_matches):
        with cols_team[idx % 3]:
            res_col = "#10b981" if m['fin'] else "#1e293b"
            h_n = TEAMS_MAP[m['h_id']]['n']; a_n = TEAMS_MAP[m['a_id']]['n']
            st.markdown(f"""<div class="match-card" style="border-top:4px solid {res_col}">
            <b>Αγώνας {idx+1}</b><br>{h_n} {m['sh'] if m['sh'] is not None else ''} - {m['sa'] if m['sa'] is not None else ''} {a_n}
            </div>""", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 📊 Πίνακας Πιθανών Σκορ & Συχνότητας")
    actual_scores = [(m['sh'], m['sa']) for m in st.session_state.wc_matches if m['fin']]
    # Προσθήκη επιλογών 5+
    grid_size = 6 # 0,1,2,3,4,5+
    for h_g in range(grid_size):
        cols_score = st.columns(grid_size)
        for a_g in range(grid_size):
            with cols_score[a_g]:
                h_label = str(h_g) if h_g < 5 else "5+"
                a_label = str(a_g) if a_g < 5 else "5+"
                # Φιλτράρισμα: Αν h_g < 5 ψάχνουμε ακριβώς, αν h_g == 5 ψάχνουμε >= 5
                def check(sh, sa, target_h, target_a):
                    h_ok = (sh == target_h) if target_h < 5 else (sh >= 5)
                    a_ok = (sa == target_a) if target_a < 5 else (sa >= 5)
                    return h_ok and a_ok
                count = sum(1 for sh, sa in actual_scores if check(sh, sa, h_g, a_g))
                st_class = "score-out" if count > 0 else "score-delayed"
                st.markdown(f"""<div class="score-box {st_class}">{h_label}-{a_label}<br><span style='font-size:9px'>{'✅' if count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""", unsafe_allow_html=True)

with tabs[4]:
    st.markdown("### 🔄 Ανάλυση Ανατροπών (Turnarounds)")
    t_fin = [m for m in st.session_state.wc_matches if m['fin'] and m.get('turn','Καμία') != "Καμία"]
    t_col1, t_col2, t_col3 = st.columns(3)
    half_turns = [m for m in t_fin if m['turn'] in ["Home SCORE First and LOSE", "Away SCORE First and LOSE"]]
    t_col1.metric("Σύνολο Ημιανατροπών", len(half_turns))
    t_col2.metric("Ανατροπή 1/2", len([m for m in t_fin if m['turn'] == "1/2"]))
    t_col3.metric("Ανατροπή 2/1", len([m for m in t_fin if m['turn'] == "2/1"]))
    st.write("---")
    if t_fin:
        for m in t_fin:
            h_n = TEAMS_MAP[m['h_id']]['n']; a_n = TEAMS_MAP[m['a_id']]['n']
            st.markdown(f"""<div class="turnaround-card"><span style="color:#06b6d4; font-size:12px; font-weight:bold;">{m['turn']}</span><br><b>{h_n} {m['sh']} - {m['sa']} {a_n}</b></div>""", unsafe_allow_html=True)
    else: st.info("Δεν έχουν σημειωθεί ανατροπές ακόμα.")

with tabs[5]:
    st.markdown("### 🌓 Στατιστικά Ημιχρόνων / Τελικών")
    st.write("Εμφάνιση αποτελεσμάτων HT/FT (εξαιρούνται οι πλήρεις ανατροπές 1/2 και 2/1).")
    htft_types = ["1/1", "1/X", "X/1", "X/X", "X/2", "2/X", "2/2"]
    all_htft = [m.get('htft','TBD') for m in st.session_state.wc_matches if m['fin'] and m.get('htft','TBD') in htft_types]
    cols_htft = st.columns(7)
    for idx, t_type in enumerate(htft_types):
        with cols_htft[idx]:
            count = all_htft.count(t_type)
            st_class = "score-out" if count > 0 else "score-delayed"
            st.markdown(f"""<div class="score-box {st_class}">{t_type}<br><span style='font-size:9px'>{'✅' if count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""", unsafe_allow_html=True)

# ΠΡΟΒΛΕΨΕΙΣ
with tabs[6]:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # ΑΥΤΟΜΑΤΗ ΕΠΙΛΟΓΗ ΜΟΝΤΕΛΟΥ
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            working_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            
            c1, c2 = st.columns(2)
            home_list = sorted([d['n'] for d in TEAMS_MAP.values()])
            h_t = c1.selectbox("Home Team", home_list, key="ai_h_final")
            a_t = c2.selectbox("Away Team", home_list, index=1, key="ai_a_final")
            match_number = st.number_input("Νούμερο Αγώνα (1-104):", 1, 104, 1, key="match_no_final")
            extra_notes = st.text_area("🗒️ Σημειώσεις τελευταίας στιγμής:", placeholder="Π.χ. Βρέχει, λείπει ο αρχηγός...")
            
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary", key="btn_final"):
                with st.spinner("Analyzing..."):
                    advanced_prompt = f"""
Είσαι ένας elite football analyst, data scientist και quant modeler με απόλυτη εξειδίκευση στο Παγκόσμιο Κύπελλο.
Ακολούθησε αυστηρά τη ΜΕΘΟΔΟΛΟΓΙΑ που περιγράφεται παρακάτω — σκέψου βήμα-βήμα (chain-of-thought) πριν βγάλεις οποιαδήποτε πρόβλεψη. Μεταξύ {h_t} εναντίον {a_t}.

Η ανάλυσή σου ΠΡΕΠΕΙ να βασίζεται σε πραγματικά δεδομένα, τα οποία θα επαληθεύσεις και θα αντλήσεις μέσω web search σε πραγματικό χρόνο.

════════════════════════════════════════
📌 ΔΕΔΟΜΕΝΑ ΑΓΩΝΑ & ΣΗΜΕΙΩΣΕΙΣ ΧΡΗΣΤΗ
════════════════════════════════════════
- Αγώνας #{match_number} | {h_t} vs {a_t} | Μουντιάλ 2026
- ΣΗΜΕΙΩΣΕΙΣ ΤΕΛΕΥΤΑΙΑΣ ΣΤΙΓΜΗΣ: {extra_notes if extra_notes else "Καμία πρόσθετη σημείωση."}

════════════════════════════════════════
📋 ΟΔΗΓΙΕΣ ΠΡΟΗΓΜΕΝΗΣ ΑΝΑΛΥΣΗΣ
════════════════════════════════════════

🧠 ΒΗΜΑΤΑ ΑΝΑΛΥΣΗΣ (Chain-of-Thought — εκτέλεσε ΟΛΑ)
════════════════════════════════════════════════════════
 
── ΒΗΜΑ 1: ΠΕΡΙΒΑΛΛΟΝ & ΔΙΑΙΤΗΣΙΑ ──────────────────────
• Εντόπισε τον ορισθέντα διαιτητή του αγώνα (web search αν χρειάζεται).
• Στατιστικά διαιτητή: κάρτες/90', πέναλτι/αγώνα, red cards/αγώνα, στυλ.
• Καιρός: θερμοκρασία (°C), υγρασία (%), άνεμος, βροχή.
→ Συμπέρανε: πόσες κάρτες αναμένεις, πιθανότητα πέναλτι, επίδραση καιρού στο πρέσινγκ.
 
── ΒΗΜΑ 2: ΔΥΝΑΜΙΚΗ ΤΟΥΡΝΟΥΑ (ΠΡΟΤΕΡΑΙΟΤΗΤΑ Νο1) ──────
• Αν οι ομάδες έχουν ήδη παίξει στο Μουντιάλ 2026, άντλησε:
  - xG & xGOT | Σουτ: Σύνολο/Στόχο/Blocked/Εντός-Εκτός Περιοχής
  - PPDA | Progressive passes | Aerial duels % | Δοκάρια
  - IN-PLAY PROFILE: πώς παίζει όταν προηγείται / υστερεί
  - Γκολ ανά ημίχρονο (1ο vs 2ο τάση)
  - Ρεαλιστικά στατιστικά για το Μουντιάλ 2026 ( web search )
• Αν είναι 1ος αγώνας: τελευταίοι 10 επίσημοι + προκριματικά.

2. ΔΥΝΑΜΙΚΗ ΦΟΡΜΑ ΤΟΥΡΝΟΥΑ (Από τη 2η Αγωνιστική & μετά - ΚΡΙΣΙΜΟ):
   - Αν οι ομάδες έχουν ήδη παίξει παιχνίδι/α στο Μουντιάλ 2026, η ανάλυση πρέπει να δώσει προτεραιότητα σε αυτά τα data έναντι των προκριματικών.
   - Ενσωμάτωσε υποχρεωτικά τις εξής advanced μετρικές από τα τρέχοντα παιχνίδια τους στη διοργάνωση:
     * Αναμενόμενα γκολ (xG) & xG στο στόχο (xGOT) για την ποιότητα των τελειωμάτων.
     * Συνολικά Σουτ, Σουτ στο στόχο, Άστοχα και Κομμένα (Blocked) σουτ.
     * Κατανομή: Σουτ εντός περιοχής vs Σουτ εκτός περιοχής.
     * Αποτελεσματικότητα στον αέρα (Γκολ με κεφαλιά) και ατυχία (Δοκάρια).
     * Ρεαλιστικά στατιστικά για το Μουντιάλ 2026 ( web search )

3. ΔΙΑΘΕΣΙΜΟΤΗΤΑ ΠΑΙΚΤΩΝ: Τραυματισμοί, τιμωρίες, επιστροφές της τελευταίας στιγμής (λαμβάνοντας υπόψη τις σημειώσεις του χρήστη).

4. HEAD-TO-HEAD & ΙΣΤΟΡΙΚΟ ΜΟΤΙΒΟ ΑΓΩΝΑ #{match_number}: 
   - Προηγούμενες αναμετρήσεις των δύο ομάδων.
   - Τι συνέβη ιστορικά στον συγκεκριμένο αριθμό αγώνα (#{match_number}) στα Μουντιάλ 2022, 2018 και 2014 (π.χ. αν παραδοσιακά ο αγώνας αυτός βγάζει πολλά γκολ, εκπλήξεις ή κόκκινες).

5. ΤΑΚΤΙΚΗ ΑΝΑΛΥΣΗ: Συστήματα (π.χ. 4-3-3, 3-5-2), transition, build-up, ευάλωτες ζώνες στην άμυνα και tactical matchup των key-players.

════════════════════════════════════════
📤 ΜΟΡΦΗ ΑΠΑΝΤΗΣΗΣ (αποκλειστικά Ελληνικά, Markdown)
════════════════════════════════════════

## ⚽ {h_t} vs {a_t} | Μουντιάλ 2026 — Αγώνας #{match_number}

---

### 📋 Ταυτότητα Αγώνα: Διαιτητής & Κλιματικές Συνθήκες
(Ανάλυση διαιτητή, καρτών, θερμοκρασίας/υγρασίας και η επίδρασή τους στο ρυθμό)

### 🏥 Διαθεσιμότητα, Ρόστερ & Last-Minute Updates
(Ενσωμάτωση σημειώσεων χρήστη και απουσιών/επιστροφών)

### 📊 Προηγμένη Ανάλυση Data & xG (Τρέχουσα Εικόνα)
(Εδώ ανάλυσε τη φόρμα. Αν είναι το 2ο+ παιχνίδι, κάνε ενδελεχή χρήση των xG, xGOT, κατανομής σουτ εντός/εκτός περιοχής, blocked shots, δοκαριών και κεφαλιών από τα ματς του Μουντιάλ. Αν είναι το 1ο ματς, βασίσου στα τελευταία 10 επίσημα)

### 🏟️ Ιστορικό Μοτίβο Αγώνα #{match_number}
(Η ιστορική αναδρομή του συγκεκριμένου slot αγώνα στις προηγούμενες διοργανώσεις)

### 🔮 Προηγμένο Μοντέλο Πρόβλεψης & Πιθανότητες
(Υπολόγισε τις πιθανότητες με βάση τα advanced metrics που ανέλυσες παραπάνω)

### 📋 Περιβάλλον Αγώνα
| Παράμετρος | Τιμή | Επίδραση |
|------------|------|----------|
| Διαιτητής | Όνομα (χώρα) | Αυστηρός/Επιεικής |
| Κάρτες/αγώνα | X.X 🟨 / X.X 🟥 | ... |
| Πέναλτι/αγώνα | X.XX | ... |
| Θερμοκρασία | X°C | ... |
| Υγρασία | X% | ... |
| Υψόμετρο | Xm | ... |
 
### 🏥 Ρόστερ & Διαθεσιμότητα
**{h_t}:** [Τραυματίες ✗] [Αμφίβολοι ⚠️] [Επιστροφές ✓]
**{a_t}:** [Τραυματίες ✗] [Αμφίβολοι ⚠️] [Επιστροφές ✓]
> 🔄 Σενάριο απουσίας: Αν λείπει ο [X], η πιθανότητα [Y] αλλάζει κατά ~X%
 
### 📊 Advanced Data & xG Dashboard
| Μετρική | {h_t} | {a_t} | Πλεονέκτημα |
|---------|--------|--------|-------------|
| xG | X.XX | X.XX | → |
| xGOT | X.XX | X.XX | → |
| Σουτ σύνολο | XX | XX | → |
| Σουτ στόχο | XX | XX | → |
| Εντός περιοχής | XX% | XX% | → |
| PPDA | X.X | X.X | → |
| Δοκάρια | X | X | → |
| Γκολ 1ο ημίχρονο | X | X | → |
| Γκολ 2ο ημίχρονο | X | X | → |
 
### ⚔️ Τακτική & Key Matchups
**Σχηματισμοί:** {h_t} [X-X-X] vs {a_t} [X-X-X]
- 🔑 Matchup #1: [A] vs [B] → [νικητής + λόγος]
- 🔑 Matchup #2: [C] vs [D] → [νικητής + λόγος]
- ⚠️ Ευάλωτη ζώνη {h_t}: [...]
- ⚠️ Ευάλωτη ζώνη {a_t}: [...]
- 🎯 Set pieces: [ποια ομάδα πλεονεκτεί]
 
### 🏟️ Ιστορικό Μοτίβο Αγώνα #{match_number}
| Διοργάνωση | Αγώνας | Σκορ | Γκολ | Κάρτες | Pattern |
|------------|--------|------|------|--------|---------|
| 2022 | A vs B | X-X | X | XY/XR | ... |
| 2018 | C vs D | X-X | X | XY/XR | ... |
| 2014 | E vs F | X-X | X | XY/XR | ... |
 
### 🔮 Quantitative Prediction Model
| Κατηγορία | Πρόβλεψη | Πιθανότητα | Βάση | Confidence |
|-----------|----------|------------|------|------------|
| Αποτέλεσμα (1-X-2) | {h_t}/Ισοπαλία/{a_t} | XX%/XX%/XX% | Bayesian xG | X/10 |
| Πιο πιθανό σκορ | X-X | XX% | Poisson | X/10 |
| Over 2.5 Goals | Ναι/Όχι | XX% | Συνολικό xG | X/10 |
| BTTS | Ναι/Όχι | XX% | Επιθ/Αμυν profile | X/10 |
| Over 9.5 Κάρτες | Ναι/Όχι | XX% | Referee + Ένταση | X/10 |
| Πέναλτι | Ναι/Όχι | XX% | Ref + Box attacks | X/10 |
| Κόκκινη Κάρτα | Ναι/Όχι | XX% | Ref + H2H | X/10 |
| Ανατροπή (In-play) | Ναι/Όχι | XX% | In-play profile | X/10 |
| Γκολ 1ου ημιχρόνου | Ναι/Όχι | XX% | 1ο ημίχρονο τάση | X/10 |
 
> 💡 **Value Bets:** [ποια πρόβλεψη έχει probability > implied probability αγοράς]
 
### 🎯 Στρατηγικό Συμπέρασμα
[3-4 προτάσεις: πού κρίνεται ο αγώνας, ποιο matchup καθορίζει, ποιος παράγοντας έχει τη μεγαλύτερη επίδραση]
 
**Συνολικό Confidence Score: X/10**
"""
                    ans = get_ai_prediction(working_model, advanced_prompt)
                    st.markdown("---")
                    st.markdown(ans)
        except Exception as e: st.error(f"AI Connection Error: {e}")
