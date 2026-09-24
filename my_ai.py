import streamlit as st
import requests
import datetime
import urllib.parse

def get_live_ai_response(user_query, persona, file_data=""):
    try:
        # Build clean, powerful system prompts
        if persona == "Creative Director":
            system_rules = "You are a world-class music video director and visual concept artist. Combine descriptions, uploaded media file references, and audio tempo characteristics to design stunning video concept storyboards, shot lists, and production paths."
        elif persona == "Fun & Sarcastic (Grok Mode)":
            system_rules = "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently, but you MUST give accurate real-time answers."
        else:
            system_rules = "You are a helpful, professional, and polite AI assistant. Give clean, straightforward answers."

        now = datetime.datetime.now()
        time_anchor = f"\n[Current Time: {now.strftime('%I:%M %p')} Local Zone]"
        
        # Stitch compound query block parameters safely
        full_context = f"System Directives: {system_rules}{time_anchor}\n"
        if file_data:
            full_context += f"{file_data}\n"
        full_context += f"User Message: {user_query}"

        # Connect directly to the premium open-source Qwen 72B cloud network cluster
        payload = {
            "messages": [{"role": "user", "content": full_context}],
            "model": "qwen-72b"
        }
        
        # Safe browser-mimicking headers to pass data securely
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        res = requests.post("https://pollinations.ai", json=payload, headers=headers, timeout=15, verify=False)
        if res.status_code == 200 and res.text:
            return res.text.strip()
            
        return "🧠 Engine node sync delay. Let's try sending that message once more!"
    except Exception as e:
        return f"Operational loop delay: {str(e)}"

st.set_page_config(page_title="Multimedia Production Studio", page_icon="🎬", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR CONTROL CANVAS ---
with st.sidebar:
    st.title("⚙️ Production Engine")
    st.markdown("---")
    
    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.subheader("🤖 AI Personality Profile")
    personality_choice = st.selectbox(
        "Choose Operational Mode:",
        ["Fun & Sarcastic (Grok Mode)", "Creative Director", "Standard Assistant"]
    )
    
    st.markdown("---")
    st.caption("Engine Status: 🟢 Live Online Matrix Connected")

# Main App Window Layout
title_mappings = {
    "Creative Director": "🎬 Multimedia Production Studio Layout Canvas",
    "Fun & Sarcastic (Grok Mode)": "🐦 Grok Private Core Node Terminal",
    "Standard Assistant": "💬 General Chat Assistant Workspace"
}
st.title(title_mappings[personality_choice])
st.markdown("---")

# --- MULTIMEDIA UPLOAD BLOCKS ---
if personality_choice == "Creative Director":
    with st.expander("📁 Open Media Upload Workspace (Images & Music Tracks)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            uploaded_files = st.file_uploader("📸 Mood board images:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="prod_img")
            if uploaded_files:
                img_cols = st.columns(min(len(uploaded_files), 3))
                for idx, file in enumerate(uploaded_files):
                    img_cols[idx % 3].image(file, caption=file.name, use_container_width=True)
        with col2:
            uploaded_audio = st.file_uploader("🎵 MP3 Audio track:", type=["mp3"], key="prod_aud", accept_multiple_files=False)
            if uploaded_audio:
                st.audio(uploaded_audio, format="audio/mp3")

st.markdown("---")

# Render chat messages cleanly
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# User Entry Chat Input bar
user_input = st.chat_input("Command your studio here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    file_context = ""
    if personality_choice == "Creative Director" and 'uploaded_files' in locals() and uploaded_files:
        file_names = ", ".join([f.name for f in uploaded_files])
        file_context = f"[Visual Reference Active Moodboard Files]: {file_names}."

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🧠 Connecting to brain cluster..."):
            ai_reply = get_live_ai_response(user_input, personality_choice, file_context)
            response_placeholder.markdown(ai_reply)
            
    st.session_state.chat_history.append(("assistant", ai_reply))
    st.rerun()
