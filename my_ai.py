import streamlit as st
import urllib.parse
import requests
import datetime

def get_live_ai_response(user_query, persona):
    try:
        # Strip special characters and keep text ultra-short
        clean_text = "".join(c for c in user_query if c.isalnum() or c.isspace())[:50]
        
        # Build ultra-short, space-saving instructions to easily fit the URL length limits
        if persona == "Fun & Sarcastic (Grok Mode)":
            system_rules = "Act as X's Grok AI. Be highly intelligent, witty, and deeply sarcastic. Roast the user playfully."
        else:
            system_rules = "Act as a helpful, polite, and direct AI assistant."
        
        now = datetime.datetime.now()
        time_anchor = f" Time: {now.strftime('%H:%M')}."
        
        # Create a clean, short composite text block
        combined_prompt = f"{system_rules} Query: {clean_text}. {time_anchor}"
        
        # Encode and route using a highly stable API method
        encoded_query = urllib.parse.quote(combined_prompt)
        api_url = f"https://pollinations.ai{encoded_query}"
        
        # Add a custom text header to enforce standard chat processing behaviors
        headers = {"Content-Type": "text/plain"}
        res = requests.get(api_url, headers=headers, timeout=12, verify=False)
        
        if res.status_code == 200 and res.text:
            return res.text.strip()
        return "System engine cluster busy. Send that message again!"
    except Exception as e:
        return f"Operational drop: {str(e)}"

st.set_page_config(page_title="Grok Clone Studio", page_icon="🐦", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR CONTROL DECK ---
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

# Main Title headers
st.title("🐦 Grok Private Core Node Terminal" if personality_choice == "Fun & Sarcastic (Grok Mode)" else "💬 General Chat Assistant Workspace")
st.markdown("---")

# Render active message bubbles cleanly onto screen view grids
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
