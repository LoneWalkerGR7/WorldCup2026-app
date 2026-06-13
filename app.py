import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG & CSS (COSMIC THEME) ---
st.set_page_config(page_title="World Cup `app.py`. Έκανα ακριβώς την αλλαγή που ζήτησες στις ο 2026 Pro Stats", layout="wide", page_icon="🏆")

st.markdown("""
νομασίες των ανατροπών, διατηρώντας όλα τα υπόλοιπα στοιχεία (Cosmic Slate, Advanced    <style>
    .stApp { background-color: #020617; color: white !important; font-family AI, Στατιστικά) άθικτα.

### Ο Οριστικός Κώδικας (`app.py`): 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba( - Αντικατάστησε τα πάντα στο GitHub

```python
import streamlit as st
import pandas as pd
import0,0,0,0); }
    h1, h2, h3, h4, h5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { random
import google.generativeai as genai
import os
from datetime import datetime, timedelta

# --- 1. CONFIG color: white !important; }
    
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border- & CSS (COSMIC THEME) ---
st.set_page_config(page_title="World Cupradius: 12px;
        padding: 15px;
        text-align: center; 2026 Pro Stats", layout="wide", page_icon="🏆")

st.markdown("""

        box-shadow: 0 4px 6px rgba(0, 0, 0,    <style>
    .stApp { background-color: #020617; color: white !important; font-family 0.3);
    }
    .stat-val { font-size: 22px;: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba( font-weight: 800; color: #06b6d4 !important; }
    0,0,0,0); }
    h1, h2, h3, h4, h.stat-label { font-size: 9px; color: #94a3b8 !important5, h6, label, span, p, .stMarkdown, [data-testid="stTable"] { color: white !important; }
    
    .stat-card {
        background: #0f1; text-transform: uppercase; }

    div[data-testid="stTable"] { background-color:72a;
        border: 1px solid #1e293b;
        border- #0f172a; border-radius: 10px; border: 1px solid #radius: 12px;
        padding: 15px;
        text-align: center;1e293b; padding: 5px; }
    div[data-testid="stTable
        box-shadow: 0 4px 6px rgba(0, 0, 0,"] table { color: white !important; width: 100% !important; font-size:  0.3);
    }
    .stat-val { font-size: 22px;12px !important; }
    
    button[data-testid="stBaseButton-secondary"] {
        color: black !important font-weight: 800; color: #06b6d4 !important; }
    ;
        background-color: #f1f5f9 !important;
        font-weight: .stat-label { font-size: 9px; color: #94a3b8 !important800 !important;
        border: 2px solid #ffffff !important;
        text-transform; text-transform: uppercase; }

    div[data-testid="stTable"] { background-color:: uppercase;
    }

    .match-card {
        background: #0f172a #0f172a; border-radius: 10px; border: 1px solid #;
        border: 1px solid #1e293b;
        border-radius: 1e293b; padding: 5px; }
    div[data-testid="stTable16px;
        padding: 12px;
        margin-bottom: 10px;"] table { color: white !important; width: 100% !important; font-size: 
    }
    .st-venue { font-size: 9px; color: #94a3b8 !important; font-style: italic; margin-top: 5px; }
    .12px !important; }
    
    button[data-testid="stBaseButton-secondary"] {
        color: black !importantgroup-tag { background: rgba(6, 182, 212, 0.2;
        background-color: #f1f5f9 !important;
        font-weight: ); color: #22d3ee !important; padding: 2px 10px; border-800 !important;
        border: 2px solid #ffffff !important;
        text-transform: uppercase;
    }

    .match-card {
        background: #0f172aradius: 99px; font-size: 10px; font-weight: bold; }
;
        border: 1px solid #1e293b;
        border-radius:     
    button[data-testid="stBaseButton-primary"] {
        background-color: #ef4444 !important;16px;
        padding: 12px;
        margin-bottom: 10px;
        color: white !important;
        border: none !important;
        font-weight: 8
    }
    .st-venue { font-size: 9px; color: #94a00 !important;
    }

    .score-box { padding: 10px; border-3b8 !important; font-style: italic; margin-top: 5px; }
    .radius: 8px; text-align: center; margin: 5px; font-weight: bold;group-tag { background: rgba(6, 182, 212, 0.2 border: 1px solid #1e293b; }
    .score-out { background-); color: #22d3ee !important; padding: 2px 10px; border-radius: 99px; font-size: 10px; font-weight: bold; }
color: #064e3b; color: #10b981 !important; border:    
    button[data-testid="stBaseButton-primary"] {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
 1px solid #10b981; }
    .score-delayed { background-color:        font-weight: 800 !important;
    }

    .score-box { padding: #450a0a; color: #ef4444 !important; border: 1px solid #ef4444; opacity: 0.6; }
    
    .turnaround-card {
        background: #1e293b;
        padding: 10px;
 10px; border-radius: 8px; text-align: center; margin: 5px        border-radius: 8px;
        margin-bottom: 5px;
        border-left; font-weight: bold; border: 1px solid #1e293b; }
    : 4px solid #06b6d4;
    }
    </style>
    """,.score-out { background-color: #064e3b; color: #10b9 unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS_81 !important; border: 1px solid #10b981; }
    .scoreMAP = {
    "1": {"n": "Mexico", "img": "https://flagcdn.com-delayed { background-color: #450a0a; color: #ef4444 !important; border: 1px solid #ef4444; opacity: 0.6; }
/w80/mx.png", "g": "A"}, "2": {"n": "South Africa    
    .turnaround-card {
        background: #1e293b;
        padding", "img": "https://flagcdn.com/w80/za.png", "g": ": 10px;
        border-radius: 8px;
        margin-bottom: 5A"},
    "3": {"n": "South Korea", "img": "https://flagcdn.compx;
        border-left: 4px solid #06b6d4;
    }
/w80/kr.png", "g": "A"}, "4": {"n": "Czechia    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔ", "img": "https://flagcdn.com/w80/cz.png", "g": "ΟΜΕΝΑ ΟΜΑΔΩΝ ---
TEAMS_MAP = {
    "1": {"n": "Mexico", "img": "A"},
    "5": {"n": "Canada", "img": "https://flagcdn.com/https://flagcdn.com/w80/mx.png", "g": "A"}, "2":w80/ca.png", "g": "B"}, "6": {"n": "Bosnia", {"n": "South Africa", "img": "https://flagcdn.com/w80/za. "img": "https://flagcdn.com/w80/ba.png", "g": "Bpng", "g": "A"},
    "3": {"n": "South Korea", "img": ""},
    "7": {"n": "Qatar", "img": "https://flagcdn.com/whttps://flagcdn.com/w80/kr.png", "g": "A"}, "4":80/qa.png", "g": "B"}, "8": {"n": "Switzerland", "img {"n": "Czechia", "img": "https://flagcdn.com/w80/cz.": "https://flagcdn.com/w80/ch.png", "g": "B"},
png", "g": "A"},
    "5": {"n": "Canada", "img": "https    "9": {"n": "Brazil", "img": "https://flagcdn.com/w80://flagcdn.com/w80/ca.png", "g": "B"}, "6": {"/br.png", "g": "C"}, "10": {"n": "Morocco", "imgn": "Bosnia", "img": "https://flagcdn.com/w80/ba.png": "https://flagcdn.com/w80/ma.png", "g": "C"},
", "g": "B"},
    "7": {"n": "Qatar", "img": "https://    "11": {"n": "Haiti", "img": "https://flagcdn.com/wflagcdn.com/w80/qa.png", "g": "B"}, "8": {"n80/ht.png", "g": "C"}, "12": {"n": "Scotland", "": "Switzerland", "img": "https://flagcdn.com/w80/ch.png", "img": "https://flagcdn.com/w80/gb-sct.png", "g":g": "B"},
    "9": {"n": "Brazil", "img": "https://flagcdn "C"},
    "13": {"n": "USA", "img": "https://flagcdn..com/w80/br.png", "g": "C"}, "10": {"n":com/w80/us.png", "g": "D"}, "14": {"n": " "Morocco", "img": "https://flagcdn.com/w80/ma.png", "Paraguay", "img": "https://flagcdn.com/w80/py.png", "g": "C"},
    "11": {"n": "Haiti", "img": "https://g": "D"},
    "15": {"n": "Australia", "img": "https://flagflagcdn.com/w80/ht.png", "g": "C"}, "12": {"cdn.com/w80/au.png", "g": "D"}, "16": {"nn": "Scotland", "img": "https://flagcdn.com/w80/gb-sct": "Turkey", "img": "https://flagcdn.com/w80/tr.png", ".png", "g": "C"},
    "13": {"n": "USA", "img": "https://flagcdn.com/w80/us.png", "g": "D"}, "1g": "D"},
    "17": {"n": "Germany", "img": "https://flagcdn.com/w80/de.png", "g": "E"}, "18": {"n4": {"n": "Paraguay", "img": "https://flagcdn.com/w80": "Curacao", "img": "https://flagcdn.com/w80/cw.png", "g": "E"},
    "19": {"n": "Ivory Coast", "img": "/py.png", "g": "D"},
    "15": {"n": "Australia", "img": "https://flagcdn.com/w80/au.png", "g": "D"},https://flagcdn.com/w80/ci.png", "g": "E"}, "20 "16": {"n": "Turkey", "img": "https://flagcdn.com/w80": {"n": "Ecuador", "img": "https://flagcdn.com/w80/ec/tr.png", "g": "D"},
    "17": {"n": "Germany", ".png", "g": "E"},
    "21": {"n": "Netherlands", "img":img": "https://flagcdn.com/w80/de.png", "g": "E"}, "18": {"n": "Curacao", "img": "https://flagcdn.com/w8 "https://flagcdn.com/w80/nl.png", "g": "F"}, "22": {"n": "Japan", "img": "https://flagcdn.com/w80/jp0/cw.png", "g": "E"},
    "19": {"n": "Ivory.png", "g": "F"},
    "23": {"n": "Sweden", "img": Coast", "img": "https://flagcdn.com/w80/ci.png", "g": "https://flagcdn.com/w80/se.png", "g": "F"}, "2 "E"}, "20": {"n": "Ecuador", "img": "https://flagcdn.com4": {"n": "Tunisia", "img": "https://flagcdn.com/w80//w80/ec.png", "g": "E"},
    "21": {"n":tn.png", "g": "F"},
    "25": {"n": "Belgium", "img "Netherlands", "img": "https://flagcdn.com/w80/nl.png", "g": "https://flagcdn.com/w80/be.png", "g": "G"}, "": "F"}, "22": {"n": "Japan", "img": "https://flagcdn.com26": {"n": "Egypt", "img": "https://flagcdn.com/w80//w80/jp.png", "g": "F"},
    "23": {"n": "Sweden", "img": "https://flagcdn.com/w80/se.png", "geg.png", "g": "G"},
    "27": {"n": "Iran", "img": "https://flagcdn.com/w80/ir.png", "g": "G"}, "": "F"}, "24": {"n": "Tunisia", "img": "https://flagcdn.28": {"n": "New Zealand", "img": "https://flagcdn.com/w80com/w80/tn.png", "g": "F"},
    "25": {"n/nz.png", "g": "G"},
    "29": {"n": "Spain", "": "Belgium", "img": "https://flagcdn.com/w80/be.png", "img": "https://flagcdn.com/w80/es.png", "g": "H"},g": "G"}, "26": {"n": "Egypt", "img": "https://flagcdn. "30": {"n": "Cape Verde", "img": "https://flagcdn.com/w8com/w80/eg.png", "g": "G"},
    "27": {"n0/cv.png", "g": "H"},
    "31": {"n": "Saudi Arabia": "Iran", "img": "https://flagcdn.com/w80/ir.png", "", "img": "https://flagcdn.com/w80/sa.png", "g": "g": "G"}, "28": {"n": "New Zealand", "img": "https://flagcdnH"}, "32": {"n": "Uruguay", "img": "https://flagcdn.com.com/w80/nz.png", "g": "G"},
    "29": {"/w80/uy.png", "g": "H"},
    "33": {"n":n": "Spain", "img": "https://flagcdn.com/w80/es.png", "France", "img": "https://flagcdn.com/w80/fr.png", "g "g": "H"}, "30": {"n": "Cape Verde", "img": "https://flag": "I"}, "34": {"n": "Senegal", "img": "https://flagcdn.cdn.com/w80/cv.png", "g": "H"},
    "31":com/w80/sn.png", "g": "I"},
    "35": {"n {"n": "Saudi Arabia", "img": "https://flagcdn.com/w80/sa.": "Iraq", "img": "https://flagcdn.com/w80/iq.png", "png", "g": "H"}, "32": {"n": "Uruguay", "img": "g": "I"}, "36": {"n": "Norway", "img": "https://flagcdn.https://flagcdn.com/w80/uy.png", "g": "H"},
    "com/w80/no.png", "g": "I"},
    "37": {"n33": {"n": "France", "img": "https://flagcdn.com/w80/": "Argentina", "img": "https://flagcdn.com/w80/ar.png", "fr.png", "g": "I"}, "34": {"n": "Senegal", "img":g": "J"}, "38": {"n": "Algeria", "img": "https://flagcdn "https://flagcdn.com/w80/sn.png", "g": "I"},
    "35": {"n": "Iraq", "img": "https://flagcdn.com/w80.com/w80/dz.png", "g": "J"},
    "39": {"/iq.png", "g": "I"}, "36": {"n": "Norway", "img":n": "Austria", "img": "https://flagcdn.com/w80/at.png", "g": "J"}, "40": {"n": "Jordan", "img": "https://flagcdn "https://flagcdn.com/w80/no.png", "g": "I"},
    .com/w80/jo.png", "g": "J"},
    "41": {""37": {"n": "Argentina", "img": "https://flagcdn.com/w80n": "Portugal", "img": "https://flagcdn.com/w80/pt.png",/ar.png", "g": "J"}, "38": {"n": "Algeria", "img "g": "K"}, "42": {"n": "DR Congo", "img": "https://flag": "https://flagcdn.com/w80/dz.png", "g": "J"},
cdn.com/w80/cd.png", "g": "K"},
    "43":    "39": {"n": "Austria", "img": "https://flagcdn.com/w8 {"n": "Uzbekistan", "img": "https://flagcdn.com/w80/uz0/at.png", "g": "J"}, "40": {"n": "Jordan", "img.png", "g": "K"}, "44": {"n": "Colombia", "img": "https": "https://flagcdn.com/w80/jo.png", "g": "J"},
://flagcdn.com/w80/co.png", "g": "K"},
    "4    "41": {"n": "Portugal", "img": "https://flagcdn.com/w85": {"n": "England", "img": "https://flagcdn.com/w80/gb0/pt.png", "g": "K"}, "42": {"n": "DR Congo", "-eng.png", "g": "L"}, "46": {"n": "Croatia", "imgimg": "https://flagcdn.com/w80/cd.png", "g": "K"},": "https://flagcdn.com/w80/hr.png", "g": "L"},

    "43": {"n": "Uzbekistan", "img": "https://flagcdn.com    "47": {"n": "Ghana", "img": "https://flagcdn.com/w8/w80/uz.png", "g": "K"}, "44": {"n": "Colombia0/gh.png", "g": "L"}, "48": {"n": "Panama", "", "img": "https://flagcdn.com/w80/co.png", "g": "img": "https://flagcdn.com/w80/pa.png", "g": "L"}K"},
    "45": {"n": "England", "img": "https://flagcdn.com
}

RAW_MATCHES = [
    ["A", "11/06 22:/w80/gb-eng.png", "g": "L"}, "46": {"n":00", "Estadio Azteca", "1", "2"], ["A", "12/06 "Croatia", "img": "https://flagcdn.com/w80/hr.png", " 05:00", "Estadio Akron", "3", "4"],
    ["B", "g": "L"},
    "47": {"n": "Ghana", "img": "https://flag12/06 22:00", "BMO Field", "5", "6"], ["cdn.com/w80/gh.png", "g": "L"}, "48": {"nD", "13/06 04:00", "SoFi Stadium", "13",": "Panama", "img": "https://flagcdn.com/w80/pa.png", "14"],
    ["D", "14/06 07:00", "BC "g": "L"}
}

RAW_MATCHES = [
    ["A", "11/06 Place", "15", "16"], ["B", "13/06 22:0 22:00", "Estadio Azteca", "1", "2"], ["A", "10", "Levi's Stadium", "7", "8"],
    ["C", "14/02/06 05:00", "Estadio Akron", "3", "4"],
    6 01:00", "MetLife Stadium", "9", "10"], ["C", "["B", "12/06 22:00", "BMO Field", "5",14/06 04:00", "Gillette Stadium", "11", "12 "6"], ["D", "13/06 04:00", "SoFi Stadium","],
    ["E", "14/06 20:00", "NRG Stadium", "13", "14"],
    ["D", "14/06 07:0 "17", "18"], ["F", "14/06 23:00", "AT&T Stadium", "0", "BC Place", "15", "16"], ["B", "13/06 22:00", "Levi's Stadium", "7", "8"],
    ["C", "21", "22"],
    ["E", "15/06 02:00", "Lincoln Field", "14/06 01:00", "MetLife Stadium", "9", "10"],19", "20"], ["F", "15/06 05:00", " ["C", "14/06 04:00", "Gillette Stadium", "11Estadio BBVA", "23", "24"],
    ["H", "15/06", "12"],
    ["E", "14/06 20:00", " 19:00", "Mercedes-Benz", "29", "30"], ["G", "15/06 22:00", "Lumen Field", "25", "26NRG Stadium", "17", "18"], ["F", "14/06 23"],
    ["H", "16/06 01:00", "Hard Rock", ":00", "AT&T Stadium", "21", "22"],
    ["E", "15/06 02:00", "Lincoln Field", "19", "20"],31", "32"], ["G", "16/06 04:00", "SoFi Stadium", "27 ["F", "15/06 05:00", "Estadio BBVA", "2", "28"],
    ["J", "17/06 07:00", "3", "24"],
    ["H", "15/06 19:00",Levi's Stadium", "39", "40"], ["I", "16/06 1 "Mercedes-Benz", "29", "30"], ["G", "15/06 20:00", "MetLife", "33", "34"],
    ["I", "12:00", "Lumen Field", "25", "26"],
    ["H", "7/06 01:00", "Gillette", "35", "36"], ["16/06 01:00", "Hard Rock", "31", "32"], ["G", "16/J", "17/06 04:00", "Arrowhead", "37", "06 04:00", "SoFi Stadium", "27", "28"],
    38"],
    ["K", "17/06 08:00", "NRG["J", "17/06 07:00", "Levi's Stadium", "3 Stadium", "41", "42"], ["L", "17/06 11:09", "40"], ["I", "16/06 10:00", "Met0", "AT&T Stadium", "45", "46"],
    ["L", "18/06 02:Life", "33", "34"],
    ["I", "17/06 0100", "BMO Field", "47", "48"], ["K", "18/06 05:00:00", "Gillette", "35", "36"], ["J", "17/0", "Estadio Azteca", "43", "44"],
    ["A", "18/6 04:00", "Arrowhead", "37", "38"],
    ["K06 07:00", "Mercedes-Benz", "4", "2"], ["B", "", "17/06 08:00", "NRG Stadium", "41", "18/06 10:00", "SoFi Stadium", "8", "6"],
42"], ["L", "17/06 11:00", "AT&T Stadium    ["B", "19/06 01:00", "BC Place", "5",", "45", "46"],
    ["L", "18/06 02: "7"], ["A", "19/06 04:00", "Estadio Akron",00", "BMO Field", "47", "48"], ["K", "18/06 05:00 "1", "3"],
    ["D", "20/06 06:00",", "Estadio Azteca", "43", "44"],
    ["A", "18/06 07: "Levi's Stadium", "16", "14"], ["D", "19/06 00", "Mercedes-Benz", "4", "2"], ["B", "18/06 10:00", "Lumen Field", "13", "15"],
    ["C", "20/06 01:00", "Gillette", "12", "1010:00", "SoFi Stadium", "8", "6"],
    ["B", "19/06 01:00", "BC Place", "5", "7"], ["A","], ["C", "20/06 03:30", "Lincoln Field", "9", "11"],
    ["F", "21/06 07:00", "Est "19/06 04:00", "Estadio Akron", "1", "3"],
    ["D", "20/06 06:00", "Levi's Stadium",adio BBVA", "24", "22"], ["F", "20/06 08 "16", "14"], ["D", "19/06 10:00",:00", "NRG Stadium", "21", "23"],
    ["E", "2 "Lumen Field", "13", "15"],
    ["C", "20/060/06 11:00", "BMO Field", "17", "19"], ["E", "21/ 01:00", "Gillette", "12", "10"], ["C", "206 03:00", "Arrowhead", "20", "18"],
    ["0/06 03:30", "Lincoln Field", "9", "11"],
    H", "21/06 07:00", "Mercedes-Benz", "29",["F", "21/06 07:00", "Estadio BBVA", "2 "31"], ["G", "21/06 10:00", "SoFi Stadium4", "22"], ["F", "20/06 08:00", "NR", "25", "27"],
    ["H", "22/06 01:G Stadium", "21", "23"],
    ["E", "20/06 11:00", "BMO Field", "17", "19"], ["E", "2100", "Hard Rock", "32", "30"], ["G", "22/06 04:00/06 03:00", "Arrowhead", "20", "18"],
    ", "BC Place", "28", "26"],
    ["J", "22/06["H", "21/06 07:00", "Mercedes-Benz", "29", "31"], ["G", "21/06 10:00", "SoFi 08:00", "AT&T Stadium", "37", "39"], ["I", Stadium", "25", "27"],
    ["H", "22/06 01 "23/06 12:00", "Lincoln Field", "33", "35"],
    ["I", "23/06 03:00", "MetLife", ":00", "Hard Rock", "32", "30"], ["G", "22/06 04:0036", "34"], ["J", "23/06 06:00", "Levi's Stadium",", "BC Place", "28", "26"],
    ["J", "22/06 "40", "38"],
    ["K", "23/06 08:0 08:00", "AT&T Stadium", "37", "39"], ["I",0", "NRG Stadium", "41", "43"], ["L", "23/06 11:00 "23/06 12:00", "Lincoln Field", "33", "35", "Gillette", "45", "47"],
    ["L", "24/06"],
    ["I", "23/06 03:00", "MetLife", "36", "34"], ["J", "23/06 06:00", " 02:00", "BMO Field", "48", "46"], ["K", "Levi's Stadium", "40", "38"],
    ["K", "23/0624/06 05:00", "Estadio Akron", "44", "42"],
    ["B", "24/06 10:00", "BC Place", " 08:00", "NRG Stadium", "41", "43"], ["L", "23/06 11:00", "Gillette", "45", "47"],
    ["L", "24/06 02:00", "BMO Field", "48", "46"], ["K", "24/8", "5"], ["B", "24/06 10:00", "Lumen Field", "6", "7"],
    ["C", "25/06 01:006 05:00", "Estadio Akron", "44", "42"],
    0", "Hard Rock Stadium", "12", "9"], ["C", "25/06 ["B", "24/06 10:00", "BC Place", "8", "5"], ["B", "24/06 10:00", "Lumen Field", "01:00", "Mercedes-Benz", "10", "11"],
    ["A",6", "7"],
    ["C", "25/06 01:00", " "25/06 04:00", "Estadio Azteca", "4", "1Hard Rock Stadium", "12", "9"], ["C", "25/06 01:"], ["A", "25/06 04:00", "Estadio BBVA", "2", "3"],
    ["E", "25/06 11:00", "MetLife", "20", "17"], ["E", "25/06 11:00", "Mercedes-Benz", "10", "11"],
    ["A", "2500", "Lincoln Field", "18", "19"],
    ["F", "26//06 04:00", "Estadio Azteca", "4", "1"], ["A", "25/06 04:00", "Estadio BBVA", "2", "06 02:00", "AT&T Stadium", "22", "23"], ["F", "26/06 02:00", "Arrowhead", "24", "3"],
    ["E", "25/06 11:00", "MetLife",21"],
    ["D", "26/06 05:00", "SoFi "20", "17"], ["E", "25/06 11:00", Stadium", "16", "13"], ["D", "26/06 05:0 "Lincoln Field", "18", "19"],
    ["F", "26/06 0", "Levi's Stadium", "14", "15"],
    ["I", "2602:00", "AT&T Stadium", "22", "23"], ["F", "/06 10:00", "Gillette", "36", "33"], ["I26/06 02:00", "Arrowhead", "24", "21"],
    ["D", "2", "26/06 10:00", "BMO Field", "34", "6/06 05:00", "SoFi Stadium", "16", "13"], ["D", "26/35"],
    ["H", "27/06 03:00", "Estadio06 05:00", "Levi's Stadium", "14", "15"],
 Akron", "32", "29"], ["H", "27/06 03:0    ["I", "26/06 10:00", "Gillette", "360", "NRG Stadium", "30", "31"],
    ["G", "27/06 06:", "33"], ["I", "26/06 10:00", "BMO00", "Lumen Field", "26", "27"], ["G", "27/06 06:00 Field", "34", "35"],
    ["H", "27/06 03:00", "Estadio Akron", "32", "29"], ["H", "27/", "BC Place", "28", "25"],
    ["L", "28/0606 03:00", "NRG Stadium", "30", "31"],
     12:00", "MetLife", "48", "45"], ["L", "2["G", "27/06 06:00", "Lumen Field", "268/06 12:00", "Lincoln Field", "46", "47"],
    ["K", "28", "27"], ["G", "27/06 06:00", "BC Place/06 02:30", "Hard Rock Stadium", "44", "41"], ["K", "28/", "28", "25"],
    ["L", "28/06 12:06 02:30", "Mercedes-Benz", "42", "43"],
    00", "MetLife", "48", "45"], ["L", "28/06 12:00["J", "28/06 05:00", "Arrowhead", "38",", "Lincoln Field", "46", "47"],
    ["K", "28/06 "39"], ["J", "28/06 05:00", "AT&T 02:30", "Hard Rock Stadium", "44", "41"], ["K", " Stadium", "40", "37"]
]

# --- 4. SESSION STATE ---
def init28/06 02:30", "Mercedes-Benz", "42", "43"],
    ["J", "28/06 05:00", "Arrowhead", "_session():
    matches = []
    for i, m_data in enumerate(RAW_MATCHES):38", "39"], ["J", "28/06 05:00", "
        matches.append({
            "id": i+1, "group": m_data[0],AT&T Stadium", "40", "37"]
]

# --- 4. SESSION STATE --- "dt": m_data[1], "st": m_data[2],
            "h_id
def init_session():
    matches = []
    for i, m_data in enumerate(RAW_MATCHES):
": m_data[3], "a_id": m_data[4], "sh": None, "        matches.append({
            "id": i+1, "group": m_data[0], "dt": m_data[1sa": None, "fin": False,
            "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0, "p_h":], "st": m_data[2],
            "h_id": m_data[3], " 0, "p_a": 0, "og_h": 0, "og_a":a_id": m_data[4], "sh": None, "sa": None, "fin": False 0,
            "ref": "TBD", "turn": "Καμία"
        })
    ,
            "y_h": 0, "y_a": 0, "r_h":st.session_state.wc_matches = matches

if 'wc_matches' not in st.session_ 0, "r_a": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0,
            "ref":state:
    init_session()

# --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_ "TBD", "turn": "Καμία"
        })
    st.session_state.wc_state.wc_matches:
        if not m['fin']:
            m['sh'], m['sa']matches = matches

if 'wc_matches' not in st.session_state:
    init_session()

# --- 5. FUNCTIONS ---
def auto_play():
    for m in st.session_state = random.randint(0, 4), random.randint(0, 4)
            m['y_h'], m['y_a'] = random.randint(0, 3), random.randint(0.wc_matches:
        if not m['fin']:
            m['sh'], m['sa'] = random.randint(0,, 3)
            m['r_h'] = random.randint(0, 1) if random 4), random.randint(0, 4)
            m['y_h'], m['y_.random() > 0.9 else 0
            m['r_a'] = random.randint(0, 1) ifa'] = random.randint(0, 3), random.randint(0, 3)
            m['r_h'] = random.randint(0, 1) if random.random() > 0. random.random() > 0.9 else 0
            # Τυχαία επιλογή ανατροπής αν9 else 0
            m['r_a'] = random.randint(0, 1) if random.random() > 0.9 else 0
            m['fin'] = True
    st.rerun()

def reset(): υπάρχει νικητής
            if m['sh'] > m['sa'] and random.random() > 0.85: m['turn'] = "Home SCORE First and LOSE"
            elif m['sa'] > m['
    init_session()
    st.cache_data.clear()
    st.rerun()

@st.cache_datash'] and random.random() > 0.85: m['turn'] = "Away SCORE First and(ttl=3600)
def get_ai_prediction(model_id, prompt):
     LOSE"
            m['fin'] = True
    st.rerun()

def reset():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model =init_session()
    st.cache_data.clear()
    st.rerun()

@st genai.GenerativeModel(model_id)
    return model.generate_content(prompt).text

.cache_data(ttl=3600)
def get_ai_prediction(model_id,# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 202 prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])6 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m in st.session_
    model = genai.GenerativeModel(model_id)
    return model.generate_content(state.wc_matches if m['fin']]
total_y = sum(m['y_h'] +prompt).text

# --- 6. HEADER & DASHBOARD ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m m['y_a'] for m in fin_m)
total_r = sum(m['r_h'] + m['r_a'] for m in fin_m)
total_p = sum(m = [m for m in st.session_state.wc_matches if m['fin']]
total_y['p_h'] + m['p_a'] for m in fin_m)
total_og = = sum(m['y_h'] + m['y_a'] for m in fin_m)
total_r = sum( sum(m['og_h'] + m['og_a'] for m in fin_m)

c1, c2, c3, c4, c5, c6 = st.columns(6)
m['r_h'] + m['r_a'] for m in fin_m)
total_pwith c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/ = sum(m['p_h'] + m['p_a'] for m in fin_m)
total_og = sum(m['og_h'] + m['og_a'] for m in fin_72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
m)

c1, c2, c3, c4, c5, c6 = st.columnswith c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{(6)
with c1: st.markdown(f'<div class="stat-card"><div class="sum(m["sh"]+m["sa"] for m in fin_m if m["sh"] is notstat-val">{len(fin_m)}/72</div><div class="stat-label">Matches</div> None)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_allow_html=True)</div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="
with c3: st.markdown(f'<div class="stat-card"><div class="stat-valstat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin_m if m["" style="color:#facc15!important">{total_y}</div><div class="stat-labelsh"] is not None)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_allow_">🟨Yellow</div></div>', unsafe_allow_html=True)
with c4: st.html=True)
with c3: st.markdown(f'<div class="stat-card"><div classmarkdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444!important">{total_r}</div><div class="stat-label">🟥Red</div></div>',="stat-val" style="color:#facc15!important">{total_y}</div><div class unsafe_allow_html=True)
with c5: st.markdown(f'<div class="stat-="stat-label">🟨Yellow</div></div>', unsafe_allow_html=True)
with ccard"><div class="stat-val" style="color:#22d3ee!important">{total_p4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="}</div><div class="stat-label">🎯Pens</div></div>', unsafe_allow_html=True)
color:#ef4444!important">{total_r}</div><div class="stat-label">🟥Red</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<divwith c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{total_og}</div><div class="stat-label">⚠️OG</div></div>', unsafe class="stat-card"><div class="stat-val" style="color:#22d3ee!important_allow_html=True)

st.write("")
b1, b2 = st.columns([2">{total_p}</div><div class="stat-label">🎯Pens</div></div>', unsafe_allow_html, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙ=True)
with c6: st.markdown(f'<div class="stat-card"><div class="ΧΝΙΔΙ (SIMULATOR)", on_click=auto_play, type="primary")
withstat-val" style="color:#fb923c!important">{total_og}</div><div class b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset, type="secondary")="stat-label">⚠️OG</div></div>', unsafe_allow_html=True)

st.write("")


tabs = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊 ΒΑΘΜb1, b2 = st.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "📊 ΑΝΑΛΟ ΠΑΙΧΝΙΔΙ (SIMULATOR)", on_click=auto_play, type="ΥΣΗ ΣΚΟΡ", "🔄 ΑΝΑΤΡΟΠΕΣ", "🔮 ΠΡΟΒΛΕprimary")
with b2: st.button("🔄 RESET ALL TOURNAMENT", on_click=reset,ΨΕΙΣ"])

with tabs[0]:
    cols = st.columns(3)
    for idx type="secondary")

tabs = st.tabs(["📅 ΗΜΕΡΟΛΟΓΙΟ", "📊, m in enumerate(st.session_state.wc_matches):
        h = TEAMS_MAP. ΒΑΘΜΟΛΟΓΙΕΣ", "📈 ΠΟΡΕΙΑ ΟΜΑΔΩΝ", "get(m['h_id'], {"n": "N/A", "img": ""})
        a = TEAMS_MAP.get(m['a_id'], {"n": "N/A", "img📊 ΑΝΑΛΥΣΗ ΣΚΟΡ", "🔄 ΑΝΑΤΡΟΠΕΣ", "🔮 Π": ""})
        with cols[idx % 3]:
            st.markdown(f"""
            <ΡΟΒΛΕΨΕΙΣ"])

with tabs[0]:
    cols = st.columns(3)div class="match-card">
                <div style="display:flex; justify-content: space-between
    for idx, m in enumerate(st.session_state.wc_matches):
        h = TE; margin-bottom:5px;">
                    <span class="group-tag">GROUP {m['group']}AMS_MAP.get(m['h_id'], {"n": "N/A", "img": ""</span>
                    <span style="font-size:10px; color:#94a3b8;">})
        a = TEAMS_MAP.get(m['a_id'], {"n": "N/🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; justify-content:A", "img": ""})
        with cols[idx % 3]:
            st.markdown(f space-around; align-items:center;">
                    <div style="text-align:center; width:"""
            <div class="match-card">
                <div style="display:flex; justify-content40%; font-weight:bold;"><img src="{h['img']}" width="25"><br>{h['n']}: space-between; margin-bottom:5px;">
                    <span class="group-tag">GROUP {</div>
                    <div style="font-size:20px; color:#06b6d4;m['group']}</span>
                    <span style="font-size:10px; color:#94a3b8;">🕒 {m['dt']}</span>
                </div>
                <div style="display:flex; font-weight:800;">{m['sh'] if m['sh'] is not None else '-'} justify-content: space-around; align-items:center;">
                    <div style="text-align:center; width:40%; font-weight:bold;"><img src="{h['img']}" width="25"><br>{h['n']}</div>
                    <div style="font-size:20px; color:#06b6d4; font-weight:800;">{m['sh'] if m[' : {m['sa'] if m['sa'] is not None else '-'}</div>
                    <div style="text-align:center; width:40%;"><img src="{a['img']}" width="25sh'] is not None else '-'} : {m['sa'] if m['sa'] is not None else '-"><br>{a['n']}</div>
                </div>
                <div style="font-size:9px;'}</div>
                    <div style="text-align:center; width:40%;"><img src="{a color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:4px;">
                    🟨 {m['y['img']}" width="25"><br>{a['n']}</div>
                </div>
                <div style_h']}:{m['y_a']} | 🟥 {m['r_h']}:{m['r="font-size:9px; color:#94a3b8; text-align:center; border_a']} | 🎯 {m['p_h']}:{m['p_a']} | ⚠️ {-top: 1px solid #1e293b; padding-top:4px;">
                    m['og_h']}:{m['og_a']}
                </div>
                <div style="font-🟨 {m['y_h']}:{m['y_a']} | 🟥 {m['size:9px; color:#94a3b8; text-align:center; padding-top:r_h']}:{m['r_a']} | 🎯 {m['p_h']}:{m['2px;">
                    🏁 Ref: {m['ref']} | 📍 {m['st']} | 🔄p_a']} | ⚠️ {m['og_h']}:{m['og_a']}
                </div> {m['turn']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
                <div style="font-size:9px; color:#94a3b8; text-with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columns(align:center; padding-top:2px;">
                    🏁 Ref: {m['ref']} | 📍2)
                sh_v = ch.number_input(f"Goals {h['n']}",  {m['st']} | 🔄 {m['turn']}
                </div>
            </div>
            """, unsafe_allow_html=0, 15, m['sh'] if m['sh'] is not None else 0, key=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {True)
            with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columnsa['n']}", 0, 15, m['sa'] if m['sa'] is not None(2)
                sh_v = ch.number_input(f"Goals {h['n']}", else 0, key=f"sa{m['id']}")
                yh_v = ch.slider( 0, 15, m['sh'] if m['sh'] is not None else 0, keyf"Yellow {h['n']}", 0, 10, m['y_h'], key=f"yh{m['id']}")
                ya_v = ca.slider(f"Yellow {a['=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {a['n']}", n']}", 0, 10, m['y_a'], key=f"ya{m['0, 15, m['sa'] if m['sa'] is not None else 0, key=id']}")
                rh_v = ch.number_input(f"Red {h['n']}", f"sa{m['id']}")
                yh_v = ch.slider(f"Yellow {h['n']}", 0, 0, 5, m['r_h'], key=f"rh{m['id']}")
                ra10, m['y_h'], key=f"yh{m['id']}")
                ya_v_v = ca.number_input(f"Red {a['n']}", 0, 5, = ca.slider(f"Yellow {a['n']}", 0, 10, m['y m['r_a'], key=f"ra{m['id']}")
                ph_v = ch.number_input(f"Pens_a'], key=f"ya{m['id']}")
                rh_v = ch.number_input {h['n']}", 0, 5, m['p_h'], key=f"ph{(f"Red {h['n']}", 0, 5, m['r_h'], key=m['id']}")
                pa_v = ca.number_input(f"Pens {a['n']f"rh{m['id']}")
                ra_v = ca.number_input(f"Red {}", 0, 5, m['p_a'], key=f"pa{m['id']}")
a['n']}", 0, 5, m['r_a'], key=f"ra{m                oh_v = ch.number_input(f"OG {h['n']}", 0, ['id']}")
                ph_v = ch.number_input(f"Pens {h['n']}",5, m['og_h'], key=f"oh{m['id']}")
                oa_v = 0, 5, m['p_h'], key=f"ph{m['id']}")
                 ca.number_input(f"OG {a['n']}", 0, 5, m['og_a'], key=f"oa{m['id']}")
                ref_v = st.text_input("Referee", m['ref'], key=f"ref_in{m['id']}")
                turn_v = st.selectbox("Ανατροπή", ["Καμία", "2/1 (Ανατροπή)", "1/2 (Ανατροπή)", "Home SCORE First and LOSE", "Away SCORE First and LOSE"], index=0, key=f"turn_{m['id']}")
                if st.button("Save", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v, "sa": sa_v, "fin": True, "y_h": yh_v, "y_a": ya_v, "r_h": rh_v, "r_a": ra_v, "p_h": ph_v,pa_v = ca.number_input(f"Pens {a['n']}", 0, 5, m['p_a'], key=f"pa{m['id']}")
                oh_v = ch.number_input(f"OG {h['n']}", 0, 5, m['og_h'], key=f"oh{m['id']}")
                oa_v = ca.number_input(f"OG {a['n']}", 0, 5, m['og_a'], key=f "p_a": pa_v, "og_h": oh_v, "og_a": oa_v"oa{m['id']}")
                ref_v = st.text_input("Referee", m['ref'], key=f"ref_in{m['id']}")
                turn_v = st.selectbox("Ανατροπή", ["Καμία", "2/1 (Ανατροπή)", "1/2 (Ανατροπή)", "Home SCORE First and LOSE", "Away SCORE First and LOSE"], index=0,, "ref": ref_v, "turn": turn_v})
                    st.rerun()

with key=f"turn_{m['id']}")
                if st.button("Save Result", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v, "sa": sa_v, "fin": True, tabs[1]:
    cols_s = st.columns(3)
    GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", " "y_h": yh_v, "y_a": ya_v, "r_h": rhI", "J", "K", "L"]
    for i, gId in enumerate(GROUPS__v, "r_a": ra_v, "p_h": ph_v, "p_L):
        with cols_s[i % 3]:
            st.markdown(f"#### Groupa": pa_v, "og_h": oh_v, "og_a": oa_v, "ref": ref_v, {gId}")
            g_team_ids = [tid for tid, d in TEAMS_MAP. "turn": turn_v})
                    st.rerun()

# ΒΑΘΜΟΛΟΓΙΕΣ
with tabsitems() if d['g'] == gId]
            res = []
            for tid in g_team[1]:
    cols_s = st.columns(3)
    GROUPS_L = ["A_ids:
                team = TEAMS_MAP[tid]
                pts, gd, y, r,", "B", "C", "D", "E", "F", "G", "H", "I p, og = 0, 0, 0, 0, 0, 0
                for", "J", "K", "L"]
    for i, gId in enumerate(GROUPS_L m in st.session_state.wc_matches:
                    if m['fin'] and (m['h):
        with cols_s[i % 3]:
            st.markdown(f"#### Group {_id'] == tid or m['a_id'] == tid):
                        is_h = m['h_id'] == tid
                        h_s, a_s = (m['sh'], m['sa'])gId}")
            g_team_ids = [tid for tid, d in TEAMS_MAP.items if is_h else (m['sa'], m['sh'])
                        y += m['y_h'] if is_h else() if d['g'] == gId]
            res = []
            for tid in g_team_ids:
                team = TEAMS_MAP[tid]
                pts, gd, y, r, p m['y_a']
                        r += m['r_h'] if is_h else m['r, og = 0, 0, 0, 0, 0, 0
                for m_a']
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
                        elif h_s == a_s: pts += 1
                 in st.session_state.wc_matches:
                    if m['fin'] and (m['h_res.append({"Flag": team['img'], "Team": team['n'], "Pts": pts, "GDid'] == tid or m['a_id'] == tid):
                        is_h = m['h_": gd, "Y": y, "R": r})
            df = pd.DataFrame(res).sortid'] == tid
                        h_s, a_s = (m['sh'], m['sa']) if is_h else (m['_values(by=["Pts", "GD"], ascending=False)
            st.data_editor(df,sa'], m['sh'])
                        y += m['y_h'] if is_h else m['y column_config={"Flag": st.column_config.ImageColumn("🏳️")}, hide_index=True_a']
                        r += m['r_h'] if is_h else m['r_a'], key=f"table_{gId}")

with tabs[2]:
    all_names = sorted([d['n'] for d in TEAMS_MAP.values()])
    sel_t = st.selectbox("
                        gd += (h_s - a_s)
                        if h_s > a_s: pts += 3
Επιλέξτε Ομάδα:", all_names)
    team_id = next(k for k                        elif h_s == a_s: pts += 1
                res.append({"Flag": team['img'], "Team": team[',v in TEAMS_MAP.items() if v['n'] == sel_t)
    t_n'], "Pts": pts, "GD": gd, "Y": y, "R": r})
            matches = [m for m in st.session_state.wc_matches if (m['h_id']df = pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False)
 == team_id or m['a_id'] == team_id)]
    t_pts, t_gf, t            st.data_editor(df, column_config={"Flag": st.column_config.ImageColumn("_ga, t_y, t_r = 0, 0, 0, 0, 0
    for m in🏳️")}, hide_index=True, key=f"table_{gId}")

# ΠΟΡ t_matches:
        if m['fin']:
            is_h = m['h_id'] ==ΕΙΑ ΟΜΑΔΩΝ
with tabs[2]:
    all_names = sorted([d['n'] for d in TEAMS_ team_id
            g, c = (m['sh'], m['sa']) if is_h else (m['sa'], mMAP.values()])
    sel_t = st.selectbox("Επιλέξτε Ομάδα:", all_names)
    team_id = next(k for k,v in TEAMS_MAP.items()['sh'])
            t_gf += g; t_ga += c
            t_y += m['y_h'] if is_ if v['n'] == sel_t)
    t_matches = [m for m in st.sessionh else m['y_a']
            if g > c: t_pts += 3
            elif_state.wc_matches if (m['h_id'] == team_id or m['a_id g == c: t_pts += 1
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Points", t_pts);'] == team_id)]
    
    t_pts, t_gf, t_ga, t_y, t_r c_s2.metric("Goals", f"{t_gf}-{t_ga}"); c_s3. = 0, 0, 0, 0, 0
    for m in t_matches:metric("Cards (Y-R)", f"{t_y}-{t_r}")
    cols_team =
        if m['fin']:
            is_h = m['h_id'] == team_id
 st.columns(3)
    for idx, m in enumerate(t_matches):
        with cols_            g, c = (m['sh'], m['sa']) if is_h else (m['sa'],team[idx % 3]:
            res_col = "#10b981" if m[' m['sh'])
            t_gf += g; t_ga += c
            t_y += m['y_h'] iffin'] else "#1e293b"
            h_n = TEAMS_MAP[m[' is_h else m['y_a']
            t_r += m['r_h'] if is_h else m['h_id']]['n']; a_n = TEAMS_MAP[m['a_id']]['n']
            str_a']
            if g > c: t_pts += 3
            elif g == c:.markdown(f"""<div class="match-card" style="border-top:4px solid {res t_pts += 1
    
    c_s1, c_s2, c_s3_col}">
            <b>Αγώνας {idx+1}</b><br>{h_n} {m['sh'] if m['sh'] is not None else ''} - {m['sa'] if m[', c_s4 = st.columns(4)
    c_s1.metric("Points", t_pts);sa'] is not None else ''} {a_n}
            </div>""", unsafe_allow_html=True)

with tabs[3]: c_s2.metric("Goals", f"{t_gf}-{t_ga}"); c_s3.metric("Cards (Y-R
    st.markdown("### 📊 Πίνακας Πιθανών Σκορ & Συχν)", f"{t_y}-{t_r}")
    
    cols_team = st.columns(3)
    for idx,ότητας")
    actual_scores = [(m['sh'], m['sa']) for m in st.session_state.wc_matches if m['fin']]
    for h_g in range(5):
        cols_ m in enumerate(t_matches):
        with cols_team[idx % 3]:
            res_col = "#10b9score = st.columns(5)
        for a_g in range(5):
            with cols_81" if m['fin'] else "#1e293b"
            h_n = TEscore[a_g]:
                current_score = (h_g, a_g)
                countAMS_MAP[m['h_id']]['n']; a_n = TEAMS_MAP[m['a_id']]['n']
            st.markdown(f"""<div class="match-card" style = actual_scores.count(current_score)
                st_class = "score-out" if count="border-top:4px solid {res_col}">
            <b>Αγώνας {idx+1 > 0 else "score-delayed"
                st.markdown(f"""<div class="score-box}</b><br>{h_n} {m['sh'] if m['sh'] is not None else '' {st_class}">{h_g}-{a_g}<br><span style='font-size:9} - {m['sa'] if m['sa'] is not None else ''} {a_n}
            </div>""", unsafe_px'>{'✅' if count > 0 else '⏳'} {count if count > 0 else ''}</span></div>""", unsafe_allow_html=True)

with tabs[4]:
    st.markdown("###allow_html=True)

# ΑΝΑΛΥΣΗ ΣΚΟΡ
with tabs[3]: 🔄 Ανάλυση Ανατροπών (Turnarounds)")
    t_fin = [m for m in
    st.markdown("### 📊 Πίνακας Πιθανών Σκορ & Συχν st.session_state.wc_matches if m['fin'] and m['turn'] != "Καμία"]ότητας")
    actual_scores = [(m['sh'], m['sa']) for m in st.session_state.wc_matches if
    t_col1, t_col2, t_col3 = st.columns(3)
 m['fin']]
    for h_g in range(5):
        cols_score = st.columns    t_col1.metric("Σύνολο Ανατροπών", len(t_fin))
    t_col2.(5)
        for a_g in range(5):
            with cols_score[a_gmetric("Home SCORE First and LOSE", len([m for m in t_fin if m['turn'] == "Home SCORE]:
                current_score = (h_g, a_g)
                count = actual_scores. First and LOSE"]))
    t_col3.metric("Away SCORE First and LOSE", len([mcount(current_score)
                st_class = "score-out" if count > 0 else "score-delayed"
                st for m in t_fin if m['turn'] == "Away SCORE First and LOSE"]))
    st.write("---")
    if.markdown(f"""<div class="score-box {st_class}">{h_g}-{a_ t_fin:
        for m in t_fin:
            h_n = TEAMS_MAP[g}<br><span style='font-size:9px'>{'✅' if count > 0 else '⏳'} {count if count >m['h_id']]['n']; a_n = TEAMS_MAP[m['a_id']]['n']
            st.markdown(f"""<div class="turnaround-card"><span style="color:#06b6d4; font-size:12px; font-weight:bold;">{m['turn']}</span><br><b>{h_n} {m['sh']} - {m['sa']} {a_n}</b></div>""", unsafe_allow_html= 0 else ''}</span></div>""", unsafe_allow_html=True)

# ΑΝΑΤΡΟΠΕΣ
with tabs[4]:
    st.markdown("### 🔄 Ανάλυση Ανατροπών (Turnarounds)")
    t_True)

with tabs[5]:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            cfin = [m for m in st.session_state.wc_matches if m['fin'] and m['turn'] != "Καμία"]
    t_col1, t_col2, t_col3 = st.columns(3)
    t_col1.metric("Σύνολο Ανατροπών", len(t_fin))
    t_col2.1, c2 = st.columns(2)
            home = c1.selectbox("Home", all_names, key="ai_h")
            away = c2.selectbox("Away", all_names, indexmetric("SCORE First and LOSE (Home)", len([m for m in t_fin if m['turn'] == "Home SCORE First and LOSE"]))
    t_col3.metric("SCORE First and LOSE (Away)", len([m for=1, key="ai_a")
            m_no = st.number_input("Αγώνας #", 1, 104, 1)
            extra_notes = st.text_area("🗒️ Σημειώσεις τελευταίας στιγμής:", placeholder="Π.χ. Βρέχει, λείπει ο αρχηγός...")
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩ m in t_fin if m['turn'] == "Away SCORE First and LOSE"]))
    st.write("---")
    if t_fin:
        for m in t_fin:
            h_n = TEAMS_MAP[ΘΕΙΣ", type="primary"):
                with st.spinner("Analyzing..."):
                    prompt = f"m['h_id']]['n']; a_n = TEAMS_MAP[m['a_id']]['n']
            st.markdown(f"""<div class="turnaround-card"><span style="color:#06b6d4Analyze match #{m_no}: {home} vs {away}. Notes: {extra_notes}. Tactical prediction in Greek."
                    ans = get_ai_prediction('gemini-1.5-flash', prompt)
                    st.info(ans)
        except Exception as e: st.error(f"Error: {e; font-size:12px; font-weight:bold;">{m['turn']}</span><br><b>{h_n} {m['sh']} - {m['sa']} {a_n}</b> (Όμιλος {m['group']})</div>""", unsafe_allow_html=True)
    else: st}")
```.info("Δεν έχουν σημειωθεί ανατροπές ακόμα.")

with tabs[5]:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            c1, c2 = st.columns(2)
            home = c1.selectbox("Home", all_names, key="ai_h")
            away = c2.selectbox("Away", all_names, index=1, key="ai_a")
            m_no = st.number_input("Αγώνας #", 1, 104, 1)
            extra_notes = st.text_area("🗒️ Σημειώσεις τελευταίας στιγμής:", placeholder="Π.χ. Βρέχει, λείπει ο αρχηγός...")
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary"):
                with st.spinner("Analyzing..."):
                    prompt = f"Analyze match #{m_no}: {home} vs {away}. Notes: {extra_notes}. Tactical prediction in Greek."
                    ans = get_ai_prediction('gemini-1.5-flash', prompt)
                    st.info(ans)
        except Exception as e: st.error(f"Error: {e}")
