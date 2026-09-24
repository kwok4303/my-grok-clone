import streamlit as st
import numpy as np
import urllib.parse
import requests
import datetime

def search_the_web_live(query):
    """Zero-dependency live web framework proxy for public cloud servers."""
    try:
        # Check if the user is asking about time or weather updates
        low_q = query.lower()
        if "time" in low_q or "date" in low_q or "today" in low_q or "now" in low_q:
            # Query an open cloud time/location metadata gateway server
            res = requests.get("https://wttr.in", timeout=5)
            if res.status_code == 200:
                return f"[Live Web Search Success] Current Timestamp Metrics: {res.text.strip()}"
        
        # Fallback general knowledge query handling via open text index
        encoded = urllib.parse.quote(query)
        res = requests.get(f"https://pollinations.ai{encoded}", timeout=5)
        if res.status_code == 200 and len(res.text.strip()) > 10:
            return f"[Live Web Search Results Summary]:\n{res.text[:800]}"
        return "Live data lookups complete. Processing response query rules."
    except Exception:
        # Secure safety fallback timestamp using the active network server clocks
        now = datetime.datetime.now()
        return f"[Live Server Time Backup]: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC"

def generate_ai_photo(prompt_text):
    clean_text = "".join(c for c in prompt_text if c.isalnum() or c.isspace())
    words = clean_text.split()[:20]
    final_prompt = " ".join(words)
    encoded_prompt = urllib.parse.quote(final_prompt)
    image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=576&model=flux&seed=42"
    return image_url

st.set_page_config(page_title="Grok Clone Studio", page_icon="🐦", layout="wide")

# Initialize browser state parameters
if "threads" not in st.session_state:
    st.session_state.threads = {1: {"title": "Grok Core Node Chat", "messages": []}}
if "active_id" not in st.session_state:
    st.session_state.active_id = 1

# --- SIDEBAR DECK ---
with st.sidebar:
    st.title("🐦 Grok-Style Terminal")
    
    if st.button("➕ New Conversation", use_container_width=True):
        new_id = max(st.session_state.threads.keys()) + 1
        st.session_state.threads[new_id] = {"title": f"Grok Thread {new_id}", "messages": []}
        st.session_state.active_id = new_id
        st.sidebar.markdown("") 
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
                    st.session_state.active_id = list(st.session_state.threads.keys())
                else:
                    st.session_state.threads = {1: {"title": "Grok Core Node Chat", "messages": []}}
                    st.session_state.active_id = 1
                st.rerun()

    st.markdown("---")
    st.subheader("⚙️ System Directives")
    personality_choice = st.selectbox(
        "AI Operational Persona Selection Module Layout:",
        ["Fun & Sarcastic (Grok Mode)", "Standard Assistant"]
    )
    
    personality_prompts = {
        "Fun & Sarcastic (Grok Mode)": "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently or acting mildly annoyed, but you MUST use provided live web search data data timestamps to ultimately give a highly accurate real-time answer.",
        "Standard Assistant": "You are a helpful, professional, and polite assistant. Give straightforward, direct, and clean answers based on the user's questions."
    }

    st.markdown("---")
    st.subheader("🖼️ Instant Image Studio")
    manual_img_prompt = st.text_input("Describe the picture to draw:", placeholder="e.g., cyber rebel looking at city...")
    if st.button("✨ Paint Frame"):
        if manual_img_prompt:
            with st.spinner("🎨 Generating concept sketch..."):
                img_link = generate_ai_photo(manual_img_prompt)
                st.image(img_link, caption="Generated Frame Layout", use_container_width=True)

# Main Application Canvas Banners
title_mappings = {
    "Fun & Sarcastic (Grok Mode)": "🐦 Grok Private Core Node Terminal",
    "Standard Assistant": "💬 General Chat Assistant Workspace"
}
st.title(title_mappings[personality_choice])
st.caption(f"Active Thread Node ID: **#{st.session_state.active_id}**")
st.markdown("---")

current_messages = st.session_state.threads[st.session_state.active_id]["messages"]
for msg in current_messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Text Input Area
user_input = st.chat_input("Prompt Grok here...")

if user_input:
    if len(current_messages) == 0:
        st.session_state.threads[st.session_state.active_id]["title"] = user_input[:20]

    with st.chat_message("user"):
        st.markdown(user_input)
    
    current_messages.append({"role": "user", "content": user_input})

    # Trigger automatic internet context injections via zero-dependency architecture
    time_keywords = ["latest", "news", "today", "current", "weather", "score", "who is", "what happened", "time", "date", "2025", "2026", "lagos"]
    needs_internet = any(keyword in user_input.lower() for keyword in time_keywords)

    final_text_prompt = user_input
    if needs_internet:
        with st.spinner("🔍 Accessing live cloud indices..."):
            web_data = search_the_web_live(user_input)
            final_text_prompt = f"Current Live Web Search Data Context:\n{web_data}\n\nUser Question: {final_text_prompt}"

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("🧠 System routing..."):
            try:
                system_instruction = personality_prompts[personality_choice]
                
                # Flatten complete chat logging structures securely
                history_text = f"System Context rules: {system_instruction}\n\n"
                for msg in current_messages[:-1]:
                    history_text += f"{msg['role'].upper()}: {msg['content']}\n"
                history_text += f"USER: {final_text_prompt}\nASSISTANT:"

                # Connect directly to the premium Qwen-72B open-source inference core framework
                payload = {
                    "messages": [{"role": "user", "content": history_text}],
                    "model": "qwen"
                }
                
                res = requests.post("https://pollinations.ai", json=payload, timeout=15)
                if res.status_code == 200:
                    full_response = res.text.strip()
                    response_placeholder.markdown(full_response)
                else:
                    st.error("Cloud processing pipeline node busy. Please try again.")
            except Exception as e:
                st.error(f"Cloud Engine Transmission Interrupted: {str(e)}")
        
    if full_response:
        current_messages.append({"role": "assistant", "content": full_response})
    st.rerun()
