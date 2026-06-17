import streamlit as st
import pandas as pd
import random.png", "g": "L"}, "46": {"n": "Croatia", "img": "
import google.generativeai as genai
import os
import json
from datetime import datetime, timedelta
https://flagcdn.com/w80/hr.png", "g": "L"},
    "from supabase import create_client, Client

# --- ΣΥΝΔΕΣΗ ΜΕ ΒΑΣΗ ΔΕ47": {"n": "Ghana", "img": "https://flagcdn.com/w80/ΔΟΜΕΝΩΝ (SUPABASE) ---
try:
    url = st.secrets["SUPABASEgh.png", "g": "L"}, "48": {"n": "Panama", "img":_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_ "https://flagcdn.com/w80/pa.png", "g": "L"}
}client(url, key)
except Exception as e:
    st.error("🚨 Σφάλμα Secrets: Βεβαιωθεί

RAW_MATCHES = [
    ["A", "11/06 22:00", "τε ότι έχετε βάλει σωστά τα SUPABASE_URL και SUPABASE_KEY.")

def loadEstadio Azteca", "1", "2"], ["A", "12/06 05:_from_db():
    try:
        response = supabase.table("tournament_persistence").select("data00", "Estadio Akron", "3", "4"],
    ["B", "12/06 22:00", "BMO Field", "5", "6"], ["D", "1").eq("id", 1).execute()
        if response.data and len(response.data) > 0:
            raw_3/06 04:00", "SoFi Stadium", "13", "14"],data = response.data[0]['data']
            if isinstance(raw_data, str):
                return json.loads
    ["D", "14/06 07:00", "BC Place", "1(raw_data)
            return raw_data
    except:
        pass
    return None

def5", "16"], ["B", "13/06 22:00", "Levi save_to_db(data):
    try:
        supabase.table("tournament_persistence").upsert({"id": 1,'s Stadium", "7", "8"],
    ["C", "14/06 01 "data": data}).execute()
    except Exception as e:
        st.error(f"Σφάλ:00", "MetLife Stadium", "9", "10"], ["C", "14/0μα αποθήκευσης: {e}")

# --- 1. CONFIG & CSS (COSMIC THE6 04:00", "Gillette Stadium", "11", "12"],
    ["ME) ---
st.set_page_config(page_title="World Cup 2026 ProE", "14/06 20:00", "NRG Stadium", "17", Stats", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
     "18"], ["F", "14/06 23:00", "AT&T Stadium", "21", "22"],
    ["E", "15/06 02.stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-:00", "Lincoln Field", "19", "20"], ["F", "15/0serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,6 05:00", "Estadio BBVA", "23", "24"],
    0); }
    h1, h2, h3, h4, h5, h6, label["H", "15/06 19:00", "Mercedes-Benz", "29, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important;", "30"], ["G", "15/06 22:00", "Lumen }
    .stat-card { background: #0f172a; border: 1px solid Field", "25", "26"],
    ["H", "16/06 01 #1e293b; border-radius: 12px; padding: 15px;:00", "Hard Rock", "31", "32"], ["G", "16/0 text-align: center; box-shadow: 0 4px 6px rgba(0, 06 04:00", "SoFi Stadium", "27", "28"],
    [", 0, 0.3); }
    .stat-val { font-size: 22J", "17/06 07:00", "Levi's Stadium", "39px; font-weight: 800; color: #06b6d4 !important; }", "40"], ["I", "16/06 10:00", "MetLife
    .stat-label { font-size: 9px; color: #94a3b8 !important;", "33", "34"],
    ["I", "17/06 01:00", "Gillette", "35", "36"], ["J", "17/06 text-transform: uppercase; }
    div[data-testid="stTable"] { background-color: #0f172a; 04:00", "Arrowhead", "37", "38"],
    ["K", border-radius: 10px; border: 1px solid #1e293b; padding "17/06 08:00", "NRG Stadium", "41", "4: 5px; }
    div[data-testid="stTable"] table { color: white !important;2"], ["L", "17/06 11:00", "AT&T Stadium", width: 100% !important; font-size: 12px !important; }
     "45", "46"],
    ["L", "18/06 02:00", "BMO Field", "47", "48"], ["K", "18/06 05:00",button[data-testid="stBaseButton-secondary"] { color: black !important; background-color: # "Estadio Azteca", "43", "44"],
    ["A", "18/0f1f5f9 !important; font-weight: 800 !important; border: 2px solid #ffffff !important; text-transform: uppercase; }
    .match-card { background: #0f172a; border: 1px solid #1e293b; border-radius6 07:00", "Mercedes-Benz", "4", "2"], ["B", "18/06 10:00", "SoFi Stadium", "8", "6"],
    : 16px; padding: 12px; margin-bottom: 10px; }
["B", "19/06 01:00", "BC Place", "5", "    .group-tag { background: rgba(6, 182, 212, 07"], ["A", "19/06 04:00", "Estadio Akron", ".2); color: #22d3ee !important; padding: 2px 10px;1", "3"],
    ["D", "20/06 06:00", " border-radius: 99px; font-size: 10px; font-weight: bold;Levi's Stadium", "16", "14"], ["D", "19/06 1 }
    button[data-testid="stBaseButton-primary"] { background-color: #ef440:00", "Lumen Field", "13", "15"],
    ["C", "44 !important; color: white !important; border: none !important; font-weight: 8020/06 01:00", "Gillette", "12", "10"],0 !important; }
    .score-box { padding: 10px; border-radius:  ["C", "20/06 03:30", "Lincoln Field", "9", "8px; text-align: center; margin: 5px; font-weight: bold; border: 11"],
    ["F", "21/06 07:00", "Estadio1px solid #1e293b; min-width: 65px; }
    . BBVA", "24", "22"], ["F", "20/06 08:score-out { background-color: #064e3b; color: #10b9800", "NRG Stadium", "21", "23"],
    ["E", "20/06 11:1 !important; border: 1px solid #10b981; }
    .score-00", "BMO Field", "17", "19"], ["E", "21/0delayed { background-color: #450a0a; color: #ef4444 !important6 03:00", "Arrowhead", "20", "18"],
    ["H; border: 1px solid #ef4444; opacity: 0.6; }
    ", "21/06 07:00", "Mercedes-Benz", "29", ".turnaround-card { background: #1e293b; padding: 10px; border31"], ["G", "21/06 10:00", "SoFi Stadium",-radius: 8px; margin-bottom: 5px; border-left: 4px solid # "25", "27"],
    ["H", "22/06 01:006b6d4; }
    </style>
    """, unsafe_allow_html=True)0", "Hard Rock", "32", "30"], ["G", "22/06 

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS_MAP =04:00", "BC Place", "28", "26"],
    ["J", " {
    "1": {"n": "Mexico", "img": "https://flagcdn.com/w22/06 08:00", "AT&T Stadium", "37", "380/mx.png", "g": "A"}, "2": {"n": "South Africa", "img": "https://flagcdn.com/w80/za.png", "g": "A"},9"], ["I", "23/06 12:00", "Lincoln Field", "33", "35"],

    "3": {"n": "South Korea", "img": "https://flagcdn.com/w    ["I", "23/06 03:00", "MetLife", "3680/kr.png", "g": "A"}, "4": {"n": "Czechia", "", "34"], ["J", "23/06 06:00", "Levi's Stadium", "40", "38"],
    ["K", "23/06 08:00", "NRG Stadium", "41", "43"], ["L", "23/06 11:00", "Gillette", "45", "47"],
    img": "https://flagcdn.com/w80/cz.png", "g": "A"},
    "5": {"n": "Canada", "img": "https://flagcdn.com/w80/ca.png", "g": "B"}, "6": {"n": "Bosnia", "img": "https://flagcdn.com/w80/ba.png", "g": "B"},
["L", "24/06 02:00", "BMO Field", "48    "7": {"n": "Qatar", "img": "https://flagcdn.com/w80", "46"], ["K", "24/06 05:00", "Estadio/qa.png", "g": "B"}, "8": {"n": "Switzerland", "img": " Akron", "44", "42"],
    ["B", "24/06 10:00", "BC Place", "8", "5"], ["B", "24/06 https://flagcdn.com/w80/ch.png", "g": "B"},
    "9": {"n": "Brazil", "img": "https://flagcdn.com/w80/br10:00", "Lumen Field", "6", "7"],
    ["C", "2.png", "g": "C"}, "10": {"n": "Morocco", "img": "5/06 01:00", "Hard Rock Stadium", "12", "9"], ["https://flagcdn.com/w80/ma.png", "g": "C"},
    "C", "25/06 01:00", "Mercedes-Benz", "10",11": {"n": "Haiti", "img": "https://flagcdn.com/w80 "11"],
    ["A", "25/06 04:00", "Est/ht.png", "g": "C"}, "12": {"n": "Scotland", "img": "https://flagcdn.com/w80/gb-sct.png", "g": "Cadio Azteca", "4", "1"], ["A", "25/06 04:00", "Estadio BBVA", "2", "3"],
    ["E", "25/0"},
    "13": {"n": "USA", "img": "https://flagcdn.com/6 11:00", "MetLife", "20", "17"], ["E", "w80/us.png", "g": "D"}, "14": {"n": "Paragu25/06 11:00", "Lincoln Field", "18", "19"],ay", "img": "https://flagcdn.com/w80/py.png", "g":
    ["F", "26/06 02:00", "AT&T Stadium", "D"},
    "15": {"n": "Australia", "img": "https://flagcdn. "22", "23"], ["F", "26/06 02:00",com/w80/au.png", "g": "D"}, "16": {"n": " "Arrowhead", "24", "21"],
    ["D", "26/06 Turkey", "img": "https://flagcdn.com/w80/tr.png", "g":05:00", "SoFi Stadium", "16", "13"], ["D", "2 "D"},
    "17": {"n": "Germany", "img": "https://flagcdn.6/06 05:00", "Levi's Stadium", "14", "15com/w80/de.png", "g": "E"}, "18": {"n": ""],
    ["I", "26/06 10:00", "Gillette", "Curacao", "img": "https://flagcdn.com/w80/cw.png", "g36", "33"], ["I", "26/06 10:00", "": "E"},
    "19": {"n": "Ivory Coast", "img": "https://BMO Field", "34", "35"],
    ["H", "27/06 flagcdn.com/w80/ci.png", "g": "E"}, "20": {"03:00", "Estadio Akron", "32", "29"], ["H", "2n": "Ecuador", "img": "https://flagcdn.com/w80/ec.png7/06 03:00", "NRG Stadium", "30", "31"],", "g": "E"},
    "21": {"n": "Netherlands", "img": "https
    ["G", "27/06 06:00", "Lumen Field", "://flagcdn.com/w80/nl.png", "g": "F"}, "22":26", "27"], ["G", "27/06 06:00", " {"n": "Japan", "img": "https://flagcdn.com/w80/jp.pngBC Place", "28", "25"],
    ["L", "28/06 1", "g": "F"},
    "23": {"n": "Sweden", "img": "https2:00", "MetLife", "48", "45"], ["L", "28/://flagcdn.com/w80/se.png", "g": "F"}, "24":06 12:00", "Lincoln Field", "46", "47"],
    [" {"n": "Tunisia", "img": "https://flagcdn.com/w80/tn.K", "28/06 02:30", "Hard Rock Stadium", "44",png", "g": "F"},
    "25": {"n": "Belgium", "img": " "41"], ["K", "28/06 02:30", "Mercedes-Benzhttps://flagcdn.com/w80/be.png", "g": "G"}, "26", "42", "43"],
    ["J", "28/06 05:": {"n": "Egypt", "img": "https://flagcdn.com/w80/eg.00", "Arrowhead", "38", "39"], ["J", "28/06png", "g": "G"},
    "27": {"n": "Iran", "img": " 05:00", "AT&T Stadium", "40", "37"]
]

https://flagcdn.com/w80/ir.png", "g": "G"}, "28# --- 4. SESSION STATE ---
def init_session():
    data = load_from_db()
    if data and len": {"n": "New Zealand", "img": "https://flagcdn.com/w80/nz(data) > 0:
        st.session_state.wc_matches = data
    else:.png", "g": "G"},
    "29": {"n": "Spain", "img": "https://flagcdn.com/w80/es.png", "g": "H"}, "3
        matches = []
        for i, m_data in enumerate(RAW_MATCHES):
            matches.append({
                "id": i+1, "group": m_data[0], "dt": m_data[10": {"n": "Cape Verde", "img": "https://flagcdn.com/w80/cv.png", "g": "H"},
    "31": {"n": "Saudi Arabia", "], "st": m_data[2],
                "h_id": m_data[3], "a_id": m_dataimg": "https://flagcdn.com/w80/sa.png", "g": "H"},[4], "sh": None, "sa": None, "fin": False,
                "y_h "32": {"n": "Uruguay", "img": "https://flagcdn.com/w": 0, "y_a": 0, "r_h": 0, "r_a80/uy.png", "g": "H"},
    "33": {"n": "France": 0, "p_h": 0, "p_a": 0, "og_h", "img": "https://flagcdn.com/w80/fr.png", "g": "": 0, "og_a": 0,
                "ref": "TBD", "turn": "Καμία", "I"}, "34": {"n": "Senegal", "img": "https://flagcdn.com/htft": "TBD"
            })
        st.session_state.wc_matches = matches

w80/sn.png", "g": "I"},
    "35": {"n": "if 'wc_matches' not in st.session_state:
    init_session()

# --- 5. FUNCTIONS ---
defIraq", "img": "https://flagcdn.com/w80/iq.png", "g": auto_play():
    for m in st.session_state.wc_matches:
        if not m "I"}, "36": {"n": "Norway", "img": "https://flagcdn.com/w80/no.png", "g": "I"},
    "37": {"n": "['fin']:
            m['sh'], m['sa'] = random.randint(0, 5), random.randint(0, 5Argentina", "img": "https://flagcdn.com/w80/ar.png", "g":)
            m['y_h'], m['y_a'] = random.randint(0, 3 "J"}, "38": {"n": "Algeria", "img": "https://flagcdn.com), random.randint(0, 3)
            m['r_h'] = random.randint(0, /w80/dz.png", "g": "J"},
    "39": {"n":1) if random.random() > 0.9 else 0
            m['r_a'] = "Austria", "img": "https://flagcdn.com/w80/at.png", "g random.randint(0, 1) if random.random() > 0.9 else 0
            ": "J"}, "40": {"n": "Jordan", "img": "https://flagcdn.comif m['sh'] > m['sa'] and random.random() > 0.85: m['/w80/jo.png", "g": "J"},
    "41": {"n":turn'] = "Home SCORE First and LOSE"
            elif m['sa'] > m['sh'] and "Portugal", "img": "https://flagcdn.com/w80/pt.png", "g random.random() > 0.85: m['turn'] = "Away SCORE First and LOSE"": "K"}, "42": {"n": "DR Congo", "img": "https://flagcdn.
            res = "X"
            if m['sh'] > m['sa']: res = "1"com/w80/cd.png", "g": "K"},
    "43": {"n
            elif m['sa'] > m['sh']: res = "2"
            m['htft']": "Uzbekistan", "img": "https://flagcdn.com/w80/uz.png = f"{random.choice(['1','X','2'])}/{res}"
            m['fin'] =", "g": "K"}, "44": {"n": "Colombia", "img": "https://flag True
    save_to_db(st.session_state.wc_matches)
    st.rercdn.com/w80/co.png", "g": "K"},
    "45":un()

def reset_tourney():
    st.session_state.wc_matches = []
    save {"n": "England", "img": "https://flagcdn.com/w80/gb-eng_to_db([])
    st.cache_data.clear()
    st.rerun()

@.png", "g": "L"}, "46": {"n": "Croatia", "img": "https://flagcdn.com/w80/hr.png", "g": "L"},
    "st.cache_data(ttl=3600)
def get_ai_prediction(model_id, prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY47": {"n": "Ghana", "img": "https://flagcdn.com/w80/"])
    model = genai.GenerativeModel(model_id)
    return model.generate_contentgh.png", "g": "L"}, "48": {"n": "Panama", "img":(prompt).text

# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUND "https://flagcdn.com/w80/pa.png", "g": "L"}
}IAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_

RAW_MATCHES = [
    ["A", "11/06 22:00", "m = [m for m in st.session_state.wc_matches if m.get('fin')]
total_y = sum(mEstadio Azteca", "1", "2"], ["A", "12/06 05:00", "Estadio Akron", "3", "4"],
    ["B", "12/0.get('y_h',0) + m.get('y_a',0) for m in fin_m)
total_r = sum(m.get('r_h',0) + m.get6 22:00", "BMO Field", "5", "6"], ["D", "13/06 04:00", "SoFi Stadium", "13", "14"],('r_a',0) for m in fin_m)
total_p = sum(m.get
    ["D", "14/06 07:00", "BC Place", "1('p_h',0) + m.get('p_a',0) for m in fin_m5", "16"], ["B", "13/06 22:00", "Levi's Stadium", "7", "8"],
    ["C", "14/06 01)
total_og = sum(m.get('og_h',0) + m.get('og_a',0) for m in fin_m)

c1, c2, c3, c4:00", "MetLife Stadium", "9", "10"], ["C", "14/0, c5, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div>6 04:00", "Gillette Stadium", "11", "12"],
    ["<div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2E", "14/06 20:00", "NRG Stadium", "17", "18"], ["F", "14/06 23:00", "AT&T: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m Stadium", "21", "22"],
    ["E", "15/06 02.get("sh",0)+m.get("sa",0) for m in fin_m if m.:00", "Lincoln Field", "19", "20"], ["F", "15/0get("sh") is not None)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_6 05:00", "Estadio BBVA", "23", "24"],
    allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><["H", "15/06 19:00", "Mercedes-Benz", "29div class="stat-val" style="color:#facc15!important">{total_y}</div><div class="stat-label">🟨Yellow</div></div>', unsafe_allow_html=True)
", "30"], ["G", "15/06 22:00", "Lumen Field", "25", "26"],
    ["H", "16/06 01with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef44:00", "Hard Rock", "31", "32"], ["G", "16/044!important">{total_r}</div><div class="stat-label">🟥Red</div></div>', unsafe6 04:00", "SoFi Stadium", "27", "28"],
    ["_allow_html=True)
with c5: st.markdown(f'<div class="stat-cardJ", "17/06 07:00", "Levi's Stadium", "39"><div class="stat-val" style="color:#22d3ee!important">{total_p}</div><div class="stat-", "40"], ["I", "16/06 10:00", "MetLifelabel">🎯Pens</div></div>', unsafe_allow_html=True)
with c6: st.markdown(", "33", "34"],
    ["I", "17/06 01:f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{total_og}</div><div class="stat-label">⚠️OG</div></div>', unsafe_allow_html=True)

00", "Gillette", "35", "36"], ["J", "17/06 04:00", "Arrowhead", "37", "38"],
    ["K", "17/06 08:00", "NRG Stadium", "41", "42"], ["L", "17/06 11:00", "AT&T Stadium", "45", "46"],
    ["L", "18/06 02:00", "BMO Fieldst.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ (SIMULATOR)", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset_tourney, type="secondary")

tabs = st.tabs(["📅 Η", "47", "48"], ["K", "18/06 05:00ΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "📊 ΑΝΑΛΥΣΗ ΣΚΟΡ", "", "Estadio Azteca", "43", "44"],
    ["A", "18/06 07:00", "Mercedes-Benz", "4", "2"], ["B", "🔄 ΑΝΑΤΡΟΠΕΣ", "🌓 ΗΜΙΧΡΟΝΑ / ΤΕΛΙΚΑ", "18/06 10:00", "SoFi Stadium", "8", "6"],
🔮 ΠΡΟΒΛΕΨΕΙΣ"])

with tabs[0]:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        h = TEAMS_MAP.get(m['h_id'], {"n": "N/A", "img": ""})
        a    ["B", "19/06 01:00", "BC Place", "5", "7"], ["A", "19/06 04:00", "Estadio Akron", "1", "3"],
    ["D", "20/06 06:00", = TEAMS_MAP.get(m['a_id'], {"n": "N/A", "img": ""})
        with cols[idx % 3]:
            st.markdown(f"""<div class "Levi's Stadium", "16", "14"], ["D", "19/06 10:00", "Lumen Field", "13", "15"],
    ["C",="match-card">
                <div style="display:flex; justify-content: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
 "20/06 01:00", "Gillette", "12", "10"], ["C", "20/06 03:30", "Lincoln Field", "9",                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space- "11"],
    ["F", "21/06 07:00", "Estadio BBVA", "24", "22"], ["F", "20/06 08:00", "NRG Stadium", "21", "23"],
    ["E", "2around; align-items:center;">
                    <div style="text-align:center; width:400/06 11:00", "BMO Field", "17", "19"], ["E", "21/%; font-weight:bold;"><img src="{h['img']}" width="25"><br>{h['n']}</div>
                    <div style="font-size:20px; color:#06b6d06 03:00", "Arrowhead", "20", "18"],
    ["H", "21/06 07:00", "Mercedes-Benz", "29",4; font-weight:800;">{m.get('sh','-') if m.get('sh "31"], ["G", "21/06 10:00", "SoFi Stadium') is not None else '-'} : {m.get('sa','-') if m.get('sa') is not None else '-'}</div>
                    <div style="text-align:center; width:40%;"><img src="{a['img", "25", "27"],
    ["H", "22/06 01:']}" width="25"><br>{a['n']}</div>
                </div>
                <div style="font00", "Hard Rock", "32", "30"], ["G", "22/06 04:00", "BC Place", "28", "26"],
    ["J",-size:9px; color:#94a3b8; text-align:center; border-top "22/06 08:00", "AT&T Stadium", "37", ": 1px solid #1e293b; padding-top:4px;">
                    🟨 {m.get('y_h',0)}:{m.get('y_a',0)}39"], ["I", "23/06 12:00", "Lincoln Field", "33", "35"],
    ["I", "23/06 03:00", "MetLife", "36", "34"], ["J", "23/06 0 | 🟥 {m.get('r_h',0)}:{m.get('r_a',0)} | 🎯 {m.get('p_h',0)}:{m.get('p_a',6:00", "Levi's Stadium", "40", "38"],
    ["K",0)} | ⚠️ {m.get('og_h',0)}:{m.get('og_a "23/06 08:00", "NRG Stadium", "41", "4',0)}
                </div>
                <div style="font-size:9px; color:#94a3b8; text-align:center; padding-top:2px;">
                    🏁 Ref: {m3"], ["L", "23/06 11:00", "Gillette", "45", "47"],
    ["L", "24/06 02:00",.get('ref','TBD')} | 📍 {m.get('st','TBD')} | 🔄 "BMO Field", "48", "46"], ["K", "24/06 0 {m.get('turn','Καμία')} | 🌓 {m.get('htft','TBD')}5:00", "Estadio Akron", "44", "42"],
    ["B", "24/06 10:00", "BC Place", "8", "5"], ["B
                </div>
            </div>""", unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργ", "24/06 10:00", "Lumen Field", "6", "7ασία"):
                ch, ca = st.columns(2)
                sh_v = ch.number_input(f"Goals {h['n']}", 0, 15, m.get('sh',0) if m.get('sh') is not None else 0, key=f"sh{m['"],
    ["C", "25/06 01:00", "Hard Rock Stadium", "12", "9"], ["C", "25/06 01:00", "Mercedes-Benz", "10", "11"],
    ["A", "25/06 id']}")
                sa_v = ca.number_input(f"Goals {a['n']}", 0, 15, m.get('sa',0) if m.get('sa') is not None04:00", "Estadio Azteca", "4", "1"], ["A", "25 else 0, key=f"sa{m['id']}")
                yh_v = ch.slider(f/06 04:00", "Estadio BBVA", "2", "3"],
    ["E", "25/06 11:00", "MetLife", "20","Yellow {h['n']}", 0, 10, m.get('y_h',0 "17"], ["E", "25/06 11:00", "Lincoln Field",), key=f"yh{m['id']}")
                ya_v = ca.slider(f"Yellow {a['n']}", 0, 10, m.get('y_a',0), key "18", "19"],
    ["F", "26/06 02:0=f"ya{m['id']}")
                rh_v = ch.number_input(f"Red0", "AT&T Stadium", "22", "23"], ["F", "26/06 02:00", "Arrowhead", "24", "21"],
    ["D {h['n']}", 0, 5, m.get('r_h',0), key=", "26/06 05:00", "SoFi Stadium", "16", "f"rh{m['id']}")
                ra_v = ca.number_input(f"Red {a['n']}", 0, 5, m.get('r_a',0), key=f"ra{m['id']}")
                ph_v = ch.number_input(f"Pens {h['n']}", 0, 5, m.get('p_h',0), key=f"ph{m['id']}")
                pa_v = ca.number_input(f"Pens {a['n']}", 0, 5, m.get('p_a',0), key=f"pa{m['id']}")
                oh_v = ch.number_input(f"OG {h['n']}", 0, 5, m.get('og_h',0), key=f"oh{13"], ["D", "26/06 05:00", "Levi's Stadium", "14", "15"],
    ["I", "26/06 10:00", "Gillette", "36", "33"], ["I", "26/06 10:00", "BMO Field", "34", "35"],
    ["Hm['id']}")
                oa_v = ca.number_input(f"OG {a['n']}", 0, 5, m.get('og_a',0), key=f"oa{m", "27/06 03:00", "Estadio Akron", "32", "29"], ["H", "27/06 03:00", "NRG Stadium", "30", "31"],
    ["G", "27/06 06:00", "Lumen Field", "26", "27"], ["G", "27/06 06:00", "BC Place", "28", "25"],
    ["L", "28/06 ['id']}")
                ref_v = st.text_input("Referee", m.get('ref','T12:00", "MetLife", "48", "45"], ["L", "28BD'), key=f"ref_in{m['id']}")
                turn_v = st.selectbox("/06 12:00", "Lincoln Field", "46", "47"],
    Ανατροπή", ["Καμία", "Home SCORE First and LOSE", "Away SCORE First and LOSE["K", "28/06 02:30", "Hard Rock Stadium", "44", "1/2", "2/1"], index=0, key=f"turn_{m['id", "41"], ["K", "28/06 02:30", "Mercedes-']}")
                htft_v = st.selectbox("Ημίχρονο/Τελικό", ["TBD", "1/1", "1/X", "1/2", "X/1", "X/X", "X/2Benz", "42", "43"],
    ["J", "28/06 05:00", "Arrowhead", "38", "39"], ["J", "28/06 05:00", "AT&T Stadium", "40", "37"]
]", "2/1", "2/X", "2/2"], index=0, key=f"htft_{m['id']}")

# --- 4. SESSION STATE ---
if 'wc_matches' not in st.session_state:
                if st.button("Save Result", key=f"btn{m['id']}"):
                    m.
    data = load_from_db()
    if data: st.session_state.wc_matchesupdate({"sh": sh_v, "sa": sa_v, "fin": True, "y_h = data
    else:
        matches = []
        for i, m_data in enumerate(RAW_MATCHES):
": yh_v, "y_a": ya_v, "r_h": rh_v, "r_a":            matches.append({
                "id": i+1, "group": m_data[0], "dt": m_data[1 ra_v, "p_h": ph_v, "p_a": pa_v, "og], "st": m_data[2],
                "h_id": m_data[3], "a_id": m_data_h": oh_v, "og_a": oa_v, "ref": ref_v, "turn": turn_v, "[4], "sh": None, "sa": None, "fin": False,
                "y_h": 0, "y_a": 0, "r_h": 0, "r_ahtft": htft_v})
                    save_to_db(st.session_state.wc_matches)
                    st.rerun()

with tabs[1]:
    cols_s = st.columns(3)
    GROUPS_L = ["A", "B", "C", "D", "E": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_", "F", "G", "H", "I", "J", "K", "L"]
    a": 0,
                "ref": "TBD", "turn": "Καμία", "htft": "TBD"
for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_team_ids = [            })
        st.session_state.wc_matches = matches

# --- 5. FUNCTIONS ---
tid for tid, d in TEAMS_MAP.items() if d['g'] == gId]
            def auto_play():
    for m in st.session_state.wc_matches:
        if notres = []
            for tid in g_team_ids:
                team = TEAMS_MAP[tid m['fin']:
            m['sh'], m['sa'] = random.randint(0, 5), random.randint(0, 5)
            m['y_h'], m['y_a'] = random.randint(0]
                pts, gd, y, r = 0, 0, 0, 0
                for m in st.session_, 3), random.randint(0, 3)
            m['r_h'] = random.randint(0, state.wc_matches:
                    if m.get('fin') and (m.get('h_id') == tid or m.get('a_id') == tid):
                        is_h = m.get2) if random.random() > 0.9 else 0
            m['r_a'] = random('h_id') == tid
                        h_s, a_s = (m.get('sh',.randint(0, 2) if random.random() > 0.9 else 0
            if m['sh'] > m['sa'] and random.random() > 0.85: m['turn'] = "Home SCORE First and LOSE"
            elif m['sa'] > m['sh'] and random0), m.get('sa',0)) if is_h else (m.get('sa',0), m.get('sh',0))
                        y += m.get('y_h',0) if is_h else m.get('y_a',0)
                        r += m.get('r_h',0) if is_h.random() > 0.85: m['turn'] = "Away SCORE First and LOSE"
            res = "X"
            if m['sh'] > m['sa']: res = "1"
 else m.get('r_a',0)
                        gd += (h_s - a_s)            elif m['sa'] > m['sh']: res = "2"
            m['htft'] = f"{random.choice(['1','X','2'])}/{res}"
            m['fin'] = True
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                res.append({"Flag": team['img'], "Team": team['n
    save_to_db(st.session_state.wc_matches)
    st.rerun()

def reset_all_tournament():
    save_to_db([])
    st.session_state'], "Pts": pts, "GD": gd, "Y": y, "R": r})
            df.clear()
    st.cache_data.clear()
    st.rerun()

@st. = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
            cache_data(ttl=3600)
def get_ai_prediction(prompt):
    apist.data_editor(df, column_config={"Flag": st.column_config.ImageColumn("🏳️")}, hide_index=True, key=f"table_{gId}")

with tabs[2]:_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key
    all_names = sorted([d['n'] for d in TEAMS_MAP.values()])
    sel_t = st.selectbox("Επιλέξτε Ομάδα:", all_names)
    team_id = next(k for k,v in TEAMS_MAP.items() if v['n'] ===api_key)
    # Θωρακισμένη κλήση χωρίς models/ πρόθεμα (το sel_t)
    t_matches = [m for m in st.session_state.wc_matches SDK το βάζει μόνο του)
    model = genai.GenerativeModel(model_name='gemini-1 if (m.get('h_id') == team_id or m.get('a_id') ==.5-flash', tools=[{"google_search": {}}])
    return model.generate_content(prompt).text

# --- 6. HEADER ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO team_id)]
    t_pts, t_gf, t_ga, t_y, t_r = 0, 0, 0, 0, 0
    for m in t_matches:
        if m.get('fin'):
            is_h = m.get('h_id') == team_id
            g, c = (m.get('sh',0), m.get('sa',0)) if is STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m in st.session_state.wc_matches if m.get('fin')]
c1, c2, c3, c4, c5_h else (m.get('sa',0), m.get('sh',0))
            t_gf += g; t_ga += c
            t_y += m.get('y_h',0) if is_h else m.get('y_a',0)
            if g > c: t_pts += 3
, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m.get("sh",0)+m            elif g == c: t_pts += 1
    c_s1, c_s2, c_s3.get("sa",0) for m in fin_m)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_, c_s4 = st.columns(4)
    c_s1.metric("Points", t_pts); c_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><s2.metric("Goals", f"{t_gf}-{t_ga}"); c_s3.metric("div class="stat-val" style="color:#facc15!important">{sum(m.get("y_h",0)+m.get("y_a",0) for m in fin_m)}</div>Cards (Y)", t_y)
    cols_team = st.columns(3)
    for idx, m in enumerate(t_matches):
        with cols_team[idx % 3]:
            res_col = "#<div class="stat-label">🟨Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444!important">{sum(m.get("r_h",0)+m.get("r_a",0) for m in fin_m)}</div><div class="stat10b981" if m.get('fin') else "#1e293b"
            h_n = TEAMS_MAP[m.get('h_id')]['n']; a_n = TEAMS_MAP[m.get('a_id')]['n']
            st.markdown(f"""<div class="match--label">🟥Red</div></div>', unsafe_allow_html=True)
with c5: st.markdowncard" style="border-top:4px solid {res_col}">
            <b>Αγώνας {(f'<div class="stat-card"><div class="stat-val" style="color:#22didx+1}</b><br>{h_n} {m.get('sh') if m.get('sh') is not None else ''} - {m.get('sa') if m.get('sa') is not None else ''} {a_n}
            </div>""", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 📊 Πίνακας Πιθανών Σκο3ee!important">{sum(m.get("p_h",0)+m.get("p_a",0) for m in fin_m)}</div><div class="stat-label">🎯Pens</div></div>',ρ & Συχνότητας")
    actual_scores = [(m.get('sh'), m.get('sa')) for m in st.session_state.wc_matches if m.get('fin')]
    grid_ unsafe_allow_html=True)
with c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{sum(msize = 6 
    for h_g in range(grid_size):
        cols_score = st.columns(grid_size)
        for a_g in range(grid_size):
            with.get("og_h",0)+m.get("og_a",0) for m in fin_m)}</div><div class="stat-label">⚠️OG</div></div>', unsafe_allow_html=True) cols_score[a_g]:
                h_label = str(h_g) if h_g

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ (SIMULATOR)", on_ < 5 else "5+"
                a_label = str(a_g) if a_g <click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset_all_tournament, type="secondary")

tabs = st.tabs(["📅 5 else "5+"
                def check(sh, sa, target_h, target_a):
                    if sh is None or sa is None: return False
                    h_ok = (sh == target_h) if target_h < ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "📊 ΑΝΑΛΥΣΗ ΣΚΟΡ", "🔄 ΑΝΑΤΡΟΠΕΣ", "🌓 ΗΜΙΧΡΟΝΑ / ΤΕΛΙΚΑ", "🔮 ΠΡΟ 5 else (sh >= 5)
                    a_ok = (sa == target_a) if target_a < 5 else (sa >= 5)
                    return h_ok and a_ok
                count = sum(1 for sh, sa in actual_scores if check(sh, sa, h_g, a_g))
                stΒΛΕΨΕΙΣ"])

with tabs[0]: # ΗΜΕΡΟΛΟΓΙΟ
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        _class = "score-out" if count > 0 else "score-delayed"
                st.markdown(f"""<div class="score-box {st_class}">{h_label}-{a_label}<h = TEAMS_MAP.get(m['h_id'], {"n": "N/A", "img": ""})
        a = TEAMS_MAP.get(m['a_id'], {"n": "N/A", "imgbr><span style='font-size:9px'>{'✅' if count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""", unsafe_allow_html=True)

with tabs": ""})
        with cols[idx % 3]:
            st.markdown(f"""<div class="match-card">
                <div style="display:flex; justify-content: space-between; margin[4]:
    st.markdown("### 🔄 Ανάλυση Ανατροπών (Turnarounds)")
    t_fin = [m for m in st.session_state.wc_matches if m.get('-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-fin') and m.get('turn','Καμία') != "Καμία"]
    t_col1, t_col2, t_col3 = st.columns(3)
    half_turns = [m for m in t_fin if m.get('turn') in ["Home SCORE First and LOSE", "Away SCORE First and LOSE"]]
    t_col1.metric("Σύνολο Ημιανατροπών", len(half_turns))
    t_col2.metric("Ανατροπή 1/around; align-items:center;">
                    <div style="text-align:center; width:40%; font-weight:bold;"><img src="{h['img']}" width="25"><br>{h['n']}2", len([m for m in t_fin if m.get('turn') == "1/2"]))
    t_col3.metric("Ανατροπή 2/1", len([m for m in</div>
                    <div style="font-size:20px; color:#06b6d4; t_fin if m.get('turn') == "2/1"]))
    st.write("---") font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="
    if t_fin:
        for m in t_fin:
            h_n = TEAMS_MAP[m.get('h_id')]['n']; a_n = TEAMS_MAP[m.get('a_id')]['n']
            st.markdown(f"""<div class="turnaround-card"><span style="colortext-align:center; width:40%;"><img src="{a['img']}" width="25"><br>{a['n']}</div>
                </div>
                <div style="font-size:9px;:#06b6d4; font-size:12px; font-weight:bold;">{m.get('turn')}</span><br><b>{h_n} {m.get('sh')} - { color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:4px;">
                    🟨 {m.getm.get('sa')} {a_n}</b></div>""", unsafe_allow_html=True)
    else: st.info("Δεν έχουν σημειωθεί ανατροπές ακόμα.")

with tabs[5]:('y_h',0)}:{m.get('y_a',0)} | 🟥 {m.get('r_h',0)}:{m.get('r_a',0)} | 🎯 {m
    st.markdown("### 🌓 Στατιστικά Ημιχρόνων / Τελικών")
.get('p_h',0)}:{m.get('p_a',0)} | ⚠️ {    htft_types = ["1/1", "1/X", "X/1", "X/X", "X/2", "2/X", "2/2"]
    all_htft = [m.get('htm.get('og_h',0)}:{m.get('og_a',0)}
                </div>
                <div style="font-size:9px; color:#94a3b8; text-align:center; padding-top:2px;">
                    🏁 Ref: {m.get('ref','TBD')} | 📍 {m.get('st','TBD')} | 🔄 {m.get('turnft','TBD') for m in st.session_state.wc_matches if m.get('fin') and m.get('htft','TBD') in htft_types]
    cols_htft =','Καμία')} | 🌓 {m.get('htft','TBD')}
                </div>
            </div> st.columns(7)
    for idx, t_type in enumerate(htft_types):
        with cols_htft[idx]:
            count = all_htft.count(t_type)
""", unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columns(2)
                sh_v = ch.number_input            st_class = "score-out" if count > 0 else "score-delayed"
            st(f"Goals {h['n']}", 0, 15, m.get('sh',0) if m.get('sh') is not None else 0, key=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {a['n']}", 0, 15, m..markdown(f"""<div class="score-box {st_class}">{t_type}<br><span style='font-size:9px'>{'✅' if count > 0 else '⏳'} {count if count > 0 elseget('sa',0) if m.get('sa') is not None else 0, key=f" ''}</span></div>""", unsafe_allow_html=True)

with tabs[6]:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ (Advanced AI)")
    api_key =sa{m['id']}")
                yh_v = ch.slider(f"Yellow {h['n']}", 0, 10, m.get('y_h',0), key=f"yh{m['id']}")
                ya st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # ΑΥΤΟΜΑΤΗ ΕΠΙΛΟΓΗ ΜΟΝΤΕΛΟΥ ΜΕΣΩ ΑΝΑΖΗΤΗΣΗΣ ΓΙΑ ΑΠΟΦΥΓ_v = ca.slider(f"Yellow {a['n']}", 0, 10, m.get('y_a',0), key=f"ya{m['id']}")
                rh_vΗ 404
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            working_model = 'models/ = ch.number_input(f"Red {h['n']}", 0, 5, m.get('r_h',0), key=f"rh{m['id']}")
                ra_v =gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
            
            c1, c2 = st.columns(2 ca.number_input(f"Red {a['n']}", 0, 5, m.get('r_a',0), key=f"ra{m['id']}")
                ph_v = ch.number_input(f"Pens {h['n']}", 0, 5, m.get(')
            h_t = c1.selectbox("Home Team", all_names, key="ai_hp_h',0), key=f"ph{m['id']}")
                pa_v = ca.number_input(f"Pens {a['n']}", 0, 5, m.get('p_final")
            a_t = c2.selectbox("Away Team", all_names, index=1, key="ai_a_final")
            match_number = st.number_input("Νούμερο_a',0), key=f"pa{m['id']}")
                oh_v = ch.number_input(f"OG {h['n']}", 0, 5, m.get('og_ Αγώνα (1-104):", 1, 104, 1, key="match_no_final")
            extra_notes = st.text_area("🗒️ Σημειώσειςh',0), key=f"oh{m['id']}")
                oa_v = ca.number_ τελευταίας στιγμής:", placeholder="Π.χ. Βρέχει, λείπει ο αρχηγός...")input(f"OG {a['n']}", 0, 5, m.get('og_a',0), key=f"oa{m['id']}")
                ref_v = st.text_input
            
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary("Referee", m.get('ref','TBD'), key=f"ref_in{m['id']}")
                turn_v = st.selectbox("Ανατροπή", ["Καμία", "Home SCORE First and LOSE", "Away SCORE First and LOSE", "1/2", "2/1"], index=0", key="btn_final"):
                with st.spinner("Analyzing..."):
                    # ΕΝΣΩΜΑΤΩΣΗ ΤΩΝ ΔΙΠΛΩΝ ΑΓΚΙΣΤΡΩΝ ΣΤΟ ΠΡΟΜΠΤ ΓΙΑ ΑΠΟΦΥΓΗ ΣΦΑΛΜΑΤΩΝ
                    advanced_prompt = f"""
Είσαι ένας elite football, key=f"turn_{m['id']}")
                htft_v = st.selectbox("Ημίχρονο/Τελικό", ["TBD", "1/1", "1/X", "1/ analyst, data scientist και quant modeler με απόλυτη εξειδίκευση στο Παγκόσμιο2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"], index=0, key=f"htft_{m['id']}")
                if st.button("Save Κύπελλο.
Ακολούθησε αυστηρά τη ΜΕΘΟΔΟΛΟΓΙΑ που περιγράφεται παρακάτω — σκέψου βήμα-βήμα (chain-of-thought) πριν βγάλεις οποιαδήποτε πρόβλεψη. Μεταξύ {h_t} εναν Result", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v,τίον {a_t}.

Η ανάλυσή σου ΠΡΕΠΕΙ να βασίζεται σε πραγματικά δεδομένα, τα οποία θα επαληθεύσεις και θα αντλήσεις μέσω web search σε πραγματικό χρόνο.

════ "sa": sa_v, "fin": True, "y_h": yh_v, "y_a": ya_v, "r_h": rh_v, "r_a": ra_v, "p_h": ph_v, "p_a": pa_v, "og_h": oh_v, "og════════════════════════════════════
📌 ΔΕΔΟΜΕΝΑ ΑΓΩΝΑ & ΣΗΜΕΙΩΣΕΙΣ ΧΡΗΣΤΗ
════════════════════════════════════════
- Αγώνας #{match_number} | {h_t} vs {a_t} | Μουν_a": oa_v, "ref": ref_v, "turn": turn_v, "htft": htft_v})
τιάλ 2026
- ΣΗΜΕΙΩΣΕΙΣ ΤΕΛΕΥΤΑΙΑΣ ΣΤΙΓΜΗΣ: {extra_notes if extra_notes else "Καμία πρόσθετη σημείωση."}

🧠 ΒΗΜΑ                    save_to_db(st.session_state.wc_matches); st.rerun()

with tabs[1]: # ΒΑΘΜΟΛΟΓΙΕΣ
    cols_s = st.columns(3)
    GROUPS_L = ["A", "B", "C", "D", "E",ΤΑ ΑΝΑΛΥΣΗΣ
1. ΔΙΑΙΤΗΤΗΣ & ΚΑΙΡΟΣ: Βρες ποιος σφυρίζ "F", "G", "H", "I", "J", "K", "L"]
    for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:ει στον αγώνα #{match_number} και τι καιρό θα κάνει.
2. ΦΟΡΜΑ: xG και αποτελέσματα τελευταίων αγώνων.
3. ΙΣΤΟΡΙΚΟ: Τι έγινε ιστορικά στον
            st.markdown(f"#### Group {gId}")
            g_team_ids = [tid for tid, d in TEAMS_MAP.items() if d['g'] == gId]
            res αγώνα #{match_number} το 2022, 2018 και 2014.

ΑΠΑΝΤΗΣΗ (Ελληνικά):
## ⚽ {h_t} = []
            for tid in g_team_ids:
                team = TEAMS_MAP[tid] vs {a_t}
### 📋 Ταυτότητα Αγώνα: Διαιτητής & Καιρός

                pts, gd, y, r, p, og = 0, 0, 0, 0, 0, 0
                for m in st.session_state.wc_matches:
                    ### 🏥 Διαθεσιμότητα & Σημειώσεις
### 📊 Data & xG Analysis
### 🏟️ Ιif m.get('fin') and (m.get('h_id') == tid or m.get('a_id') == tid):
                        is_h = m.get('h_id') == tid
                        h_s,στορικό Μοτίβο Αγώνα #{match_number}
### 🔮 Quantitative Prediction Model
| Κατηγορία | Πρόβλεψη | Πιθανότητα |
|-----------|----------|------------|
| 1-X-2 | ... | XX% |
| Σκορ | X-X | — | a_s = (m.get('sh',0), m.get('sa',0)) if is_
| Πέναλτι | Ναι/Όχι | XX% |
| Κόκκινη | Ναι/Όχι | XX% |
| Ανατροπή | Ναι/Όχι | XX%h else (m.get('sa',0), m.get('sh',0))
                        y += m.get('y_h',0) if is_h else m.get('y_a',0)
                        r += m. |
"""
                    ans = get_ai_prediction(working_model, advanced_prompt)
                    stget('r_h',0) if is_h else m.get('r_a',0)
.markdown("---")
                    st.markdown(ans)
        except Exception as e: st.error(f"AI Connection Error: {e}")
```                        p += m.get('p_h',0) if is_h else m.get('p_a',0)
                        og += m.get('og_h',0) if is_h else m.get('og_a',0)
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
