import streamlit as st
import numpy as np
import urllib.parse
import json
import requests
import datetime

def get_live_ai_response(user_query, persona, file_data=""):
    try:
        if persona == "Creative Director":
            system_rules = "You are a world-class music video director and visual concept artist. Combine descriptions, uploaded media file references, and audio tempo characteristics to design stunning video concept storyboards, shot lists, and production paths."
        elif persona == "Fun & Sarcastic (Grok Mode)":
            system_rules = "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently, but you MUST give accurate real-time answers."
        else:
            system_rules = "You are a helpful, professional, and polite AI assistant. Give clean, straightforward answers."

        now = datetime.datetime.now()
        time_anchor = f" | Current Time: {now.strftime('%I:%M %p')} Local Zone"
        
        # Build completely flat context strings without any line breaks (\n) to prevent %0A crashes
        full_context = f"System Directives: {system_rules}{time_anchor} | "
        if file_data:
            full_context += f"{file_data} | "
        full_context += f"User Message: {user_query}"
        
        flat_context = full_context.replace("\n", " ").replace("\r", " ")

        # Gateway A: Connecting directly to Hugging Face serverless execution architecture
        api_url = "https://huggingface.co"
        payload = {
            "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_rules}{time_anchor}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{flat_context}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "parameters": {"max_new_tokens": 1024, "return_full_text": False}
        }
        
        res = requests.post(api_url, json=payload, timeout=8, verify=False)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                return data["generated_text"].strip()
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"].strip()
                
        # Gateway B: FIXED & Protected single-step URL fallback structure with accurate routing slashes
        encoded_query = urllib.parse.quote(flat_context)
        fallback_url = f"https://pollinations.ai{encoded_query}"
        
        fallback_res = requests.get(fallback_url, timeout=10, verify=False)
        if fallback_res.status_code == 200 and fallback_res.text:
            return fallback_res.text.strip()
            
        return "System cloud core busy. Please try clicking submission again!"
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
