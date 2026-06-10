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

# --- 2. ΔΕΔΟΜΕΝΑ ---
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
    ["C", "25/06 01:00", "Hard Rock", "Scotland", "Brazil"],
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
    ["G", "27/06 06:00", "BC Place", "New Zealand", "Belgium"],
    ["L", "28/06 12:00", "MetLife", "Panama", "England"],
    ["L", "28/06 12:00", "Lincoln Field", "Croatia", "Ghana"],
    ["K", "28/06 02:30", "Hard Rock", "Colombia", "Portugal"],
    ["K", "28/06 02:30", "Mercedes-Benz", "DR Congo", "Uzbekistan"],
    ["J", "28/06 05:00", "Arrowhead", "Algeria", "Austria"],
    ["J", "28/06 05:00", "AT&T Stadium", "Jordan", "Argentina"]
]

# --- 3. SESSION STATE ---
if 'wc_matches' not in st.session_state:
    matches = []
    for i, m_data in enumerate(RAW_MATCHES):
        matches.append({
            "id": i+1, "group": m_data[0], "dt": m_data[1], "st": m_data[2],
            "h": m_data[3], "a": m_data[4], "sh": None, "sa": None, "fin": False,
            "y_h": 0, "y_a": 0, "r_h": 0, "r_a": 0, "p_h": 0, "p_a": 0, "og_h": 0, "og_a": 0
        })
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
    if 'wc_matches' in st.session_state: del st.session_state['wc_matches']
    st.rerun()

@st.cache_data(ttl=3600)
def Μετράω_τα_κουκιά(model_id, prompt):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_id)
    return model.generate_content(prompt).text

# --- 5. HEADER ---
st.markdown("<h1>🏆 MUNDIAL 2026 PRO STATS PORTAL</h1>", unsafe_allow_html=True)
fin_m = [m for m in st.session_state.wc_matches if m['fin']]
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.markdown(f'<div class="stat-card"><div class="stat-val">{len(fin_m)}/72</div><div class="stat-label">Matches</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{sum(m["sh"]+m["sa"] for m in fin_m)}</div><div class="stat-label">⚽Goals</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#facc15!important">{sum(m["y_h"]+m["y_a"] for m in fin_m)}</div><div class="stat-label">🟨Yellow</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ef4444!important">{sum(m["r_h"]+m["r_a"] for m in fin_m)}</div><div class="stat-label">🟥Red</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#22d3ee!important">{sum(m["p_h"]+m["p_a"] for m in fin_m)}</div><div class="stat-label">🎯Pens</div></div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#fb923c!important">{sum(m["og_h"]+m["og_a"] for m in fin_m)}</div><div class="stat-label">⚠️OG</div></div>', unsafe_allow_html=True)

st.write("")
b1, b2 = st.columns([2, 1])
with b1: st.button("⚡ ΠΑΙΞΕ ΤΟ ΠΑΙΧΝΙΔΙ", on_click=auto_play, type="primary")
with b2: st.button("🔄 RESET TOURNAMENT", on_click=reset, type="secondary")

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
                <div style="font-size:9px; color:#94a3b8; text-align:center; border-top: 1px solid #1e293b; padding-top:4px;">
                    🟨 {m['y_h']}:{m['y_a']} | 🟥 {m['r_h']}:{m['r_a']} | 🎯 {m['p_h']}:{m['p_a']} | ⚠️ {m['og_h']}:{m['og_a']}
                </div>
                <div class="st-venue">📍 {m['st']}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("✏️ Επεξεργασία"):
                ch, ca = st.columns(2)
                sh_v = ch.number_input(f"Goals {m['h']}", 0, 15, m['sh'] if m['sh'] is not None else 0, key=f"sh{m['id']}")
                sa_v = ca.number_input(f"Goals {m['a']}", 0, 15, m['sa'] if m['sa'] is not None else 0, key=f"sa{m['id']}")
                yh_v = ch.slider(f"Yellow {m['h']}", 0, 10, m['y_h'], key=f"yh{m['id']}")
                ya_v = ca.slider(f"Yellow {m['a']}", 0, 10, m['y_a'], key=f"ya{m['id']}")
                rh_v = ch.checkbox(f"Red {m['h']}", value=bool(m['r_h']), key=f"rh{m['id']}")
                ra_v = ca.checkbox(f"Red {m['a']}", value=bool(m['r_a']), key=f"ra{m['id']}")
                if st.button("Save Result", key=f"btn{m['id']}"):
                    m.update({"sh": sh_v, "sa": sa_v, "fin": True, "y_h": yh_v, "y_a": ya_v, "r_h": int(rh_v), "r_a": int(ra_v)})
                    st.rerun()

with t2:
    GROUPS_L = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    cols_s = st.columns(3)
    for i, gId in enumerate(GROUPS_L):
        with cols_s[i % 3]:
            st.markdown(f"#### Group {gId}")
            g_teams = sorted(list(set([m['h'] for m in st.session_state.wc_matches if m['group'] == gId] + [m['a'] for m in st.session_state.wc_matches if m['group'] == gId])))
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
            st.table(pd.DataFrame(res).sort_values(by=["Pts", "GD"], ascending=False))

with t3:
    st.markdown("### 🔮 Ο ΚΟΝΤΟΣ ΠΡΟΤΕΙΝΕΙ")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            working_model = next((m for m in model_list if '1.5-flash' in m), model_list[0])
            
            all_teams_list = sorted(list(set([t['n'] for t in TEAMS])))
            c1, c2 = st.columns(2)
            h_t = c1.selectbox("Home Team", all_teams_list, key="sel_h")
            a_t = c2.selectbox("Away Team", all_teams_list, index=1, key="sel_a")
            
            # ΠΡΟΣΘΗΚΗ ΤΟΥ ΜΕΤΑΒΛΗΤΗΣ match_number ΠΟΥ ΕΛΕΙΠΕ
            match_no = st.number_input("Νούμερο Αγώνα (1-104):", 1, 104, 1)
            
            if st.button("ΠΑΤΑ ΝΑ ΠΛΗΡΩΘΕΙΣ", type="primary"):
                with st.spinner("Ο ΚΟΝΤΟΣ αναλύει φόρμα, προϊστορία και τακτική..."):
                    advanced_prompt = f"""
                    Είσαι ένας κορυφαίος αναλυτής ποδοσφαίρου και στατιστικολόγος με εξειδίκευση στο Παγκόσμιο Κύπελλο.
                    Κάνε μια βαθιά, επαγγελματική και τεχνική ανάλυση για τον αγώνα του Μουντιάλ 2026: {h_t} εναντίον {a_t}.

                    Η ανάλυσή σου ΠΡΕΠΕΙ να βασίζεται στα εξής πραγματικά στοιχεία:
                    1. Πρόσφατη Φόρμα (Τελευταίοι 10 επίσημοι αγώνες της κάθε ομάδας).
                    2. Προϊστορία σε Μουντιάλ.
                    3. Τακτική Προσέγγιση.
                    4. Ιστορικό αγώνα #{match_no} σε προηγούμενα Μουντιάλ.

                    Επίστρεψε την απάντηση αποκλειστικά στα Ελληνικά, χρησιμοποιώντας Markdown (bold, lists) για εύκολη ανάγνωση, με τις εξής ενότητες:
                    - 📊 **Πρόσφατη Φόρμα & Στατιστικά (Τελευταίοι 10 Αγώνες)**
                    - 📜 **Προϊστορία σε Μουντιάλ & Μεγάλα Τουρνουά**
                    - 🔮 **Πρόβλεψη Σκορ & Πιθανότητες Καρτών / Κόρνερ**
                    - 🎯 **Σύντομο Τακτικό Συμπέρασμα**
                    """
                    try:
                        result_text = Μετράω_τα_κουκιά(working_model, advanced_prompt)
                        st.markdown("---")
                        st.markdown(result_text)
                    except Exception as e:
                        if "429" in str(e): st.error("🚨 Όριο Google! Περίμενε 2 λεπτά.")
                        else: st.error(f"Σφάλμα: {e}")
        except Exception as e: st.error(f"Σφάλμα σύνδεσης: {e}")
    else: st.warning("Add API Key.")
