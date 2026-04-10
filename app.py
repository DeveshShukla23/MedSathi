import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("AIzaSyBypHzpWbmVCbQsWqYvem2jgU-9vOgkBBI")
client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="MedSathi - AI Health Assistant",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
* { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0a0a 0%, #0d1f0d 50%, #0a0a0a 100%); }
.typing-title {
    color: white; font-size: 2.8rem; font-weight: 800;
    overflow: hidden; white-space: nowrap; margin: 0 auto;
    animation: typing 2.5s steps(8, end); display: inline-block;
}
@keyframes typing { from { width: 0; } to { width: 100%; } }
.main-header {
    background: linear-gradient(135deg, #1a6b3c, #2ecc71);
    padding: 30px; border-radius: 20px; text-align: center;
    margin-bottom: 20px; animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { box-shadow: 0 0 20px rgba(46,204,113,0.3); }
    to   { box-shadow: 0 0 50px rgba(46,204,113,0.8); }
}
.main-header p { color: #d4f5e2; font-size: 0.95rem; margin: 5px 0 0 0; }
.logo-float { animation: float 3s ease-in-out infinite; display: inline-block; font-size: 3rem; }
@keyframes float {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071a07 0%, #0a0a0a 100%) !important;
    border-right: 1px solid rgba(46,204,113,0.3) !important;
}
.sidebar-logo { text-align: center; padding: 20px 0; }
.sidebar-logo-icon { font-size: 4rem; animation: float 3s ease-in-out infinite, pulse-green 2s ease-in-out infinite; }
@keyframes pulse-green {
    0%   { filter: drop-shadow(0 0 5px rgba(46,204,113,0.5)); }
    50%  { filter: drop-shadow(0 0 20px rgba(46,204,113,1)); }
    100% { filter: drop-shadow(0 0 5px rgba(46,204,113,0.5)); }
}
.sidebar-title {
    color: #2ecc71; font-size: 1.6rem; font-weight: 800;
    text-align: center; margin: 5px 0;
    animation: glow-text 2s ease-in-out infinite alternate;
}
@keyframes glow-text {
    from { text-shadow: 0 0 5px rgba(46,204,113,0.5); }
    to   { text-shadow: 0 0 20px rgba(46,204,113,1); }
}
.sidebar-subtitle { color: #888; font-size: 0.75rem; text-align: center; margin-bottom: 15px; }
.stats-box {
    background: linear-gradient(135deg, rgba(46,204,113,0.1), rgba(26,107,60,0.2));
    border: 1px solid rgba(46,204,113,0.4); border-radius: 15px;
    padding: 15px 10px; text-align: center; margin: 5px 0; transition: all 0.3s ease;
}
.stats-box:hover { transform: translateY(-3px); border-color: #2ecc71; box-shadow: 0 5px 20px rgba(46,204,113,0.3); }
.stats-number { color: #2ecc71; font-size: 2rem; font-weight: 700; }
.stats-label  { color: #aaa; font-size: 0.72rem; margin-top: 2px; }
.feature-badge {
    background: rgba(46,204,113,0.1); border: 1px solid rgba(46,204,113,0.3);
    border-radius: 20px; padding: 6px 12px; font-size: 0.75rem;
    color: #2ecc71; margin: 4px 2px; display: inline-block;
}
.emergency-box {
    background: linear-gradient(135deg, rgba(231,76,60,0.2), rgba(192,57,43,0.1));
    border: 2px solid #e74c3c; border-radius: 15px; padding: 15px; margin: 10px 0;
    animation: pulse-red 1.5s ease-in-out infinite;
}
@keyframes pulse-red {
    0%   { box-shadow: 0 0 0 0 rgba(231,76,60,0.4); }
    70%  { box-shadow: 0 0 0 10px rgba(231,76,60,0); }
    100% { box-shadow: 0 0 0 0 rgba(231,76,60,0); }
}
.disclaimer {
    background: rgba(243,156,18,0.1); border-left: 4px solid #f39c12;
    padding: 12px 16px; border-radius: 10px; color: #f39c12;
    font-size: 0.82rem; margin-bottom: 15px;
}
.stButton > button {
    background: linear-gradient(135deg, #1a3a2a, #1e4d35) !important;
    color: #2ecc71 !important; border: 1px solid #2ecc71 !important;
    border-radius: 25px !important; padding: 8px 16px !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    transition: all 0.3s ease !important; width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
    color: #000 !important; transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(46,204,113,0.4) !important;
}
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important; border-radius: 15px !important;
    padding: 10px !important; margin: 5px 0 !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
}
.stChatInput > div {
    border: 2px solid #2ecc71 !important; border-radius: 25px !important;
    background: rgba(26,58,42,0.3) !important;
}
.stSelectbox > div > div {
    background: rgba(26,58,42,0.5) !important;
    border: 1px solid #2ecc71 !important; border-radius: 10px !important;
}
.symptom-header { color: #2ecc71; font-size: 1rem; font-weight: 600; margin: 10px 0; }
.powered-bar {
    background: linear-gradient(90deg, #1a6b3c, #2ecc71, #1a6b3c);
    background-size: 200% auto; height: 3px; border-radius: 3px;
    animation: shimmer 2s linear infinite; margin: 10px 0;
}
@keyframes shimmer { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🏥</div>
        <div class="sidebar-title">MedSathi</div>
        <div class="sidebar-subtitle">AI Health Assistant</div>
    </div>
    <div class="powered-bar"></div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Stats")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">6+</div>
            <div class="stats-label">Symptoms</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">2</div>
            <div class="stats-label">Languages</div>
        </div>""", unsafe_allow_html=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">24/7</div>
            <div class="stats-label">Available</div>
        </div>""", unsafe_allow_html=True)
    with col_d:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">🆓</div>
            <div class="stats-label">Free</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✨ Features")
    st.markdown("""
    <div>
        <span class="feature-badge">🤖 Gemma 3 AI</span>
        <span class="feature-badge">🌐 Bilingual</span>
        <span class="feature-badge">🚨 Emergency</span>
        <span class="feature-badge">⚡ Instant</span>
        <span class="feature-badge">🔒 Private</span>
        <span class="feature-badge">📱 Mobile</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    <small style='color:#888'>
    MedSathi uses <b style='color:#2ecc71'>Gemma 3</b> by Google
    to provide health guidance to rural communities.<br><br>
    Built for <b style='color:#2ecc71'>Gemma 3 Good Hackathon 2025</b>
    </small>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚨 Emergency Numbers")
    st.markdown("""
    <div style='background:rgba(231,76,60,0.15); border:1px solid #e74c3c;
    border-radius:10px; padding:12px; font-size:0.82rem; color:#e74c3c'>
    🚑 <b>Ambulance:</b> 108<br>
    🏥 <b>Health Helpline:</b> 104<br>
    👮 <b>Police:</b> 100<br>
    👩‍⚕️ <b>Women Helpline:</b> 1091
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center'>
        <small style='color:#555'>Made with ❤️ for Rural India</small><br>
        <small style='color:#2ecc71'>by Devesh Shukla</small>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN HEADER ───
st.markdown("""
<div class="main-header">
    <div class="logo-float">🏥</div>
    <div class="typing-title">MedSathi</div>
    <p>AI Health Assistant for Rural India | ग्रामीण भारत के लिए AI स्वास्थ्य सहायक</p>
</div>
""", unsafe_allow_html=True)

# ─── DISCLAIMER ───
st.markdown("""
<div class="disclaimer">
⚠️ <b>Disclaimer:</b> MedSathi provides general health guidance only.
Always consult a qualified doctor for medical advice.
</div>
""", unsafe_allow_html=True)

# ─── LANGUAGE + CLEAR ───
col_lang, col_clear = st.columns([3, 1])
with col_lang:
    lang = st.selectbox("🌐 Choose Language / भाषा चुनें", ["English", "Hindi"])
with col_clear:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── SYMPTOM BUTTONS ───
st.markdown('<p class="symptom-header">🔍 Common Symptoms / सामान्य लक्षण</p>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🤒 Fever / बुखार"):
        st.session_state.messages.append({"role": "user", "content": "I have high fever"})
with col2:
    if st.button("🤕 Headache / सिरदर्द"):
        st.session_state.messages.append({"role": "user", "content": "I have severe headache"})
with col3:
    if st.button("🤢 Vomiting / उल्टी"):
        st.session_state.messages.append({"role": "user", "content": "I have nausea and vomiting"})

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("😮‍💨 Cough / खांसी"):
        st.session_state.messages.append({"role": "user", "content": "I have dry cough"})
with col5:
    if st.button("🩸 Diabetes / मधुमेह"):
        st.session_state.messages.append({"role": "user", "content": "I have diabetes symptoms"})
with col6:
    if st.button("💊 BP / रक्तचाप"):
        st.session_state.messages.append({"role": "user", "content": "I have high blood pressure"})

st.markdown("---")

# ─── CHAT ───
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Apne symptoms likho... / Type your symptoms...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

if (len(st.session_state.messages) > 0 and
        st.session_state.messages[-1]["role"] == "user"):

    if lang == "Hindi":
        system_prompt = """You are MedSathi — a friendly AI health assistant for rural India.
Always respond in simple Hindi using Devanagari script only. No English words.
Format:
🔍 संभावित कारण: (1-2 simple reasons)
🏠 घर पर करें: (2-3 simple steps)
🚨 डॉक्टर के पास जाएं अगर: (warning signs)
👨‍⚕️ कृपया एक डॉक्टर से ज़रूर मिलें।
If chest pain or breathing difficulty: start with 🚨 आपातकाल: तुरंत अस्पताल जाएं!
Never give confirmed diagnosis."""
    else:
        system_prompt = """You are MedSathi — a friendly AI health assistant for rural India.
Use very simple English. Short sentences. No medical jargon.
Format:
🔍 What you might have: (1-2 simple possibilities)
🏠 What to do at home: (2-3 simple steps)
🚨 Go to doctor immediately if: (warning signs)
👨‍⚕️ Please visit a doctor for proper treatment.
If chest pain or breathing difficulty: start with 🚨 EMERGENCY: Call 108 or go to hospital immediately!
Never give confirmed diagnosis."""

    full_prompt = system_prompt + "\n\nUser: " + st.session_state.messages[-1]["content"]

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_reply = ""

        with st.spinner("MedSathi soch raha hai... 🤔"):
            response = client.models.generate_content(
                model="gemma-3-4b-it",
                contents=full_prompt
            )

        words = response.text.split(" ")
        for word in words:
            full_reply += word + " "
            message_placeholder.markdown(full_reply)
            time.sleep(0.05)

        message_placeholder.markdown(full_reply)

    reply = full_reply

    if any(word in reply.upper() for word in ["EMERGENCY", "AMBULANCE", "आपातकाल"]):
        st.markdown(f"""
        <div class="emergency-box">
            🚨 <b style='color:#e74c3c'>EMERGENCY ALERT</b><br>
            <span style='color:#fff'>{reply}</span>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})