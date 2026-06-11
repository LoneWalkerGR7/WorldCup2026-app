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
    
    .stat-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="stTable"] {
        background-color: #0f172a;
        border-radius: 10px;
        border: 1px solid #1e293b;
        padding: 5px;
    }
    div[data-testid="stTable"] table { color: white !important; width: 100% !important; }
    
    button[data-testid="stBaseButton-secondary"] {
        color: black !important;
        background-color: #f1f5f9 !important;
        font-weight: 800 !important;
        border: 2px solid #ffffff !important;
        text-transform: uppercase;
    }

    .stat-val { font-size: 22px; font-weight: 800; color: #06b6d4 !important; }
    .stat-label { font-size: 9px; color: #94a3b8 !important; text-transform: uppercase; }

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
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΟΜΑΔΩΝ & ΣΗΜΑΙΕΣ ---
TEAMS = [
    {"n": "Mexico", "g": "A", "f": "mx"}, {"n": "South Africa", "g": "A", "f": "za"}, {"n": "South Korea", "g": "A", "f": "kr"}, {"n": "Czechia", "g": "A", "f": "cz"},
    {"n": "Canada", "g": "B", "f": "ca"}, {"n": "Bosnia and Herzegovina", "g": "B", "f": "ba"}, {"n": "Qatar", "g": "B", "f": "qa"}, {"n": "Switzerland", "g": "B", "f": "ch"},
    {"n": "Brazil", "g": "C", "f": "br"}, {"n": "Morocco", "g": "C", "f": "ma"}, {"n": "Haiti", "g": "C", "f": "ht"}, {"n": "Scotland", "g": "C", "f": "gb-sct"},
    {"n": "USA", "g": "D", "f": "us"}, {"n": "Paraguay", "g": "D", "f": "py"}, {"n": "Australia", "g": "D", "f": "au"}, {"n": "Turkey", "g": "D", "f": "tr"},
    {"n": "Germany", "g": "E", "f": "de"}, {"n": "Curacao", "g": "E", "f": "cw"}, {"n": "Ivory Coast", "g": "E", "f": "ci"}, {"n": "Ecuador", "g": "E", "f": "ec"},
    {"n": "Netherlands", "g": "F", "f": "nl"}, {"n": "Japan", "g": "F", "f": "jp"}, {"n": "Sweden", "g": "F", "f": "se"}, {"n": "Tunisia", "g": "F", "f": "tn"},
    {"n": "Belgium", "g": "G", "f": "be"}, {"n": "Egypt", "g": "G", "f": "eg"}, {"n": "Iran", "g": "G", "f": "ir"}, {"n": "New Zealand", "g": "G", "f": "nz"},
    {"n": "Spain", "g": "H", "f": "es"}, {"n": "Cape Verde", "g": "H", "f": "cv"}, {"n": "Saudi Arabia", "g": "H", "f": "sa"}, {"n": "Uruguay", "g": "H", "f": "uy"},
    {"n": "France", "g": "I", "f": "fr"}, {"n": "Senegal", "g": "I", "f": "sn"}, {"n": "Iraq", "g": "I", "f": "iq"}, {"n": "Norway", "g": "I", "f": "no"},
    {"n": "Argentina", "g": "J", "f": "ar"}, {"n": "Algeria", "g": "J", "f": "dz"}, {"n": "Austria", "g": "J", "f": "at"}, {"n": "Jordan", "g": "J", "f": "jo"},
    {"n": "Portugal", "g": "K", "f": "pt"}, {"n": "DR Congo", "g": "K", "f": "cd"}, {"n": "Uzbekistan", "g": "K", "f": "uz"}, {"n": "Colombia", "g": "K", "f": "co"},
    {"n": "England", "g": "L", "f": "gb-eng"}, {"n": "Croatia", "g": "L", "f": "hr"}, {"n": "Ghana", "g": "L", "f": "gh"}, {"n": "Panama", "g": "L", "f": "pa"}
]

# Helper function για URL σημαίας
def get_flag(name):
    code = next((t['f'] for t in TEAMS if t['n'] == name), "un")
    return f"https://flagcdn.com/w40/{code}.png"

RAW_MATCHES = [
    ["A", "11/06 22:00", "Estadio Azteca", "Mexico", "South Africa"],
    ["A", "12/06 05:00", "Estadio Akron", "South Korea", "Czechia"],
    ["B", "12/06 22:00", "BMO Field", "Canada", "Bosnia and Herzegovina"],
    ["D", "13/06 04:00", "SoFi Stadium", "USA", "Paraguay"],
    ["D", "14/06 07:00", "BC Place", "Australia", "Turkey"],
    ["B", "13/06 22:00", "Levi's Stadium", "Qatar", "Switzerland"],
    ["C", "14/06 01:00", "MetLife Stadium", "Brazil", "Morocco"],
    ["C", "14/06 04:00", "Gillette Stadium", "Haiti", "Scotland"],
    ["E", "14/06 20:00", "NRG Stadium", "Germany", "Curacao"],
    ["F", "14/06 23:00", "AT&T Stadium", "Netherlands", "Japan"],
    ["E", "15/06 02:00", "Lincoln Field", "Ivory Coast", "Ecuador"],
    ["F", "15/06 05:00", "Estadio BBVA", "Sweden", "Tunisia"],
    ["H", "15/06 19:00", "Mercedes-Benz", "Spain", "Cape Verde"],
    ["G", "15/06 22:00", "Lumen Field", "Belgium", "Egypt"],
    ["H", "16/06 01:00", "Hard Rock", "Saudi Arabia", "Uruguay"],
    ["G", "16/06 04:00", "SoFi Stadium", "Iran", "New Zealand"],
    ["J", "17/06 07:00", "Levi's Stadium", "Austria", "Jordan"],
    ["I", "16/06 10:00", "MetLife", "France", "Senegal"],
    ["I", "17/06 01:00", "Gillette", "Iraq", "Norway"],
    ["J", "17/06 04:00", "Arrowhead", "Argentina", "Algeria"],
    ["K", "17/06 08:00", "NRG Stadium", "Portugal", "DR Congo"],
    ["L", "17/06 11:00", "AT&T Stadium", "England", "Croatia"],
    ["L", "18/06 02:00", "BMO Field", "Ghana", "Panama"],
    ["K", "18/06 05:00", "Estadio Azteca", "Uzbekistan", "Colombia"],
    ["A", "18/06 07:00", "Mercedes-Benz", "Czechia", "South Africa"],
    ["B", "18/06 10:00", "SoFi Stadium", "Switzerland", "Bosnia and Herzegovina"],
    ["B", "19/06 01:00", "BC Place", "Canada", "Qatar"],
    ["A", "19/06 04:00", "Estadio Akron", "Mexico", "South Korea"],
    ["D", "20/06 06:00", "Levi's Stadium", "Turkey", "Paraguay"],
    ["D", "19/06 10:00", "Lumen Field", "USA", "Australia"],
    ["C", "20/06 01:00", "Gillette", "Scotland", "Morocco"],
    ["C", "20/06 03:30", "Lincoln Field", "Brazil", "Haiti"],
    ["F", "21/06 07:00", "Estadio BBVA", "Tunisia", "Japan"],
    ["F", "20/06 08:00", "NRG Stadium", "Netherlands", "Sweden"],
    ["E", "20/06 11:00", "BMO Field", "Germany", "Ivory Coast"],
    ["E", "21/06 03:00", "Arrowhead", "Ecuador", "Curacao"],
    ["H", "21/06 07:00", "Mercedes-Benz", "Spain", "Saudi Arabia"],
    ["G", "21/06 10:00", "SoFi Stadium", "Belgium", "Iran"],
    ["H", "22/06 01:00", "Hard Rock", "Uruguay", "Cape Verde"],
    ["G", "22/06 04:00", "BC Place", "New Zealand", "Egypt"],
    ["J", "22/06 08:00", "AT&T Stadium", "Argentina", "Austria"],
    ["I", "23/06 12:00", "Lincoln Field", "France", "Iraq"],
    ["I", "23/06 03:00", "MetLife", "Norway", "Senegal"],
    ["J", "23/06 06:00", "Levi's Stadium", "Jordan", "Algeria"],
    ["K", "23/06 08:00", "NRG Stadium", "Portugal", "Uzbekistan"],
    ["L", "23/06 11:00", "Gillette", "England", "Ghana"],
    ["L", "24/06 02:00", "BMO Field", "Panama", "Croatia"],
    ["K", "24/06 05:00", "Estadio Akron", "Colombia", "DR Congo"],
    ["B", "24/06 10:00", "BC Place", "Switzerland", "Canada"],
    ["B", "24/06 10:00", "Lumen Field", "Bosnia and Herzegovina", "Qatar"],
    ["C", "25/06 01:00", "Hard Rock Stadium", "Scotland", "Brazil"],
    ["C", "25/06 01:00", "Mercedes-Benz", "Morocco", "Haiti"],
    ["A", "25/06 04:00", "Estadio Azteca", "Czechia", "Mexico"],
    ["A", "25/06 04:00", "Estadio BBVA", "South Africa", "South Korea"],
    ["E", "25/06 11:00", "MetLife", "Ecuador", "Germany"],
    ["E", "25/06 11:00", "Lincoln Field", "Curacao", "Ivory Coast"],
    ["F", "26/06 02:00", "AT&T Stadium", "Japan", "Sweden"],
    ["F", "26/06 02:00", "Arrowhead", "Tunisia", "Netherlands"],
    ["D", "26/06 05:00", "SoFi Stadium", "Turkey", "USA"],
    ["D", "26/06 05:00", "Levi's Stadium", "Paraguay", "Australia"],
    ["I", "26/06 10:00", "Gillette", "Norway", "France"],
    ["I", "26/06 10:00", "BMO Field", "Senegal", "Iraq"],
    ["H", "27/06 03:00", "Estadio Akron", "Uruguay", "Spain"],
    ["H", "27/06 03:00", "NRG Stadium", "Cape Verde", "Saudi Arabia"],
    ["G", "27/06 06:00", "Lumen Field", "Egypt", "Iran"],
    ["G", "27/06 06:00", "BC Place"
