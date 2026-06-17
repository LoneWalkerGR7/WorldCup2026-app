import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
import json
from datetime import datetime
from supabase import create_client, Client

# --- ΣΥΝΔΕΣΗ ΜΕ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (SUPABASE) ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("🚨 Σφάλμα Secrets: Ελέγξτε τα SUPABASE_URL και SUPABASE_KEY.")

def load_from_db():
    try:
        response = supabase.table("tournament_persistence").select("data").eq("id", 1).execute()
        if response.data and len(response.data) > 0:
            raw_data = response.data[0]['data']
            return json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    except: pass
    return None

def save_to_db(data):
    try: supabase.table("tournament_persistence").upsert({"id": 1, "data": data}).execute()
    except Exception as e: st.error(f"Σφάλμα αποθήκευσης: {e}")

# --- 1. CONFIG & CSS ---
st.set_page_config(page_title="World Cup 2026 Pro Stats", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: white !important; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, label, p, span { color: white !important; }
    .stat-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 15px; text-align: center; }
    .stat-val { font-size: 22px; font-weight: 800; color: #06b6d4 !important; }
    .stat-label { font-size: 9px; color: #94a3b8 !important; text-transform: uppercase; }
    .match-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 12px; margin-bottom: 10px; }
    .group-tag { background: rgba(6, 182, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; }
    .score-box { padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; border: 1px solid #1e293b; }
    .score-out { background-color: #064e3b; color: #10b981 !important; border: 1px solid #10b981; }
    .score-delayed { background-color: #450a0a; color: #ef4444 !important; border: 1px solid #ef4444; opacity: 0.6; }
    button[data-testid="stBaseButton-primary"] { background-color: #ef4444 !important; border: none !important; }
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
    data = load_from_db()
    if data: st.session_state.wc_matches = data
    else:
        st.session_state.wc_matches = [{
            "id": i+1, "group": m[0], "dt": m[1], "st": m[2], "h_id": m[3], "a_id": m[4],
            "sh": None, "sa": None, "fin": False, "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0,
            "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0, "ref": "TBD", "turn": "Καμία", "htft": "TBD"
        } for i, m in enumerate(RAW_MATCHES)]

if 'wc_matches' not in st.session_state: init_session()

# --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0, 4), random.randint(0, 4)
            m['fin'] = True
    save_to_db(st.session_state.wc_matches); st.rerun()

def reset_all():
    save_to_db([]); st.session_state.clear(); st.rerun()

# --- 6. AI ANALYZER ---
def get_ai_prediction(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Προσπάθεια για Web Search Grounding
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', tools=[{"google_search": {}}])
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        # Fallback αν το search βγάλει quota error ή 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text

# --- UI LAYOUT ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_count = len([m for m in st.session_state.wc_matches if m['fin']])
st.button("⚡ SIMULATE ALL", on_click=auto_play, type="primary")
st.button("🔄 RESET", on_click=reset_all)

tabs = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

with tabs[0]:
    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.wc_matches):
        h = TEAMS_MAP[m['h_id']]; a = TEAMS_MAP[m['a_id']]
        with cols[idx % 3]:
            st.markdown(f"""<div class="match-card">
                <b>GROUP {m['group']}</b> | {m['dt']}<br>
                {h['n']} {m['sh'] if m['sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-'} {a['n']}
            </div>""", unsafe_allow_html=True)

with tabs[1]:
    GROUPS = sorted(list(set(d['g'] for d in TEAMS_MAP.values())))
    cols_g = st.columns(3)
    for i, gId in enumerate(GROUPS):
        with cols_g[i % 3]:
            st.write(f"### Group {gId}")
            t_ids = [tid for tid, d in TEAMS_MAP.items() if d['g'] == gId]
            res = []
            for tid in t_ids:
                pts = 0
                for m in st.session_state.wc_matches:
                    if m['fin'] and (m['h_id'] == tid or m['a_id'] == tid):
                        is_h = m['h_id'] == tid
                        hs, a_s = (m['sh'], m['sa']) if is_h else (m['sa'], m['sh'])
                        if hs > a_s: pts += 3
                        elif hs == a_s: pts += 1
                res.append({"Team": TEAMS_MAP[tid]['n'], "Pts": pts})
            st.table(pd.DataFrame(res).sort_values("Pts", ascending=False))

with tabs[2]:
    st.write("### 🔮 AI PREDICTION ENGINE")
    h_sel = st.selectbox("Home", sorted([t['n'] for t in TEAMS_MAP.values()]), key="h_s")
    a_sel = st.selectbox("Away", sorted([t['n'] for t in TEAMS_MAP.values()]), key="a_s")
    m_no = st.number_input("Match #", 1, 104, 1)
    
    if st.button("ΑΝΑΛΥΣΗ ΤΩΡΑ"):
        with st.spinner("Searching Live Data..."):
            # Context από το Simulator
            prev_results = [f"{TEAMS_MAP[m['h_id']]['n']} {m['sh']}-{m['sa']} {TEAMS_MAP[m['a_id']]['n']}" 
                           for m in st.session_state.wc_matches if m['fin']]
            
            prompt = f"""
            Σήμερα είναι 17 Ιουνίου 2026. Είσαι elite αναλυτής.
            Αγώνας: {h_sel} vs {a_sel} (Match #{m_no}).
            
            Δεδομένα Simulator (μέχρι στιγμής):
            {", ".join(prev_results[-10:]) if prev_results else "Πρώτος αγώνας."}
            
            ΟΔΗΓΙΕΣ:
            1. Κάνε Web Search για τον επίσημο διαιτητή του αγώνα #{m_no} και τον καιρό.
            2. Βρες xG από τα προηγούμενα ματς του Μουντιάλ 2026.
            3. Δώσε πιθανό σκορ και κάρτες.
            Απάντησε στα Ελληνικά.
            """
            try:
                res = get_ai_prediction(prompt)
                st.markdown(res)
            except Exception as e:
                st.error(f"Σφάλμα Quota: {e}. Περιμένετε 60 δευτερόλεπτα.")
