importpx solid #ffffff !important; text-transform: uppercase; }
    .match-card { background: # streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os0f172a; border: 1px solid #1e293b; border-radius
import json
from datetime import datetime, timedelta
from supabase import create_client, Client

# --- ΣΥ: 16px; padding: 12px; margin-bottom: 10px; }
ΝΔΕΣΗ ΜΕ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (SUPABASE) ---
try    .group-tag { background: rgba(6, 182, 212, 0:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE.2); color: #22d3ee !important; padding: 2px 10px;_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
 border-radius: 99px; font-size: 10px; font-weight: bold;    st.error("🚨 Σφάλμα Secrets: Ελέγξτε τα SUPABASE_URL και SUPABASE_ }
    button[data-testid="stBaseButton-primary"] { background-color: #ef44KEY στα Settings.")

def load_from_db():
    try:
        response = supabase.table("44 !important; color: white !important; border: none !important; font-weight: 80tournament_persistence").select("data").eq("id", 1).execute()
        if response.data and0 !important; }
    .score-box { padding: 10px; border-radius:  len(response.data) > 0:
            raw_data = response.data[0]['data']8px; text-align: center; margin: 5px; font-weight: bold; border: 1px solid #1e293b; min-width: 65px; }
    .
            data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
            score-out { background-color: #064e3b; color: #10b98return data
    except:
        pass
    return None

def save_to_db(data):
1 !important; border: 1px solid #10b981; }
    .score-delayed { background-color: #450a0a; color: #ef4444 !important    try:
        supabase.table("tournament_persistence").upsert({"id": 1, "data": data}).execute()
    except Exception as e:
        st.error(f"Σφάλμα αποθήκευσης: {; border: 1px solid #ef4444; opacity: 0.6; }
    .turnaround-card { background: #1e293b; padding: 10px; bordere}")

# --- 1. CONFIG & CSS (COSMIC THEME) ---
st.set_page_-radius: 8px; margin-bottom: 5px; border-left: 4px solid #config(page_title="World Cup 2026 Pro Stats", layout="wide", page_icon="06b6d4; }
    </style>
    """, unsafe_allow_html=True)🏆")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS_MAP =: white !important; font-family: 'Inter', sans-serif; }
    [data-testid=" {
    "1": {"n": "Mexico", "img": "https://flagcdn.com/wstHeader"] { background: rgba(0,0,0,0); }
    h1, h280/mx.png", "g": "A"}, "2": {"n": "South Africa", ", h3, h4, h5, h6, label, span, p, .stMarkdown, [img": "https://flagcdn.com/w80/za.png", "g": "A"},
    "3": {"n": "South Korea", "img": "https://flagcdn.com/wdata-testid="stTable"] { color: white !important; }
    .stat-card { background: #0f172a; border: 1px solid #1e293b; border-radius80/kr.png", "g": "A"}, "4": {"n": "Czechia", "img": "https://flagcdn.com/w80/cz.png", "g": "A"},: 12px; padding: 15px; text-align: center; box-shadow: 
    "5": {"n": "Canada", "img": "https://flagcdn.com/w80 4px 6px rgba(0, 0, 0, 0.3); }
0/ca.png", "g": "B"}, "6": {"n": "Bosnia", "img    .stat-val { font-size: 22px; font-weight: 800;": "https://flagcdn.com/w80/ba.png", "g": "B"},
 color: #06b6d4 !important; }
    .stat-label { font-size:    "7": {"n": "Qatar", "img": "https://flagcdn.com/w80 9px; color: #94a3b8 !important; text-transform: uppercase; }
    div[data-testid="/qa.png", "g": "B"}, "8": {"n": "Switzerland", "img": "https://flagcdn.com/w80/ch.png", "g": "B"},
    "stTable"] { background-color: #0f172a; border-radius: 10px9": {"n": "Brazil", "img": "https://flagcdn.com/w80/br; border: 1px solid #1e293b; padding: 5px; }
    .png", "g": "C"}, "10": {"n": "Morocco", "img": "div[data-testid="stTable"] table { color: white !important; width: 100%https://flagcdn.com/w80/ma.png", "g": "C"},
    " !important; font-size: 12px !important; }
    button[data-testid="st11": {"n": "Haiti", "img": "https://flagcdn.com/w80BaseButton-secondary"] { color: black !important; background-color: #f1f5f9 !/ht.png", "g": "C"}, "12": {"n": "Scotland", "img":important; font-weight: 800 !important; border: 2px solid #ffffff !important; "https://flagcdn.com/w80/gb-sct.png", "g": "C text-transform: uppercase; }
    .match-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding"},
    "13": {"n": "USA", "img": "https://flagcdn.com/w80/us.png", "g": "D"}, "14": {"n": "Paragu: 12px; margin-bottom: 10px; }
    .group-tag { background: rgba(6, 1ay", "img": "https://flagcdn.com/w80/py.png", "g": "D"},
    "15": {"n": "Australia", "img": "https://flagcdn.com/w80/au.png", "g": "D"}, "16": {"n": "82, 212, 0.2); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: Turkey", "img": "https://flagcdn.com/w80/tr.png", "g":10px; font-weight: bold; }
    button[data-testid="stBaseButton-primary "D"},
    "17": {"n": "Germany", "img": "https://flagcdn."] { background-color: #ef4444 !important; color: white !important; border: nonecom/w80/de.png", "g": "E"}, "18": {"n": " !important; font-weight: 800 !important; }
    .score-box { padding:Curacao", "img": "https://flagcdn.com/w80/cw.png", "g 10px; border-radius: 8px; text-align: center; margin: 5px": "E"},
    "19": {"n": "Ivory Coast", "img": "https://; font-weight: bold; border: 1px solid #1e293b; min-widthflagcdn.com/w80/ci.png", "g": "E"}, "20": {": 65px; }
    .score-out { background-color: #064e3n": "Ecuador", "img": "https://flagcdn.com/w80/ec.png", "g": "E"},
    "21": {"n": "Netherlands", "img": "https://flagcdn.com/w80/nl.png", "g": "F"}, "22": {"n": "Japan", "img": "https://flagcdn.com/w80/jp.pngb; color: #10b981 !important; border: 1px solid #10b981; }
    .score-delayed { background-color: #450a0a; color: #ef4444 !important; border: 1px solid #ef4444;", "g": "F"},
    "23": {"n": "Sweden", "img": "https opacity: 0.6; }
    .turnaround-card { background: #1e293://flagcdn.com/w80/se.png", "g": "F"}, "24":b; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 4 {"n": "Tunisia", "img": "https://flagcdn.com/w80/tn.px solid #06b6d4; }
    </style>
    """, unsafe_allow_htmlpng", "g": "F"},
    "25": {"n": "Belgium", "img": "=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMShttps://flagcdn.com/w80/be.png", "g": "G"}, "26": {"n": "Egypt", "img": "https://flagcdn.com/w80/eg._MAP = {
    "1": {"n": "Mexico", "img": "https://flagcdn.png", "g": "G"},
    "27": {"n": "Iran", "img": "com/w80/mx.png", "g": "A"}, "2": {"n": "South Africa", "img": "https://flagcdn.com/w80/za.png", "g":https://flagcdn.com/w80/ir.png", "g": "G"}, "28 "A"},
    "3": {"n": "South Korea", "img": "https://flagcdn.": {"n": "New Zealand", "img": "https://flagcdn.com/w80/nz.png", "g": "G"},
    "29": {"n": "Spain", "img":com/w80/kr.png", "g": "A"}, "4": {"n": "Czech "https://flagcdn.com/w80/es.png", "g": "H"}, "3ia", "img": "https://flagcdn.com/w80/cz.png", "g":0": {"n": "Cape Verde", "img": "https://flagcdn.com/w80/ "A"},
    "5": {"n": "Canada", "img": "https://flagcdn.comcv.png", "g": "H"},
    "31": {"n": "Saudi Arabia", "/w80/ca.png", "g": "B"}, "6": {"n": "Bosniaimg": "https://flagcdn.com/w80/sa.png", "g": "H"},", "img": "https://flagcdn.com/w80/ba.png", "g": " "32": {"n": "Uruguay", "img": "https://flagcdn.com/wB"},
    "7": {"n": "Qatar", "img": "https://flagcdn.com/80/uy.png", "g": "H"},
    "33": {"n": "Francew80/qa.png", "g": "B"}, "8": {"n": "Switzerland", "", "img": "https://flagcdn.com/w80/fr.png", "g": "img": "https://flagcdn.com/w80/ch.png", "g": "B"},I"}, "34": {"n": "Senegal", "img": "https://flagcdn.com/
    "9": {"n": "Brazil", "img": "https://flagcdn.com/w8w80/sn.png", "g": "I"},
    "35": {"n": "Iraq", "img": "https://flagcdn.com/w80/iq.png", "g":0/br.png", "g": "C"}, "10": {"n": "Morocco", " "I"}, "36": {"n": "Norway", "img": "https://flagcdn.com/img": "https://flagcdn.com/w80/ma.png", "g": "C"},w80/no.png", "g": "I"},
    "37": {"n": "
    "11": {"n": "Haiti", "img": "https://flagcdn.com/Argentina", "img": "https://flagcdn.com/w80/ar.png", "g":w80/ht.png", "g": "C"}, "12": {"n": "Scotland", "J"}, "38": {"n": "Algeria", "img": "https://flagcdn.com "img": "https://flagcdn.com/w80/gb-sct.png", "g/w80/dz.png", "g": "J"},
    "39": {"n":": "C"},
    "13": {"n": "USA", "img": "https://flagcdn "Austria", "img": "https://flagcdn.com/w80/at.png", "g.com/w80/us.png", "g": "D"}, "14": {"n":": "J"}, "40": {"n": "Jordan", "img": "https://flagcdn.com "Paraguay", "img": "https://flagcdn.com/w80/py.png",/w80/jo.png", "g": "J"},
    "41": {"n": "g": "D"},
    "15": {"n": "Australia", "img": "https:// "Portugal", "img": "https://flagcdn.com/w80/pt.png", "g": "K"}, "42": {"n": "DR Congo", "img": "https://flagcdn.com/w80/cd.png", "g": "K"},
    "43": {"nflagcdn.com/w80/au.png", "g": "D"}, "16": {"n": "Turkey", "img": "https://flagcdn.com/w80/tr.png",": "Uzbekistan", "img": "https://flagcdn.com/w80/uz.png", "g": "K"}, "44": {"n": "Colombia", "img": "https://flagcdn.com/w80/co.png", "g": "K"},
    "45": "g": "D"},
    "17": {"n": "Germany", "img": "https:// {"n": "England", "img": "https://flagcdn.com/w80/gb-engflagcdn.com/w80/de.png", "g": "E"}, "18": {"n": "Curacao", "img": "https://flagcdn.com/w80/cw.png", "g": "E"},
    "19": {"n": "Ivory Coast", "img":.png", "g": "L"}, "46": {"n": "Croatia", "img": " "https://flagcdn.com/w80/ci.png", "g": "E"}, "2https://flagcdn.com/w80/hr.png", "g": "L"},
    "0": {"n": "Ecuador", "img": "https://flagcdn.com/w80/47": {"n": "Ghana", "img": "https://flagcdn.com/w80/ec.png", "g": "E"},
    "21": {"n": "Netherlands", "imggh.png", "g": "L"}, "48": {"n": "Panama", "img":": "https://flagcdn.com/w80/nl.png", "g": "F"}, " "https://flagcdn.com/w80/pa.png", "g": "L"}
}22": {"n": "Japan", "img": "https://flagcdn.com/w80/

RAW_MATCHES = [
    ["A", "11/06 22:00jp.png", "g": "F"},
    "23": {"n": "Sweden", "img", "Estadio Azteca", "1", "2"], ["A", "12/06 05:00", "Estadio Akron", "3", "4"],
    ["B", "12": "https://flagcdn.com/w80/se.png", "g": "F"}, "/06 22:00", "BMO Field", "5", "6"], ["D",24": {"n": "Tunisia", "img": "https://flagcdn.com/w80/tn.png", "g "13/06 04:00", "SoFi Stadium", "13", "1": "F"},
    "25": {"n": "Belgium", "img": "https://flagcdn4"],
    ["D", "14/06 07:00", "BC Place",.com/w80/be.png", "g": "G"}, "26": {"n": "15", "16"], ["B", "13/06 22:00", "Egypt", "img": "https://flagcdn.com/w80/eg.png", "g "Levi's Stadium", "7", "8"],
    ["C", "14/06 ": "G"},
    "27": {"n": "Iran", "img": "https://flagcdn01:00", "MetLife Stadium", "9", "10"], ["C", "14.com/w80/ir.png", "g": "G"}, "28": {"n":/06 04:00", "Gillette Stadium", "11", "12"],
 "New Zealand", "img": "https://flagcdn.com/w80/nz.png", "    ["E", "14/06 20:00", "NRG Stadium", "1g": "G"},
    "29": {"n": "Spain", "img": "https://flag7", "18"], ["F", "14/06 23:00", "ATcdn.com/w80/es.png", "g": "H"}, "30": {"n&T Stadium", "21", "22"],
    ["E", "15/06 ": "Cape Verde", "img": "https://flagcdn.com/w80/cv.png",02:00", "Lincoln Field", "19", "20"], ["F", "15 "g": "H"},
    "31": {"n": "Saudi Arabia", "img": "https/06 05:00", "Estadio BBVA", "23", "24"],://flagcdn.com/w80/sa.png", "g": "H"}, "32":
    ["H", "15/06 19:00", "Mercedes-Benz", " {"n": "Uruguay", "img": "https://flagcdn.com/w80/uy29", "30"], ["G", "15/06 22:00", ".png", "g": "H"},
    "33": {"n": "France", "img":Lumen Field", "25", "26"],
    ["H", "16/06  "https://flagcdn.com/w80/fr.png", "g": "I"}, "301:00", "Hard Rock", "31", "32"], ["G", "164": {"n": "Senegal", "img": "https://flagcdn.com/w80//06 04:00", "SoFi Stadium", "27", "28"],
sn.png", "g": "I"},
    "35": {"n": "Iraq", "img    ["J", "17/06 07:00", "Levi's Stadium", "": "https://flagcdn.com/w80/iq.png", "g": "I"}, "39", "40"], ["I", "16/06 10:00", "MetLife", "33", "34"],
    ["I", "17/06 036": {"n": "Norway", "img": "https://flagcdn.com/w80/1:00", "Gillette", "35", "36"], ["J", "17/no.png", "g": "I"},
    "37": {"n": "Argentina", "img06 04:00", "Arrowhead", "37", "38"],
    ["": "https://flagcdn.com/w80/ar.png", "g": "J"}, "K", "17/06 08:00", "NRG Stadium", "41",38": {"n": "Algeria", "img": "https://flagcdn.com/w80 "42"], ["L", "17/06 11:00", "AT&T/dz.png", "g": "J"},
    "39": {"n": "Austria", " Stadium", "45", "46"],
    ["L", "18/06 02img": "https://flagcdn.com/w80/at.png", "g": "J"},:00", "BMO Field", "47", "48"], ["K", "18/ "40": {"n": "Jordan", "img": "https://flagcdn.com/w8006 05:00", "Estadio Azteca", "43", "44"],
/jo.png", "g": "J"},
    "41": {"n": "Portugal", "    ["A", "18/06 07:00", "Mercedes-Benz", "4img": "https://flagcdn.com/w80/pt.png", "g": "K"},", "2"], ["B", "18/06 10:00", "SoFi Stadium "42": {"n": "DR Congo", "img": "https://flagcdn.com/w8", "8", "6"],
    ["B", "19/06 01:000/cd.png", "g": "K"},
    "43": {"n": "Uzbek", "BC Place", "5", "7"], ["A", "19/06 04:istan", "img": "https://flagcdn.com/w80/uz.png", "g":00", "Estadio Akron", "1", "3"],
    ["D", "20/0 "K"}, "44": {"n": "Colombia", "img": "https://flagcdn.com/6 06:00", "Levi's Stadium", "16", "14"], ["Dw80/co.png", "g": "K"},
    "45": {"n": "", "19/06 10:00", "Lumen Field", "13", "England", "img": "https://flagcdn.com/w80/gb-eng.png", "15"],
    ["C", "20/06 01:00", "Gilletteg": "L"}, "46": {"n": "Croatia", "img": "https://flagcdn", "12", "10"], ["C", "20/06 03:30.com/w80/hr.png", "g": "L"},
    "47": {"", "Lincoln Field", "9", "11"],
    ["F", "21/06 n": "Ghana", "img": "https://flagcdn.com/w80/gh.png",07:00", "Estadio BBVA", "24", "22"], ["F", " "g": "L"}, "48": {"n": "Panama", "img": "https://flag20/06 08:00", "NRG Stadium", "21", "23cdn.com/w80/pa.png", "g": "L"}
}

RAW_MATCH"],
    ["E", "20/06 11:00", "BMO Field",ES = [
    ["A", "11/06 22:00", "Estadio "17", "19"], ["E", "21/06 03:00", Azteca", "1", "2"], ["A", "12/06 05:00 "Arrowhead", "20", "18"],
    ["H", "21/06 ", "Estadio Akron", "3", "4"],
    ["B", "12/06 07:00", "Mercedes-Benz", "29", "31"], ["G", "222:00", "BMO Field", "5", "6"], ["D", "13/1/06 10:00", "SoFi Stadium", "25", "27"],06 04:00", "SoFi Stadium", "13", "14"],
    
    ["H", "22/06 01:00", "Hard Rock", "3["D", "14/06 07:00", "BC Place", "15",2", "30"], ["G", "22/06 04:00", "BC "16"], ["B", "13/06 22:00", "Levi's Place", "28", "26"],
    ["J", "22/06 08 Stadium", "7", "8"],
    ["C", "14/06 01:0:00", "AT&T Stadium", "37", "39"], ["I", "23/06 12:0", "MetLife Stadium", "9", "10"], ["C", "14/06 00", "Lincoln Field", "33", "35"],
    ["I", "23/04:00", "Gillette Stadium", "11", "12"],
    ["E",06 03:00", "MetLife", "36", "34"], ["J", "14/06 20:00", "NRG Stadium", "17", "1 "23/06 06:00", "Levi's Stadium", "40", "8"], ["F", "14/06 23:00", "AT&T Stadium",38"],
    ["K", "23/06 08:00", "NRG "21", "22"],
    ["E", "15/06 02:00", "Lincoln Field", " Stadium", "41", "43"], ["L", "23/06 11:00", "Gillette", "45", "47"],
    ["L", "24/019", "20"], ["F", "15/06 05:00", "Estadio BBVA", "23", "24"],
    ["H", "15/066 02:00", "BMO Field", "48", "46"], ["K", "24/06 05:00", "Estadio Akron", "44", "4 19:00", "Mercedes-Benz", "29", "30"], ["G", "2"],
    ["B", "24/06 10:00", "BC Place",15/06 22:00", "Lumen Field", "25", "26"],
    ["H", "16/06 01:00", "Hard Rock", " "8", "5"], ["B", "24/06 10:00", "L31", "32"], ["G", "16/06 04:00", "umen Field", "6", "7"],
    ["C", "25/06 01:SoFi Stadium", "27", "28"],
    ["J", "17/06 00", "Hard Rock Stadium", "12", "9"], ["C", "25/06 01:00", "Mercedes-Benz", "10", "11"],
    ["A07:00", "Levi's Stadium", "39", "40"], ["I", "", "25/06 04:00", "Estadio Azteca", "4", "16/06 10:00", "MetLife", "33", "34"],1"], ["A", "25/06 04:00", "Estadio BBVA",
    ["I", "17/06 01:00", "Gillette", "3 "2", "3"],
    ["E", "25/06 11:00",5", "36"], ["J", "17/06 04:00", "Arrow "MetLife", "20", "17"], ["E", "25/06 11head", "37", "38"],
    ["K", "17/06 08:00", "Lincoln Field", "18", "19"],
    ["F", "26:00", "NRG Stadium", "41", "42"], ["L", "17//06 02:00", "AT&T Stadium", "22", "23"],06 11:00", "AT&T Stadium", "45", "46"],
 ["F", "26/06 02:00", "Arrowhead", "24",    ["L", "18/06 02:00", "BMO Field", "4 "21"],
    ["D", "26/06 05:00", "So7", "48"], ["K", "18/06 05:00", "EstFi Stadium", "16", "13"], ["D", "26/06 05:adio Azteca", "43", "44"],
    ["A", "18/06 00", "Levi's Stadium", "14", "15"],
    ["I", "26/06 10:00", "Gillette", "36", "33"], ["07:00", "Mercedes-Benz", "4", "2"], ["B", "18/06 10:00", "SoFi Stadium", "8", "6"],
    ["BI", "26/06 10:00", "BMO Field", "34",", "19/06 01:00", "BC Place", "5", "7"], "35"],
    ["H", "27/06 03:00", "Est ["A", "19/06 04:00", "Estadio Akron", "1",adio Akron", "32", "29"], ["H", "27/06 03: "3"],
    ["D", "20/06 06:00", "Levi'00", "NRG Stadium", "30", "31"],
    ["G", "27s Stadium", "16", "14"], ["D", "19/06 10:/06 06:00", "Lumen Field", "26", "27"], ["00", "Lumen Field", "13", "15"],
    ["C", "20G", "27/06 06:00", "BC Place", "28", "/06 01:00", "Gillette", "12", "10"], ["C25"],
    ["L", "28/06 12:00", "MetLife", "20/06 03:30", "Lincoln Field", "9", "11", "48", "45"], ["L", "28/06 12:00"],
    ["F", "21/06 07:00", "Estadio BBVA", "Lincoln Field", "46", "47"],
    ["K", "28/06", "24", "22"], ["F", "20/06 08:00 02:30", "Hard Rock Stadium", "44", "41"], ["K", "", "NRG Stadium", "21", "23"],
    ["E", "20/028/06 02:30", "Mercedes-Benz", "42", "436 11:00", "BMO Field", "17", "19"], ["E","],
    ["J", "28/06 05:00", "Arrowhead", " "21/06 03:00", "Arrowhead", "20", "1838", "39"], ["J", "28/06 05:00", ""],
    ["H", "21/06 07:00", "Mercedes-Benz",AT&T Stadium", "40", "37"]
]

# --- 4. SESSION STATE --- "29", "31"], ["G", "21/06 10:00",
def init_session():
    data = load_from_db()
    if data and len(data "SoFi Stadium", "25", "27"],
    ["H", "22/06) > 0:
        st.session_state.wc_matches = data
    else:
         01:00", "Hard Rock", "32", "30"], ["G", "2matches = []
        for i, m_data in enumerate(RAW_MATCHES):
            matches.append2/06 04:00", "BC Place", "28", "26"],
({
                "id": i+1, "group": m_data[0], "dt": m_    ["J", "22/06 08:00", "AT&T Stadium", "data[1], "st": m_data[2],
                "h_id": m_data[3], "a_id": m_data[4], "sh": None, "sa": None, "37", "39"], ["I", "23/06 12:00", "Lincoln Field", "33",fin": False,
                "y_h": 0, "y_a": 0, "r "35"],
    ["I", "23/06 03:00", "Met_h": 0, "r_a": 0, "p_h": 0, "pLife", "36", "34"], ["J", "23/06 06:0_a": 0, "og_h": 0, "og_a": 0,
                0", "Levi's Stadium", "40", "38"],
    ["K", "23"ref": "TBD", "turn": "Καμία", "htft": "TBD"
            })
        st.session_/06 08:00", "NRG Stadium", "41", "43"], ["L", "23/06 11:00", "Gillette", "45", "47"],
    ["state.wc_matches = matches

if 'wc_matches' not in st.session_state:
    init_session()

#L", "24/06 02:00", "BMO Field", "48", --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_state.wc "46"], ["K", "24/06 05:00", "Estadio Akron_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.", "44", "42"],
    ["B", "24/06 10:randint(0, 5), random.randint(0, 5)
            m['y_h'],00", "BC Place", "8", "5"], ["B", "24/06 1 m['y_a'] = random.randint(0, 3), random.randint(0, 30:00", "Lumen Field", "6", "7"],
    ["C", "25)
            m['r_h'] = random.randint(0, 1) if random.random() >/06 01:00", "Hard Rock Stadium", "12", "9"], ["C 0.92 else 0
            m['r_a'] = random.randint(0, 1) if random.", "25/06 01:00", "Mercedes-Benz", "10", "random() > 0.92 else 0
            if m['sh'] > m['sa'] and11"],
    ["A", "25/06 04:00", "Estadio random.random() > 0.85: m['turn'] = "Home SCORE First and LOSE" Azteca", "4", "1"], ["A", "25/06 04:00
            elif m['sa'] > m['sh'] and random.random() > 0.85:", "Estadio BBVA", "2", "3"],
    ["E", "25/06 m['turn'] = "Away SCORE First and LOSE"
            res = "X"
            if m 11:00", "MetLife", "20", "17"], ["E", "2['sh'] > m['sa']: res = "1"
            elif m['sa'] > m['sh5/06 11:00", "Lincoln Field", "18", "19"],
']: res = "2"
            m['htft'] = f"{random.choice(['1','X','    ["F", "26/06 02:00", "AT&T Stadium", "2'])}/{res}"
            m['fin'] = True
    save_to_db(st.22", "23"], ["F", "26/06 02:00", "Arrowhead", "24", "21"],
    ["D", "26/06 0session_state.wc_matches)
    st.rerun()

def reset():
    save_to_db([])
    st5:00", "SoFi Stadium", "16", "13"], ["D", "26.session_state.clear()
    st.cache_data.clear()
    st.rerun()/06 05:00", "Levi's Stadium", "14", "15"],

@st.cache_data(ttl=3600)
def get_ai_prediction(prompt
    ["I", "26/06 10:00", "Gillette", "3):
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_6", "33"], ["I", "26/06 10:00", "BMO Field", "34", "35"],
    ["H", "27/06 03:00", "Estkey)
    # Διορθωμένο μοντέλο για αποφυγή 404
    model = genai.GenerativeModeladio Akron", "32", "29"], ["H", "27/06 03:('gemini-1.5-flash')
    return model.generate_content(prompt).text

# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 202600", "NRG Stadium", "30", "31"],
    ["G", "27/06 06: PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m00", "Lumen Field", "26", "27"], ["G", "27/06 06:00", "BC Place", "28", "25"],
    ["L in st.session_state.wc_matches if m.get('fin')]
total_y = sum(m.get('y_", "28/06 12:00", "MetLife", "48", "4h',0) + m.get('y_a',0) for m in fin_m)
total5"], ["L", "28/06 12:00", "Lincoln Field", "4_r = sum(m.get('r_h',0) + m.get('r_a',6", "47"],
    ["K", "28/06 02:30",0) for m in fin_m)
total_p = sum(m.get('p_h', "Hard Rock Stadium", "44", "41"], ["K", "28/06 00) + m.get('p_a',0) for m in fin_m)
total_og2:30", "Mercedes-Benz", "42", "43"],
    ["J", " = sum(m.get('og_h',0) + m.get('og_a',0) for m in fin_m)

c1, c2, c3, c4, c5, c28/06 05:00", "Arrowhead", "38", "39"], ["J", "28/06 05:00", "AT&T Stadium", "46 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div><div class="stat0", "37"]
]

# --- 4. SESSION STATE ---
def init_session():
    db-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(_data = load_from_db()
    if db_data:
        st.session_state.wc_matches = db_data
    else:
        matches = []
        for i, m_dataf'<div class="stat-card"><div class="stat-val">{sum(m.get("sh",0)+m. in enumerate(RAW_MATCHES):
            matches.append({
                "id": i+1, "get("sa",0) for m in fin_m)}</div><div class="stat-label">⚽Goalsgroup": m_data[0], "dt": m_data[1], "st": m_data[</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15!important">{total2],
                "h_id": m_data[3], "a_id": m_data[4], "sh": None,_y}</div><div class="stat-label">🟨Yellow</div></div>', unsafe_allow_ "sa": None, "fin": False,
                "y_h": 0, "y_ahtml=True)
with c4: st.markdown(f'<div class="stat-card"><div class": 0, "r_h": 0, "r_a": 0, "p_h="stat-val" style="color:#ef4444!important">{total_r}</div><div": 0, "p_a": 0, "og_h": 0, "og_a class="stat-label">🟥Red</div></div>', unsafe_allow_html=True)
with c5:": 0,
                "ref": "TBD", "turn": "Καμία", "htft": "TBD"
 st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee!important">{total_p}</div><div class="stat-label">🎯Pens</div>            })
        st.session_state.wc_matches = matches

if 'wc_matches' not in st.session_state:</div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="
    init_session()

# --- 5. FUNCTIONS ---
def auto_play():
    for mstat-card"><div class="stat-val" style="color:#fb923c!important">{total in st.session_state.wc_matches:
        if not m['fin']:
            m['sh_og}</div><div class="stat-label">⚠️OG</div></div>', unsafe_allow_html=True'], m['sa'] = random.randint(0, 5), random.randint(0, 5)
            m['y_h'], m['y_a'] = random.randint(0, 3),)

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button random.randint(0, 3)
            m['r_h'] = random.randint(0, ("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ (SIMULATOR)", on_1) if random.random() > 0.9 else 0
            m['r_a'] =click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL TOURN random.randint(0, 1) if random.random() > 0.9 else 0
            AMENT", on_click=reset, type="secondary")

tabs = st.tabs(["📅 ΗΜΕΡΟif m['sh'] > m['sa'] and random.random() > 0.85: m['ΛΟΓΙΟ", "📊 ΒΑΘΜΟΛΟΓΙΕΣ", "📈 ΠΟΡturn'] = "Home SCORE First and LOSE"
            elif m['sa'] > m['sh'] andΕΙΑ ΟΜΑΔΩΝ", "📊 ΑΝΑΛΥΣΗ ΣΚΟΡ", "🔄 ΑΝΑ random.random() > 0.85: m['turn'] = "Away SCORE First and LOSE"ΤΡΟΠΕΣ", "🌓 ΗΜΙΧΡΟΝΑ / ΤΕΛΙΚΑ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

with tabs[0]: # ΗΜΕΡΟΛΟΓΙΟ

            res = "X"; 
            if m['sh'] > m['sa']: res = "1"
            elif m['sa    cols = st.columns(3)
    for idx, m in enumerate(st.session_state.'] > m['sh']: res = "2"
            m['htft'] = f"{random.choicewc_matches):
        h = TEAMS_MAP.get(m['h_id'], {"n":(['1','X','2'])}/{res}"
            m['fin'] = True
    save_to "N/A", "img": ""})
        a = TEAMS_MAP.get(m['a_db(st.session_state.wc_matches); st.rerun()

def reset_all__id'], {"n": "N/A", "img": ""})
        with cols[idx % tournament():
    save_to_db([]); st.session_state.clear(); st.cache_data.3]:
            st.markdown(f"""<div class="match-card">
                <div style="display:flexclear(); st.rerun()

@st.cache_data(ttl=3600)
def; justify-content: space-between; margin-bottom:5px;">
                    <span class="group- get_ai_prediction(prompt):
    genai.configure(api_key=st.secrets["GEMINI_APItag">GROUP {m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align-items:center;">
                    <div style="_KEY"])
    # Χρήση του μοντέλου χωρίς το πρόθεμα models/ για σταθερότητα
    model = gentext-align:center; width:40%; font-weight:bold;"><img src="{h['img']ai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content(prompt).text

# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL}" width="25"><br>{h['n']}</div>
                    <div style="font-size:20px; color:#06b6d4; font-weight:800;">{m.get 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m('sh','-') if m.get('sh') is not None else '-'} : {m.get(' = [m for m in st.session_state.wc_matches if m.get('fin')]
totalsa','-') if m.get('sa') is not None else '-'}</div>
                    <div style="_y = sum(m.get('y_h',0) + m.get('y_a',text-align:center; width:40%;"><img src="{a['img']}" width="250) for m in fin_m)
total_r = sum(m.get('r_h',"><br>{a['n']}</div>
                </div>
                <div style="font-size:9px;0) + m.get('r_a',0) for m in fin_m)
total_p color:#94a3b8; text-align:center; border-top: 1px solid # = sum(m.get('p_h',0) + m.get('p_a',0)1e293b; padding-top:4px;">
                    🟨 {m.get for m in fin_m)
total_og = sum(m.get('og_h',0)('y_h',0)}:{m.get('y_a',0)} | 🟥 {m. + m.get('og_a',0) for m in fin_m)

c1, c2get('r_h',0)}:{m.get('r_a',0)} | 🎯 {m, c3, c4, c5, c6 = st.columns(6)
with c1:.get('p_h',0)}:{m.get('p_a',0)} | ⚠️ { st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m.get('og_h',0)}:{m.get('og_a',0)}
                </div>m)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2
                <div style="font-size:9px; color:#94a3b8; text-: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(malign:center; padding-top:2px;">
                    🏁 Ref: {m.get('ref','T.get("sh",0)+m.get("sa",0) for m in fin_m)}</div><BD')} | 📍 {m.get('st','TBD')} | 🔄 {m.get('turndiv class="stat-label">⚽Goals</div></div>', unsafe_allow_html=True)
with c3','Καμία')} | 🌓 {m.get('htft','TBD')}
                </div>
            </div>: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color""", unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columns(2)
                sh_v = ch.number_input(f"Goals {h[':#facc15!important">{total_y}</div><div class="stat-label">🟨Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<n']}", 0, 15, m.get('sh',0) if m.get('shdiv class="stat-card"><div class="stat-val" style="color:#ef4444!') is not None else 0, key=f"sh{m['id']}")
                sa_v =important">{total_r}</div><div class="stat-label">🟥Red</div></div>', unsafe_allow_ ca.number_input(f"Goals {a['n']}", 0, 15, m.html=True)
with c5: st.markdown(f'<div class="stat-card"><div classget('sa',0) if m.get('sa') is not None else 0, key=f"="stat-val" style="color:#22d3ee!important">{total_p}</div><divsa{m['id']}")
                yh_v = ch.slider(f"Yellow {h['n']}", 0, 10 class="stat-label">🎯Pens</div></div>', unsafe_allow_html=True)
with c6:, m.get('y_h',0), key=f"yh{m['id']}")
                ya st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#_v = ca.slider(f"Yellow {a['n']}", 0, 10, mfb923c!important">{total_og}</div><div class="stat-label">⚠️OG</div>.get('y_a',0), key=f"ya{m['id']}")
                rh_v</div>', unsafe_allow_html=True)

st.write("")
b1, b2 = st. = ch.number_input(f"Red {h['n']}", 0, 5, m.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔget('r_h',0), key=f"rh{m['id']}")
                ra_v = ca.number_input(f"Red {a['n']}", 0, 5, m.getΙ (SIMULATOR)", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset_all_tournament, type="secondary")('r_a',0), key=f"ra{m['id']}")
                ph_v = ch.number_input(f"Pens {h['n']}", 0, 5, m.get('

tabs = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜp_h',0), key=f"ph{m['id']}")
                pa_v = ca.ΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "📊 ΑΝΑΛnumber_input(f"Pens {a['n']}", 0, 5, m.get('pΥΣΗ ΣΚΟΡ", "🔄 ΑΝΑΤΡΟΠΕΣ", "🌓 ΗΜΙΧΡΟΝΑ / ΤΕ_a',0), key=f"pa{m['id']}")
                oh_v = ch.numberΛΙΚΑ", "🔮 ΠΡΟΒΛΕΨΕΙΣ"])

with tabs[0]: # ΗΜ_input(f"OG {h['n']}", 0, 5, m.get('og_ΕΡΟΛΟΓΙΟ
    cols = st.columns(3)
    for idx, m inh',0), key=f"oh{m['id']}")
                oa_v = ca.number_ enumerate(st.session_state.wc_matches):
        h = TEAMS_MAP.get(minput(f"OG {a['n']}", 0, 5, m.get('og_a['h_id'], {"n": "N/A", "img": ""})
        a = TEAMS',0), key=f"oa{m['id']}")
                ref_v = st.text_input_MAP.get(m['a_id'], {"n": "N/A", "img": ""})("Referee", m.get('ref','TBD'), key=f"ref_in{m['id']}")
        with cols[idx % 3]:
            st.markdown(f"""<div class="match-
                turn_v = st.selectbox("Ανατροπή", ["Καμία", "Home SCORE First andcard">
                <div style="display:flex; justify-content: space-between; margin-bottom: LOSE", "Away SCORE First and LOSE", "1/2", "2/1"], index=05px;">
                    <span class="group-tag">GROUP {m['group']}</span>
                    <span, key=f"turn_{m['id']}")
                htft_v = st.selectbox("Ημί style="font-size:10px; color:#94a3b8;">🕒 {m['dtχρονο/Τελικό", ["TBD", "1/1", "1/X", "1/']}</span>
                </div>
                <div style="display:flex; justify-content: space-around; align2", "X/1", "X/X", "X/2", "2/1", "2-items:center;">
                    <div style="text-align:center; width:40%; font-weight:bold;"><img src="{/X", "2/2"], index=0, key=f"htft_{m['id']}")
                if st.button("Saveh['img']}" width="25"><br>{h['n']}</div>
                    <div style="font Result", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v,-size:20px; color:#06b6d4; font-weight:800;"> "sa": sa_v, "fin": True, "y_h": yh_v, "y_a": ya_v{m.get('sh','-') if m.get('sh') is not None else '-'} : {m.get('sa','-') if m.get('sa') is not None else '-'}</div>
                    <div style="text-, "r_h": rh_v, "r_a": ra_v, "p_h": ph_v, "p_a": pa_v, "og_h": oh_v, "og_a": oa_v, "ref": ref_v, "turn": turn_v, "htft": htft_v})
                    save_to_db(align:center; width:40%;"><img src="{a['img']}" width="25"><br>{a['n']}</div>
                </div>
                <div style="font-size:9px; color:#st.session_state.wc_matches); st.rerun()

with tabs[1]: # ΒΑ94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:4px;">
                    🟨 {m.get('yΘΜΟΛΟΓΙΕΣ
    cols_s = st.columns(3)
    GROUPS_h',0)}:{m.get('y_a',0)} | 🟥 {m.get('_L = ["A", "B", "C", "D", "E", "F", "G",r_h',0)}:{m.get('r_a',0)} | 🎯 {m.get "H", "I", "J", "K", "L"]
    for i, gId in enumerate('p_h',0)}:{m.get('p_a',0)} | ⚠️ {m.(GROUPS_L):
        with cols_s[i % 3]:
            st.markdown(get('og_h',0)}:{m.get('og_a',0)}
                </div>
                f"#### Group {gId}")
            g_team_ids = [tid for tid, d in TE<div style="font-size:9px; color:#94a3b8; text-align:AMS_MAP.items() if d['g'] == gId]
            res = []
            for tid in g_team_ids:
                team = TEAMS_MAP[tid]
                pts, gd, y, r = 0,center; padding-top:2px;">
                    🏁 Ref: {m.get('ref','TBD')} | 📍 {m.get('st','TBD')} | 🔄 {m.get('turn','Καμία')} | 🌓 { 0, 0, 0
                for m in st.session_state.wc_matches:
                    if m.get('fin') and (m.get('h_id') == tid or m.getm.get('htft','TBD')}
                </div>
            </div>""", unsafe_allow_html=True)
            with st.exp('a_id') == tid):
                        is_h = m.get('h_id') == tidander("✏️ Επεξεργασία"):
                ch, ca = st.columns(2)
                
                        h_s, a_s = (m.get('sh',0), m.get('sa',0)) if is_h else (m.get('sa',0), m.get('sh',0sh_v = ch.number_input(f"Goals {h['n']}", 0, 15, m.get('sh',0) if m.get('sh') is not None else 0, key=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {a['n']}", 0, 15, m.get('sa',0) if m.get('sa') is not None else 0, key=f"sa{m['id']}")
                ))
                        y += m.get('y_h',0) if is_h else m.get('y_a',0)
                        r += m.get('r_h',0) if is_h else m.get('r_a',0)
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_yh_v = ch.slider(f"Yellow {h['n']}", 0, 10, m.get('y_h',0), key=f"yh{m['id']}")
                ya_v = ca.slider(f"Yellow {a['n']}", 0, 10, m.s: pts += 1
                res.append({"Flag": team['img'], "Team": team['n'], "Pts": pts, "GD": gd, "Y": y, "R": r})
            df = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
            get('y_a',0), key=f"ya{m['id']}")
                rh_v = ch.number_input(f"Red {h['n']}", 0, 5, m.getst.data_editor(df, column_config={"Flag": st.column_config.ImageColumn("🏳('r_h',0), key=f"rh{m['id']}")
                ra_v = ca️")}, hide_index=True, key=f"table_{gId}")

with tabs[2]: # ΠΟΡΕΙΑ ΟΜΑΔΩΝ
    all_names = sorted([d['n'] for d.number_input(f"Red {a['n']}", 0, 5, m.get('r_a',0), key=f"ra{m['id']}")
                ph_v = ch. in TEAMS_MAP.values()])
    sel_t = st.selectbox("Επιλέξτε Ομάδα:", all_namesnumber_input(f"Pens {h['n']}", 0, 5, m.get('p_h',0), key=f"ph{m['id']}")
                pa_v = ca.number)
    team_id = next(k for k,v in TEAMS_MAP.items() if v['n'] == sel_t)
    t_matches = [m for m in st.session_state_input(f"Pens {a['n']}", 0, 5, m.get('p_a',0), key=f"pa{m['id']}")
                oh_v = ch.number_input(f"OG {h['n']}", 0, 5, m.get('og_h.wc_matches if (m.get('h_id') == team_id or m.get('a_id') == team_id)]
    t_pts, t_gf, t_ga, t_',0), key=f"oh{m['id']}")
                oa_v = ca.number_input(f"OG {a['n']}", 0, 5, m.get('og_a',0), key=f"oa{m['id']}")
                ref_v = st.text_input("y, t_r = 0, 0, 0, 0, 0
    for m in t_matches:
        if m.get('fin'):
            is_h = m.get('h_id') == team_id
            g, c = (m.get('sh',0), m.get('sa',0)) if is_h else (m.get('sa',0), m.getReferee", m.get('ref','TBD'), key=f"ref_in{m['id']}")
                turn_v = st.selectbox("Ανατροπή", ["Καμία", "Home SCORE First and LO('sh',0))
            t_gf += g; t_ga += c
            t_y += m.get('y_h',0) if is_h else m.get('y_a',0)
            t_r += m.get('rSE", "Away SCORE First and LOSE", "1/2", "2/1"], index=0,_h',0) if is_h else m.get('r_a',0)
            if g > c: t_pts += 3
            elif g == c: t_pts += 1
     key=f"turn_{m['id']}")
                htft_v = st.selectbox("Ημίχρονο/Τελικό", ["TBD", "1/1", "1/X", "1/2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"], index=0, key=f"htft_{m['id']}")
                if st.button("Save Result", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v,c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Points", t_pts); c_s2.metric("Goals", f"{t_gf}-{t_ga}"); c_s3.metric("Cards (Y-R)", f"{t_y}-{t_ "sa": sa_v, "fin": True, "y_h": yh_v, "y_r}")
    cols_team = st.columns(3)
    for idx, m in enumerate(t_matchesa": ya_v, "r_h": rh_v, "r_a": ra_v, "p_h": ph_v, "p_a": pa_v, "og_h": oh_v, "og_):
        with cols_team[idx % 3]:
            res_col = "#10b981" if m.get('fin') else "#1e293b"
            h_n = TEAMS_MAP[m.get('h_id')]['n']; a_n = TEAMS_MAP[m.get('a": oa_v, "ref": ref_v, "turn": turn_v, "htft": htft_v})
                    save_to_db(st.session_state.wc_matches); sta_id')]['n']
            st.markdown(f"""<div class="match-card" style="border-top:4px solid {res_col}">
            <b>Αγώνας {idx+1}</b><br>{h_n} {m.get('sh') if m.get('sh') is.rerun()

with tabs[1]: # ΒΑΘΜΟΛΟΓΙΕΣ
    cols not None else ''} - {m.get('sa') if m.get('sa') is not None else ''} {a_n}
            </div>""", unsafe_allow_html=True)

with tabs[3_s = st.columns(3)
    GROUPS_L = ["A", "B", "C", "D", "E",]: # ΑΝΑΛΥΣΗ ΣΚΟΡ
    st.markdown("### 📊 Πίνα "F", "G", "H", "I", "J", "K", "L"]
    for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:κας Πιθανών Σκορ & Συχνότητας")
    actual_scores = [(m.get('sh'), m.get('sa')) for m in st.session_state.wc_matches if m.
            st.markdown(f"#### Group {gId}")
            g_team_ids = [tid for tid, d in TEAMS_MAP.items() if d['g'] == gId]
            res = []
            for tid in g_team_ids:
                team = TEAMS_MAP[tid]get('fin')]
    grid_size = 6 
    for h_g in range(grid_size):
        cols_score = st.columns(grid_size)
        for a_g in range(grid_size):
            with cols_score[a_g]:
                h_label, a_label = (str(
                pts, gd, y, r = 0, 0, 0, 0
                for m in st.session_h_g) if h_g < 5 else "5+"), (str(a_g) ifstate.wc_matches:
                    if m.get('fin') and (m.get('h_id a_g < 5 else "5+")
                def check(sh, sa, th, ta):
') == tid or m.get('a_id') == tid):
                        is_h = m.get                    if sh is None or sa is None: return False
                    return ((sh == th) if th < ('h_id') == tid
                        h_s, a_s = (m.get('sh',5 else (sh >= 5)) and ((sa == ta) if ta < 5 else (sa >= 0), m.get('sa',0)) if is_h else (m.get('sa',0), m.get('sh',05))
                count = sum(1 for sh, sa in actual_scores if check(sh, sa,))
                        y += m.get('y_h',0) if is_h else m.get(' h_g, a_g))
                st_class = "score-out" if count > 0y_a',0)
                        r += m.get('r_h',0) if is_h else "score-delayed"
                st.markdown(f"""<div class="score-box {st_ else m.get('r_a',0)
                        gd += (h_s - a_s)class}">{h_label}-{a_label}<br><span style='font-size:9px'>{'
                        if h_s > a_s: pts += 3
                        elif h_s == a_✅' if count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""",s: pts += 1
                res.append({"Flag": team['img'], "Team": team['n unsafe_allow_html=True)

with tabs[4]: # ΑΝΑΤΡΟΠΕΣ
    st'], "Pts": pts, "GD": gd, "Y": y, "R": r})
            df.markdown("### 🔄 Ανάλυση Ανατροπών (Turnarounds)")
    t_fin = [ = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
            m for m in st.session_state.wc_matches if m.get('fin') and m.getst.data_editor(df, column_config={"Flag": st.column_config.ImageColumn("🏳('turn','Καμία') != "Καμία"]
    t_col1, t_col2, t_col3 = st.️")}, hide_index=True, key=f"table_{gId}")

with tabs[2]:columns(3)
    half_turns = [m for m in t_fin if m.get('turn # ΠΟΡΕΙΑ ΟΜΑΔΩΝ
    all_names = sorted([d['n'] for d') in ["Home SCORE First and LOSE", "Away SCORE First and LOSE"]]
    t_col1 in TEAMS_MAP.values()])
    sel_t = st.selectbox("Επιλέξτε Ομάδα:", all_names.metric("Σύνολο Ημιανατροπών", len(half_turns))
    t_)
    team_id = next(k for k,v in TEAMS_MAP.items() if vcol2.metric("Ανατροπή 1/2", len([m for m in t_fin if['n'] == sel_t)
    t_matches = [m for m in st.session_state m.get('turn') == "1/2"]))
    t_col3.metric("Ανατρο.wc_matches if (m.get('h_id') == team_id or m.get('aπή 2/1", len([m for m in t_fin if m.get('turn') == "_id') == team_id)]
    t_pts, t_gf, t_ga, t_2/1"]))
    st.write("---")
    if t_fin:
        for m iny, t_r = 0, 0, 0, 0, 0
    for m t_fin:
            h_n = TEAMS_MAP[m.get('h_id')]['n']; a_n = TE in t_matches:
        if m.get('fin'):
            is_h = m.get('AMS_MAP[m.get('a_id')]['n']
            st.markdown(f"""<h_id') == team_id
            g, c = (m.get('sh',0), mdiv class="turnaround-card"><span style="color:#06b6d4; font-size:.get('sa',0)) if is_h else (m.get('sa',0), m.get12px; font-weight:bold;">{m.get('turn')}</span><br><b>{h_n} {m.get('sh')} - {m.get('sa')} {a_n}</b>('sh',0))
            t_gf += g; t_ga += c
            t_y += m.get('y_h</div>""", unsafe_allow_html=True)
    else: st.info("Δεν έχουν σημειω',0) if is_h else m.get('y_a',0)
            if g > cθεί ανατροπές ακόμα.")

with tabs[5]: # ΗΜΙΧΡΟΝΑ / ΤΕΛΙΚ: t_pts += 3
            elif g == c: t_pts += 1
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Points", t_pts); c_s2.metric("Goals", f"{t_gf}-{t_ga}"); c_s3.metric("Cards (Y)", t_y)
    cols_Α
    st.markdown("### 🌓 Στατιστικά Ημιχρόνων / Τελικών")
    st.write("Εμφάνιση αποτελεσμάτων HT/FT (εξαιρούνται οι πλήρεις ανατροπές 1/2 και 2/1).")
    htft_types = ["1/1", "team = st.columns(3)
    for idx, m in enumerate(t_matches):
        with1/X", "X/1", "X/X", "X/2", "2/X", "2 cols_team[idx % 3]:
            res_col = "#10b981" if m.get('fin') else/2"]
    all_htft = [m.get('htft','TBD') for m in st.session_state.wc_matches if m.get('fin') and m.get('htft',' "#1e293b"
            h_n = TEAMS_MAP[m.get('hTBD') in htft_types]
    cols_htft = st.columns(7)
    _id')]['n']; a_n = TEAMS_MAP[m.get('a_id')]['for idx, t_type in enumerate(htft_types):
        with cols_htft[idx]:n']
            st.markdown(f"""<div class="match-card" style="border-top:
            count = all_htft.count(t_type)
            st_class = "score-4px solid {res_col}">
            <b>Αγώνας {idx+1}</b><br>{out" if count > 0 else "score-delayed"
            st.markdown(f"""<div classh_n} {m.get('sh') if m.get('sh') is not None else ''}="score-box {st_class}">{t_type}<br><span style='font-size:9px'>{'✅' if - {m.get('sa') if m.get('sa') is not None else ''} {a_ count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""", unsafe_allown}
            </div>""", unsafe_allow_html=True)

with tabs[3]: # ΑΝΑΛ_html=True)

with tabs[6]: # ΠΡΟΒΛΕΨΕΙΣ
    st.ΥΣΗ ΣΚΟΡ
    st.markdown("### 📊 Πίνακας Πιθανών Σκορ & Συχνότητας")
    actual_scores = [(m.get('sh'), m.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ (Elite Web Grounding)")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            get('sa')) for m in st.session_state.wc_matches if m.get('fin')]
genai.configure(api_key=api_key)
            working_model = 'gemini-1    grid_size = 6 
    for h_g in range(grid_size):
        cols.5-flash'
            c1, c2 = st.columns(2)
            h_t_score = st.columns(grid_size)
        for a_g in range(grid_size):
            with cols_score[a_g]:
                h_label, a_label = (str( = c1.selectbox("Home Team", all_names, key="ai_h_final")
            a_th_g) if h_g < 5 else "5+"), (str(a_g) if = c2.selectbox("Away Team", all_names, index=1, key="ai_a_final a_g < 5 else "5+")
                def check(sh, sa, th, ta):
")
            match_number = st.number_input("Νούμερο Αγώνα (1-10                    if sh is None or sa is None: return False
                    return ((sh == th) if th < 4):", 1, 104, 1, key="match_no_final")
            5 else (sh >= 5)) and ((sa == ta) if ta < 5 else (sa >= extra_notes = st.text_area("🗒️ Σημειώσεις τελευταίας στιγμής:", placeholder="Π.χ. Βρέχει, λείπει ο αρχηγός...")
            if st.button("ΠΑ5))
                count = sum(1 for sh, sa in actual_scores if check(sh, sa,ΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary", key="btn_final"):
                 h_g, a_g))
                st_class = "score-out" if count > 0 else "score-delayed"
                st.markdown(f"""<div class="score-box {st_with st.spinner("Analyzing..."):
                    # ΤΟ ELITE PROMPT ΣΟΥ (ΔΙΟΡΘΩΜΕΝΑ Αclass}">{h_label}-{a_label}<br><span style='font-size:9px'>{'ΓΚΙΣΤΡΑ ΓΙΑ ΠΙΝΑΚΕΣ)
                    advanced_prompt = f"""
Ε✅' if count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""", unsafe_allow_html=True)

with tabs[4]: # ΑΝΑΤΡΟΠΕΣ
    stίσαι ένας elite football analyst, data scientist και quant modeler με απόλυτη εξειδίκευση στο Παγ.markdown("### 🔄 Ανάλυση Ανατροπών (Turnarounds)")
    t_fin = [κόσμιο Κύπελλο.
Ακολούθησε αυστηρά τη ΜΕΘΟΔΟΛΟΓΙΑ πουm for m in st.session_state.wc_matches if m.get('fin') and m.get περιγράφεται παρακάτω — σκέψου βήμα-βήμα (chain-of-thought('turn','Καμία') != "Καμία"]
    t_col1, t_col2, t_col3) πριν βγάλεις οποιαδήποτε πρόβλεψη. Μεταξύ {h_t} εναντίον {a_t = st.columns(3)
    half_turns = [m for m in t_fin if m.}.
Η ανάλυσή σου ΠΡΕΠΕΙ να βασίζεται σε πραγματικά δεδομένα μέσω web search.
📌get('turn') in ["Home SCORE First and LOSE", "Away SCORE First and LOSE"]]
    t ΔΕΔΟΜΕΝΑ ΑΓΩΝΑ: Αγώνας #{match_number} | {h__col1.metric("Σύνολο Ημιανατροπών", len(half_turns))
    t_col2.metrict} vs {a_t} | Μουντιάλ 2026.
📌 ΣΗΜΕΙΩΣΕΙΣ("Ανατροπή 1/2", len([m for m in t_fin if m.get('turn') == "1/2"]))
    t_col3.metric("Ανατροπή 2/ ΧΡΗΣΤΗ: {extra_notes}

🧠 ΒΗΜΑΤΑ:
1. ΠΕΡΙΒΑ1", len([m for m in t_fin if m.get('turn') == "2/1"]))ΛΛΟΝ: Διαιτητής αγώνα #{match_number} & Καιρός.
2. ΦΟ
    st.write("---")
    if t_fin:
        for m in t_fin:
            h_n = TEΡΜΑ: xG/xGOT από ματς Μουντιάλ 2026 (αν υπάρχουν) αλλιώς τελευταAMS_MAP[m.get('h_id')]['n']; a_n = TEAMS_MAP[ία 10.
3. ΙΣΤΟΡΙΚΟ: Τι έγινε ιστορικά στον αγώm.get('a_id')]['n']
            st.markdown(f"""<div class="turnaround-card"><span style="color:#06b6d4; font-size:12px;να #{match_number} το 2022, 2018 και 2014.

Α font-weight:bold;">{m.get('turn')}</span><br><b>{h_n} {ΠΑΝΤΗΣΗ (Ελληνικά):
## ⚽ {h_t} vs {a_t}
m.get('sh')} - {m.get('sa')} {a_n}</b></div>""", unsafe_### 📋 Ταυτότητα Αγώνα: Διαιτητής & Καιρός
### 🏥 Διαθεσιμότητα & Σημειallow_html=True)
    else: st.info("Δεν έχουν σημειωθεί ανατροπές ακόμα.")

with tabs[5]: # ΗΜΙΧΡΟΝΑ/ΤΕΛΙΚΑ
    stώσεις
### 📊 Data & xG Analysis
### 🏟️ Ιστορικό Μοτίβο Αγώνα #{match_number}
### 🔮 Quantitative Prediction Model
| Κατηγορία | Πρόβλεψη | Πιθαν.markdown("### 🌓 Στατιστικά Ημιχρόνων / Τελικών")
    htftότητα |
|-----------|----------|------------|
| 1-X-2 | ... | XX% |_types = ["1/1", "1/X", "X/1", "X/X", "X/2", "2/X", "2/2"]
    all_htft = [m.get('ht
| Σκορ | X-X | — |
| Πέναλτι | Ναι/Όχι | XX% |
|ft','TBD') for m in st.session_state.wc_matches if m.get('fin') Κόκκινη | Ναι/Όχι | XX% |
| Ανατροπή | Ναι/Όχι | XX% |
 and m.get('htft','TBD') in htft_types]
    cols_htft ="""
                    ans = get_ai_prediction(working_model, advanced_prompt)
                    st.markdown st.columns(7)
    for idx, t_type in enumerate(htft_types):
        ("---"); st.markdown(ans)
        except Exception as e: st.error(f"Error: {e}")
```with cols_htft[idx]:
            count = all_htft.count(t_type)
            st_class = "score-out" if count > 0 else "score-delayed"
            st
