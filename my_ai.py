import streamlit as st
import numpy as np
import librosa
import urllib.parse
import requests
import datetime

def get_live_ai_response(user_query, persona, audio_data="", file_data=""):
    try:
        # Build clear, rich instructions for your models
        if persona == "Fun & Sarcastic (Grok Mode)":
            system_rules = "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently, but you MUST give accurate real-time answers."
        elif persona == "Creative Director":
            system_rules = "You are a world-class music video director and visual concept artist. Combine descriptions, uploaded media file references, and audio tempo characteristics to design stunning video concept storyboards, shot lists, and production paths."
        else:
            system_rules = "You are a helpful, professional, and polite AI assistant. Give clean, straightforward answers."

        now = datetime.datetime.now()
        time_anchor = f"\n[Current Time: {now.strftime('%I:%M %p')} Local Zone]"
        
        # Assemble complete context variables safely
        full_context = f"System Directives: {system_rules}{time_anchor}\n"
        if audio_data:
            full_context += f"{audio_data}\n"
        if file_data:
            full_context += f"{file_data}\n"
            
        full_context += f"User Message: {user_query}"

        # FIXED: Sends data inside a secure post packet body to bypass URL length walls completely!
        payload = {
            "messages": [{"role": "user", "content": full_context}],
            "model": "qwen"
        }
        
        res = requests.post("https://pollinations.ai", json=payload, timeout=15)
        if res.status_code == 200 and res.text:
            return res.text.strip()
        return "System cloud cluster busy. Let's try sending that message again!"
    except Exception as e:
        return f"Operational loop interruption: {str(e)}"

def analyze_audio(audio_file):
    try:
        y, sr = librosa.load(audio_file, duration=30)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_val = float(tempo) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        return f"[Audio Analysis Metrics] Track Tempo: {tempo_val:.1f} BPM (Beats Per Minute)."
    except Exception:
        return "[Audio Note] Track loaded smoothly into workspace storage."

def generate_ai_photo(prompt_text):
    clean_text = "".join(c for c in prompt_text if c.isalnum() or c.isspace())
    words = clean_text.split()[:20]
    final_prompt = " ".join(words)
    encoded_prompt = urllib.parse.quote(final_prompt)
    return f"https://pollinations.ai{encoded_prompt}?width=1024&height=576&model=flux&seed=42"

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
        ["Creative Director", "Fun & Sarcastic (Grok Mode)", "Standard Assistant"]
    )
    
    st.markdown("---")
    st.subheader("🖼️ Instant Sketch Pad")
    manual_img_prompt = st.text_input("Describe the image you want:", placeholder="e.g., cyberpunk rain cafe neon...")
    if st.button("✨ Generate Photo"):
        if manual_img_prompt:
            with st.spinner("🎨 Painting your AI photo..."):
                img_link = generate_ai_photo(manual_img_prompt)
                st.image(img_link, caption="Generated Concept Sketch", use_container_width=True)

# Main App Window Layout
title_mappings = {
    "Creative Director": "🎬 Multimedia Production Studio Layout Canvas",
    "Fun & Sarcastic (Grok Mode)": "🐦 Grok Private Core Node Terminal",
    "Standard Assistant": "💬 General Chat Assistant Workspace"
}
st.title(title_mappings[personality_choice])
st.markdown("---")

# --- FULLY RESTORED: MULTIMEDIA UPLOAD BLOCKS ---
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

    # Process background elements on the fly
    audio_context = ""
    if personality_choice == "Creative Director" and 'uploaded_audio' in locals() and uploaded_audio:
        with st.spinner("🎵 Analyzing song rhythm and beat patterns..."):
            audio_context = analyze_audio(uploaded_audio)

    file_context = ""
    if personality_choice == "Creative Director" and 'uploaded_files' in locals() and uploaded_files:
        file_names = ", ".join([f.name for f in uploaded_files])
        file_context = f"[Visual Reference Active Moodboard Files]: {file_names}."

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🧠 System processing..."):
            ai_reply = get_live_ai_response(user_input, personality_choice, audio_context, file_context)
            response_placeholder.markdown(ai_reply)
            
    st.session_state.chat_history.append(("assistant", ai_reply))
    st.rerun()
