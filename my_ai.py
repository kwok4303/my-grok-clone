import streamlit as st
import numpy as np
import librosa
import urllib.parse
from ddgs import DDGS
from groq import Groq

# 1. CLOUD GATEWAY: Initialize the connection to the cloud brain infrastructure
# When you deploy publicly, Streamlit safely injects this password automatically!
api_key = st.secrets.get("GROQ_API_KEY", "")

def search_the_web(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if not results:
                return "No search results found."
            search_summary = ""
            for i, result in enumerate(results, 1):
                search_summary += f"[{i}] {result['title']}: {result['body']}\n"
            return search_summary
    except Exception:
        return "Failed to fetch live data."

def analyze_audio(audio_file):
    try:
        y, sr = librosa.load(audio_file, duration=30)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_val = float(tempo) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        return f"[Audio Analysis Success] Track Tempo: {tempo_val:.1f} BPM (Beats Per Minute)."
    except Exception:
        return "[Audio Note] Audio processed without parsing tempo data."

def generate_ai_photo(prompt_text):
    clean_text = "".join(c for c in prompt_text if c.isalnum() or c.isspace())
    words = clean_text.split()[:20]
    final_prompt = " ".join(words)
    encoded_prompt = urllib.parse.quote(final_prompt)
    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=576&model=flux&seed=42"
    return image_url

st.set_page_config(page_title="Grok Clone Studio", page_icon="🐦", layout="wide")

# Persistent short-term browser thread session states
if "threads" not in st.session_state:
    st.session_state.threads = {1: {"title": "Grok Core Node Chat", "messages": []}}
if "active_id" not in st.session_state:
    st.session_state.active_id = 1

# --- SIDEBAR COMPONENT ---
with st.sidebar:
    st.title("🐦 Grok-Style Terminal")
    
    if st.button("➕ New Conversation", use_container_width=True):
        new_id = max(st.session_state.threads.keys()) + 1
        st.session_state.threads[new_id] = {"title": f"Grok Thread {new_id}", "messages": []}
        st.session_state.active_id = new_id
        st.rerun()

    st.markdown("### 📁 Saved Archive Log Threads")
    for t_id in list(st.session_state.threads.keys()):
        t_title = st.session_state.threads[t_id]["title"]
        is_current = (t_id == st.session_state.active_id)
        btn_label = f"💬 {t_title}" if not is_current else f"👉 {t_title}"
        
        col_t, col_d = st.columns([0.8, 0.2])
        with col_t:
            if st.button(btn_label, key=f"th_{t_id}", use_container_width=True):
                st.session_state.active_id = t_id
                st.rerun()
        with col_d:
            if st.button("🗑️", key=f"del_{t_id}"):
                if len(st.session_state.threads) > 1:
                    del st.session_state.threads[t_id]
                    st.session_state.active_id = list(st.session_state.threads.keys())[0]
                else:
                    st.session_state.threads = {1: {"title": "Grok Core Node Chat", "messages": []}}
                    st.session_state.active_id = 1
                st.rerun()

    st.markdown("---")
    st.subheader("⚙️ System Directives")
    personality_choice = st.selectbox(
        "AI Operational Persona Profile Layout Selection Mapping Module:",
        ["Fun & Sarcastic (Grok Mode)", "Standard Assistant", "Creative Director"]
    )
    
    personality_prompts = {
        "Fun & Sarcastic (Grok Mode)": "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently or acting mildly annoyed by their text queries, but you MUST use provided live web search data to ultimately give highly accurate, specific real-time answers.",
        "Standard Assistant": "You are a helpful, professional assistant.",
        "Creative Director": "You are a world-class music video director. Combine media tracks and styles into video storyboards."
    }

    st.markdown("---")
    st.subheader("🖼️ Instant Image Rendering Studio")
    manual_img_prompt = st.text_input("Describe the picture to draw:", placeholder="e.g., cyber rebel looking at city...")
    if st.button("✨ Paint Frame"):
        if manual_img_prompt:
            with st.spinner("🎨 Generating concept sketch..."):
                img_link = generate_ai_photo(manual_img_prompt)
                st.image(img_link, caption="Generated Frame Layout", use_container_width=True)

# Main Application Frame Rendering
title_mappings = {
    "Fun & Sarcastic (Grok Mode)": "🐦 Grok Private Core Node Terminal",
    "Standard Assistant": "💬 General Chat Assistant Workspace",
    "Creative Director": "🎬 Multimedia Production Studio Studio Layout Canvas"
}
st.title(title_mappings[personality_choice])
st.caption(f"Active Thread Tracker Context ID: **#{st.session_state.active_id}**")

# Collapsible media components mapped directly into Creative Director layouts
if personality_choice == "Creative Director":
    with st.expander("📁 Open Media Upload Workspace (Images & Music Tracks)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            uploaded_files = st.file_uploader("📸 Mood board images:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"img_{st.session_state.active_id}")
            if uploaded_files:
                img_cols = st.columns(min(len(uploaded_files), 3))
                for idx, file in enumerate(uploaded_files):
                    img_cols[idx % 3].image(file, caption=file.name, use_container_width=True)
        with col2:
            uploaded_audio = st.file_uploader("🎵 MP3 Audio track:", type=["mp3"], key=f"aud_{st.session_state.active_id}", accept_multiple_files=False)
            if uploaded_audio:
                st.audio(uploaded_audio, format="audio/mp3")

st.markdown("---")

current_messages = st.session_state.threads[st.session_state.active_id]["messages"]
for msg in current_messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("Prompt Grok here...")

if user_input:
    if len(current_messages) == 0:
        st.session_state.threads[st.session_state.active_id]["title"] = user_input[:20]

    with st.chat_message("user"):
        st.markdown(user_input)
    
    current_messages.append({"role": "user", "content": user_input})

    media_audio_context = ""
    if personality_choice == "Creative Director" and 'uploaded_audio' in locals() and uploaded_audio:
        with st.spinner("🎵 Mapping wave metrics..."):
            media_audio_context = analyze_audio(uploaded_audio)

    media_file_context = ""
    if personality_choice == "Creative Director" and 'uploaded_files' in locals() and uploaded_files:
        names = ", ".join([f.name for f in uploaded_files])
        media_file_context = f"[Visual References Active]: {names}."

    time_keywords = ["latest", "news", "today", "current", "weather", "score", "who is", "what happened", "time", "date", "2025", "2026"]
    needs_internet = any(keyword in user_input.lower() for keyword in time_keywords)

    final_text_prompt = user_input
    if media_audio_context:
        final_text_prompt = f"{media_audio_context}\n\n{final_text_prompt}"
    if media_file_context:
        final_text_prompt = f"{media_file_context}\n\n{final_text_prompt}"
    if needs_internet:
        with st.spinner("🔍 Querying live data networks..."):
            web_data = search_the_web(user_input)
            final_text_prompt = f"Current Live Web Search Results:\n{web_data}\n\nUser Question: {final_text_prompt}"

    system_rule = {"role": "system", "content": personality_prompts[personality_choice]}
    
    # Format messages array correctly to comply with cloud server parameters
    formatted_history = []
    for msg in current_messages[:-1]:
        formatted_history.append({"role": msg["role"], "content": msg["content"]})
    formatted_history.append({"role": "user", "content": final_text_prompt})
    
    run_messages = [system_rule] + formatted_history

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        if not api_key:
            st.error("🔒 Groq API Key Missing! Go to the sidebar control deck layout configurations or set up Streamlit secrets parameters.")
        else:
            try:
                # Connected securely to Groq's high-speed cloud cluster framework using the elite Llama 3.3 70B brain!
                client = Groq(api_key=api_key)
                response_stream = client.chat.completions.create(
                    model='llama-3.3-70b-specdec',
                    messages=run_messages,
                    stream=True
                )
                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Cloud Engine Pipeline Connection Interrupted: {str(e)}")
        
    if full_response:
        current_messages.append({"role": "assistant", "content": full_response})
    st.rerun()
