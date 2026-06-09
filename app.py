import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import os

# --- 1. CONFIG & COSMIC SLATE THEME (CSS) ---
st.set_page_config(page_title="Mundial 2026 Pro Portal", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Dashboard Stats Cards */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }
    .stat-card:hover { border-color: #58a6ff; }
    .stat-val { font-size: 28px; font-weight: bold; color: #58a6ff; }
    .stat-label { font-size: 12px; color: #8b949e; text-transform: uppercase; }

    /* Match Cards */
    .match-box {
        background: #1c2128;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #238636;
    }
    
    /* Qualifiers Highlight */
    .qualified { border: 2px solid #238636 !important; background: rgba(35, 134, 54, 0.1) !important; }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #8b949e;
    }
    .stTabs [data-baseweb="tab--active"] { border-color: #58a6ff; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ΔΕΔΟΜΕΝΑ ΔΙΟΡΓΑΝΩΣΗΣ (48 ΟΜΑΔΕΣ - 12 ΟΜΙΛΟΙ) ---
GROUPS = {
    "Όμιλος A": ["Καναδάς", "Ελλάδα 🇬🇷", "Νιγηρία", "Αυστρία"],
    "Όμιλος B": ["Μεξικό", "Ιταλία", "Νότια Κορέα", "Ισημερινός"],
    "Όμιλος C": ["ΗΠΑ", "Πορτογαλία", "Ιράν", "Καμερούν"],
    "Όμιλος D": ["Αργεντινή", "Δανία", "Σαουδική Αραβία", "Παναμάς"],
    "Όμιλος E": ["Βραζιλία", "Σερβία", "Τυνησία", "Περού"],
    "Όμιλος F": ["Γαλλία", "Αυστραλία", "Τουρκία", "Τζαμάικα"],
    "Όμιλος G": ["Ισπανία", "Ιαπωνία", "Αίγυπτος", "Σκωτία"],
    "Όμιλος H": ["Γερμανία", "Ουρουγουάη", "Ουζμπεκιστάν", "Ονδούρα"],
    "Όμιλος I": ["Αγγλία", "Κολομβία", "Μάλι", "Νέα Ζηλανδία"],
    "Όμιλος J": ["Βέλγιο", "Παραγουάη", "Ιράκ", "Σλοβενία"],
    "Όμιλος K": ["Ολλανδία", "Χιλή", "Γκάνα", "Κατάρ"],
    "Όμιλος L": ["Κροατία", "Ελβετία", "Κίνα", "Κόστα Ρίκα"]
}

# --- 3. SESSION STATE (DATABASE ΤΗΣ ΕΦΑΡΜΟΓΗΣ) ---
if 'matches' not in st.session_state:
    matches = []
    for g_name, teams in GROUPS.items():
        # Δημιουργία 3 αγωνιστικών ανά όμιλο
        matches.append({"group": g_name, "home": teams[0], "away": teams[1], "score_h": 0, "score_a": 0, "played": False, "cards": 0, "penalties": 0})
        matches.append({"group": g_name, "home": teams[2], "away": teams[3], "score_h": 0, "score_a": 0, "played": False, "cards": 0, "penalties": 0})
        matches.append({"group": g_name, "home": teams[0], "away": teams[2], "score_h": 0, "score_a": 0, "played": False, "cards": 0, "penalties": 0})
        matches.append({"group": g_name, "home": teams[1], "away": teams[3], "score_h": 0, "score_a": 0, "played": False, "cards": 0, "penalties": 0})
    st.session_state.matches = matches

# --- 4. ΣΥΝΑΡΤΗΣΕΙΣ ΛΟΓΙΚΗΣ ---
def reset_tournament():
    for m in st.session_state.matches:
        m['score_h'], m['score_a'], m['played'], m['cards'], m['penalties'] = 0, 0, False, 0, 0
    st.rerun()

def auto_play():
    for m in st.session_state.matches:
        m['score_h'] = random.randint(0, 4)
        m['score_a'] = random.randint(0, 4)
        m['cards'] = random.randint(0, 5)
        m['penalties'] = random.choice([0, 0, 0, 1])
        m['played'] = True
    st.rerun()

# --- 5. HEADER DASHBOARD ---
total_goals = sum(m['score_h'] + m['score_a'] for m in st.session_state.matches if m['played'])
total_cards = sum(m['cards'] for m in st.session_state.matches if m['played'])
total_played = sum(1 for m in st.session_state.matches if m['played'])

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="stat-card"><div class="stat-val">{total_played}/72</div><div class="stat-label">Αγώνες</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="stat-card"><div class="stat-val">{total_goals}</div><div class="stat-label">Συνολικά Γκολ</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="stat-card"><div class="stat-val">{total_cards}</div><div class="stat-label">Κίτρινες Κάρτες</div></div>', unsafe_allow_html=True)
c4.button("⚡ Auto-Play Simulator", on_click=auto_play, use_container_width=True)
st.button("🔄 Επαναφορά", on_click=reset_tournament)

# --- 6. ΚΥΡΙΟ ΜΕΝΟΥ (TABS) ---
tabs = st.tabs(["📅 Ημερολόγιο", "📊 Βαθμολογίες", "🧠 AI Προβλέψεις", "🏟️ Στάδια"])

with tabs[0]:
    st.subheader("Πρόγραμμα Αγώνων (72 Παιχνίδια)")
    sel_group = st.selectbox("Φιλτράρισμα ανά Όμιλο:", ["Όλοι"] + list(GROUPS.keys()))
    
    for i, m in enumerate(st.session_state.matches):
        if sel_group == "Όλοι" or m['group'] == sel_group:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                col1.write(f"**{m['home']}**")
                h_sc = col2.number_input("H", 0, 10, m['score_h'], key=f"h{i}")
                a_sc = col3.number_input("A", 0, 10, m['score_a'], key=f"a{i}")
                col4.write(f"**{m['away']}**")
                if h_sc != m['score_h'] or a_sc != m['score_a']:
                    st.session_state.matches[i].update({"score_h": h_sc, "score_a": a_sc, "played": True})
                    st.rerun()

with tabs[1]:
    st.subheader("Tournament Standings (Live)")
    cols = st.columns(3)
    for idx, (g_name, teams) in enumerate(GROUPS.items()):
        with cols[idx % 3]:
            st.write(f"### {g_name}")
            # Υπολογισμός βαθμολογίας
            table = []
            for t in teams:
                stats = {"Ομάδα": t, "Αγ": 0, "Ν": 0, "Ι": 0, "Η": 0, "Γκολ": 0, "ΔΤ": 0, "Β": 0}
                for m in st.session_state.matches:
                    if m['played'] and (m['home'] == t or m['away'] == t):
                        stats["Αγ"] += 1
                        h, a = m['score_h'], m['score_a']
                        if m['home'] == t:
                            stats["Γκολ"] += h
                            stats["ΔΤ"] += (h - a)
                            if h > a: stats["Ν"], stats["Β"] = stats["Ν"]+1, stats["Β"]+3
                            elif h == a: stats["Ι"], stats["Β"] = stats["Ι"]+1, stats["Β"]+1
                            else: stats["Η"] += 1
                        else:
                            stats["Γκολ"] += a
                            stats["ΔΤ"] += (a - h)
                            if a > h: stats["Ν"], stats["Β"] = stats["Ν"]+1, stats["Β"]+3
                            elif a == h: stats["Ι"], stats["Β"] = stats["Ι"]+1, stats["Β"]+1
                            else: stats["Η"] += 1
                table.append(stats)
            
            df = pd.DataFrame(table).sort_values(by=["Β", "ΔΤ", "Γκολ"], ascending=False)
            st.dataframe(df, hide_index=True)

with tabs[2]:
    st.subheader("🧠 Gemini AI Score Predictor")
    t1 = st.selectbox("Ομάδα 1:", [t for sub in GROUPS.values() for t in sub], index=0)
    t2 = st.selectbox("Ομάδα 2:", [t for sub in GROUPS.values() for t in sub], index=1)
    
    if st.button("Λήψη Πρόβλεψης"):
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Κάνε μια επαγγελματική πρόβλεψη σκορ για το Μουντιάλ 2026: {t1} vs {t2}. Δώσε σκορ, σκόρερ και τακτική ανάλυση στα Ελληνικά."
            response = model.generate_content(prompt)
            st.info(response.text)
        else: st.error("Λείπει το API Key!")

with tabs[3]:
    st.subheader("🏟️ Επίσημα Στάδια 2026")
    st.write("1. **MetLife Stadium** - New York (82,500)")
    st.write("2. **Estadio Azteca** - Mexico City (87,500)")
    st.write("3. **BC Place** - Vancouver (54,500)")
