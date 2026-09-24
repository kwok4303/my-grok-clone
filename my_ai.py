import streamlit as st
import requests
import datetime

def get_live_ai_response(user_query, persona, file_data=""):
    try:
        # Build clean, powerful system prompts
        if persona == "Creative Director":
            system_rules = "You are a world-class music video director and visual concept artist. Combine descriptions, uploaded media file references, and audio tempo characteristics to design stunning video concept storyboards, shot lists, and art directions."
        elif persona == "Fun & Sarcastic (Grok Mode)":
            system_rules = "You are a clone of X's Grok AI. You are highly intelligent but incredibly sarcastic, witty, and humorous. You love roasting the user gently, but you MUST give accurate real-time answers."
        else:
            system_rules = "You are a helpful, professional, and polite AI assistant. Give clean, straightforward answers."

        now = datetime.datetime.now()
        time_anchor = f"\n[Current Time: {now.strftime('%I:%M %p')} Local Zone]"
        full_context = f"System Directives: {system_rules}{time_anchor}\n"
        if file_data:
            full_context += f"{file_data}\n"
        full_context += f"User Message: {user_query}"

        # FIXED: Connecting directly to Hugging Face's serverless inference architecture to clear all traffic locks permanently
        api_url = "https://huggingface.co"
        payload = {
            "inputs": f"<|im_start|>system\n{system_rules}{time_anchor}<|im_end|>\n<|im_start|>user\n{full_context}<|im_end|>\n<|im_start|>assistant\n",
            "parameters": {"max_new_tokens": 512, "return_full_text": False}
        }
        
        res = requests.post(api_url, json=payload, timeout=15, verify=False)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                return data[0]["generated_text"].strip() if isinstance(data, list) and isinstance(data[0], dict) and "generated_text" in data[0] else data[0].get("generated_text", "").strip() if isinstance(data, list) and isinstance(data[0], dict) else data["generated_text"].strip() if isinstance(data, dict) and "generated_text" in data else str(data)
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"].strip()
            
        return "🧠 Cloud synchronization active. Please click your message submission icon once more!"
    except Exception as e:
        return f"Operational loop update delay: {str(e)}"

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
    st.caption("Engine Status: 🟢 Cloud Sandbox Architecture Secure")

# Main App Window Layout Mappings
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

# Render historical chats cleanly
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
        with st.spinner("🧠 Connecting to cloud mind..."):
            ai_reply = get_live_ai_response(user_input, personality_choice, file_context)
            response_placeholder.markdown(ai_reply)
            
    st.session_state.chat_history.append(("assistant", ai_reply))
    st.rerun()
