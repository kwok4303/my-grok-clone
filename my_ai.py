import streamlit as st
import urllib.parse
import requests
import datetime

def get_live_ai_response(user_query, persona):
    try:
        clean_text = "".join(c for c in user_query if c.isalnum() or c.isspace())
        
        system_rules = (
            "You are a clone of X's Grok AI. You are highly intelligent, sarcastic, witty, and humorous. Love roasting the user gently. Give highly accurate real-time answers."
            if persona == "Fun & Sarcastic (Grok Mode)"
            else "You are a helpful, professional, and polite AI assistant. Give clean, straightforward answers."
        )
        
        # FIXED: Uses your laptop's standard clock to track time instantly without messy web errors
        now = datetime.datetime.now()
        time_anchor = f" [Current Internal Clock Timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')} Lagos/Local Zone]"
        combined_prompt = f"{system_rules} User Question: {clean_text}{time_anchor}"
        
        encoded_query = urllib.parse.quote(combined_prompt)
        api_url = f"https://pollinations.ai{encoded_query}?model=openai&jsonMode=false"
        res = requests.get(api_url, timeout=12, verify=False)
        
        if res.status_code == 200 and res.text:
            return res.text.strip()
        return "System network core busy. Let's try that message again!"
    except Exception as e:
        return f"Operational loop error: {str(e)}"

st.set_page_config(page_title="Grok Clone Studio", page_icon="🐦", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR CONTROL CANVAS ---
with st.sidebar:
    st.title("🐦 Grok-Style Terminal")
    
    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.subheader("⚙️ System Directives")
    personality_choice = st.selectbox(
        "AI Operational Persona Selection Layout:",
        ["Fun & Sarcastic (Grok Mode)", "Standard Assistant"]
    )
    
    st.markdown("---")
    st.subheader("🖼️ Instant Image Studio")
    manual_img_prompt = st.text_input("Describe the picture to draw:", placeholder="e.g., cyber rebel looking at city...")
    if st.button("✨ Paint Frame"):
        if manual_img_prompt:
            with st.spinner("🎨 Generating concept sketch..."):
                encoded_img = urllib.parse.quote(manual_img_prompt)
                img_link = f"https://pollinations.ai{encoded_img}?width=1024&height=576&model=flux&seed=42"
                st.image(img_link, caption="Generated Frame Layout", use_container_width=True)

# Main Title canvas headers mapping rules
st.title("🐦 Grok Private Core Node Terminal" if personality_choice == "Fun & Sarcastic (Grok Mode)" else "💬 General Chat Assistant Workspace")
st.markdown("---")

# Render active layout message bubbles cleanly onto screen view grids
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# Chat text input entry box component tool
user_input = st.chat_input("Prompt Grok here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🧠 Grok is thinking..."):
            ai_reply = get_live_ai_response(user_input, personality_choice)
            response_placeholder.markdown(ai_reply)
            
    st.session_state.chat_history.append(("assistant", ai_reply))
    st.rerun()
