import streamlit as st
import numpy as np
import urllib.parse
import requests
import datetime

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
        time_anchor = f" [Current Time: {now.strftime('%I:%M %p')} Local Zone]"
        
        # Stitch compound query block parameters safely WITHOUT line breaks (\n)
        full_context = f"System Directives: {system_rules} {time_anchor} | "
        if file_data:
            full_context += f"{file_data} | "
        full_context += f"User Message: {user_query}"

        # FIXED: Explicitly strip out any line breaks to completely eliminate the invalid %0A code error!
        flat_context = full_context.replace("\n", " ").replace("\r", " ")

        # URL-encode the flat text string to pass it safely through the keyless endpoint
        encoded_text = urllib.parse.quote(flat_context)
        api_url = f"https://pollinations.ai{encoded_text}?model=searchgpt&jsonMode=false"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        res = requests.get(api_url, headers=headers, timeout=15, verify=False)
        if res.status_code == 200 and res.text:
            return res.text.strip()
            
        return "System engine cluster busy. Let's try sending that message again!"
    except Exception as e:
        return f"Operational loop interruption: {str(e)}"

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
        if 'uploaded_audio' in locals() and uploaded_audio:
            file_context += f" [Audio Track Sync Active: {uploaded_audio.name}]"

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🧠 System processing..."):
            ai_reply = get_live_ai_response(user_input, personality_choice, file_context)
            response_placeholder.markdown(ai_reply)
            
    st.session_state.chat_history.append(("assistant", ai_reply))
    st.rerun()
