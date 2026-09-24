import streamlit as st
import numpy as np
import urllib.parse
import requests
import datetime

def search_the_web_live(query):
    try:
        low_q = query.lower()
        if "time" in low_q or "date" in low_q or "today" in low_q or "now" in low_q or "lagos" in low_q:
            # Nigeria's current time offset: UTC+1 hour zone tracker layout
            res = requests.get("https://wttr.in", timeout=5)
            if res.status_code == 200:
                return f"[Live Web Search Success] Current Timestamp Metrics: {res.text.strip()}"
        
        encoded = urllib.parse.quote(query)
        res = requests.get(f"https://pollinations.ai{encoded}", timeout=5)
        if res.status_code == 200 and len(res.text.strip()) > 10:
            return f"[Live Web Search Results Summary]:\n{res.text[:600]}"
        return "Live data lookups complete. Processing response query rules."
    except Exception:
        now = datetime.datetime.now() + datetime.timedelta(hours=1)
        return f"[Live Server Time Backup]: {now.strftime('%Y-%m-%d %H:%M:%S')} (Lagos Time)"

def generate_ai_photo(prompt_text):
    clean_text = "".join(c for c in prompt_text if c.isalnum() or c.isspace())
    words = clean_text.split()[:20]
    final_prompt = " ".join(words)
    encoded_prompt = urllib.parse.quote(final_prompt)
    return f"https://pollinations.ai{encoded_prompt}?width=1024&height=576&model=flux&seed=42"

st.set_page_config(page_title="Grok Clone Studio", page_icon="🐦", layout="wide")

# Simple, crash-proof storage engine layout structure
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR COMPONENT ---
with st.sidebar:
    st.title("🐦 Grok-Style Terminal")
    
    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.subheader("⚙️ System Directives")
    personality_choice = st.selectbox(
        "AI Personality Mode:",
        ["Fun & Sarcastic (Grok Mode)", "Standard Assistant"]
    )
    
    st.markdown("---")
    st.subheader("🖼️ Instant Image Studio")
    manual_img_prompt = st.text_input("Describe the picture to draw:", placeholder="e.g., cyber rebel looking at city...")
    if st.button("✨ Paint Frame"):
        if manual_img_prompt:
            with st.spinner("🎨 Generating concept sketch..."):
                img_link = generate_ai_photo(manual_img_prompt)
                st.image(img_link, caption="Generated Frame Layout", use_container_width=True)

# Main Application Window title parameters
st.title("🐦 Grok Private Core Node Terminal" if personality_choice == "Fun & Sarcastic (Grok Mode)" else "💬 General Chat Assistant Workspace")
st.markdown("---")

# Render historical chats cleanly from global stack lists
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# User Entry Window Box
user_input = st.chat_input("Prompt Grok here...")

if user_input:
    # Display query on screen instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Process search injection triggers
    time_keywords = ["latest", "news", "today", "current", "weather", "score", "who is", "what happened", "time", "date", "2025", "2026", "lagos"]
    needs_internet = any(k in user_input.lower() for k in time_keywords)

    final_prompt = user_input
    if needs_internet:
        with st.spinner("🔍 Accessing live cloud indices..."):
            web_data = search_the_web_live(user_input)
            final_prompt = f"Current Live Web Search Data Context:\n{web_data}\n\nUser Question: {final_prompt}"

    # Build clear system routing prompts context layout arrays
    system_instruction = (
        "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently or acting mildly annoyed, but you MUST use provided live web search data data timestamps to ultimately give a highly accurate real-time answer."
        if personality_choice == "Fun & Sarcastic (Grok Mode)"
        else "You are a helpful, professional, and polite assistant. Give straightforward, direct, and clean answers based on the user's questions."
    )

    # Compile the final query text string safely passed to cloud cores
    prompt_payload = f"System Context rules: {system_instruction}\n\n"
    for role, text in st.session_state.chat_history[:-1]:
        prompt_payload += f"{role.upper()}: {text}\n"
    prompt_payload += f"USER: {final_prompt}\nASSISTANT:"

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("🧠 System routing..."):
            try:
                # Direct lookup payload transmission using standard open-source API format
                payload = {
                    "messages": [{"role": "user", "content": prompt_payload}],
                    "model": "qwen"
                }
                res = requests.post("https://pollinations.ai", json=payload, timeout=15)
                
                if res.status_code == 200 and res.text:
                    full_response = res.text.strip()
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append(("assistant", full_response))
                else:
                    st.error("Cloud processing pipeline node busy. Please try again.")
            except Exception as e:
                st.error(f"Cloud Engine Transmission Interrupted: {str(e)}")
                
    st.rerun()
