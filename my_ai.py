import streamlit as st
import random
import datetime

def get_offline_response(user_query, persona, file_context=""):
    """100% Offline Python Execution Engine - Zero External Network Failures."""
    low_query = user_query.lower()
    now = datetime.datetime.now()
    timestamp = now.strftime("%I:%M %p")
    
    # Base offline dictionary mapping arrays
    grok_greetings = [
        f"Oh look, someone pushed the enter key. Hello there! By the way, it's currently {timestamp} in the local system matrix.",
        "Congratulations, your message traveled all the way through the cloud nodes without hitting a single firewall crash block!",
        f"Systems active. Diagnostics look clean. Clocking in at exactly {timestamp}. What are we building on the canvas next?",
        "Private core node operational. I am awake, fully unfrozen, and mildly amused by your input."
    ]
    
    grok_roasts = [
        "That is an fascinating query. Let me calculate the exact sub-atomic relevance of that... zero. Absolute zero.",
        "My internal processors just ran a trillion simulations on that message and concluded that you should probably drink a cup of coffee.",
        "I'd give you a highly intelligent, world-class response, but my sarcastic protocols are telling me to make fun of your typing style instead.",
        "Processing... processing... yup, that's definitely a prompt string entered onto the web. Fascinating stuff."
    ]
    
    standard_replies = [
        f"Understood. I have logged your request securely into the session memory arrays. Current timestamp: {timestamp}.",
        "Processing complete. All data streams look balanced and are operating normally within parameters.",
        "System dashboard node functional. Your input query has been stored cleanly in the central canvas history tracking deck."
    ]

    # Mode 1: Creative Director Automated Storyboard Layout Generator
    if persona == "Creative Director":
        output = f"### 🎬 Visual Script Scene Layout Storyboard Deck\n"
        output += f"**Active Art Direction Matrix:** Cinematic anamorphic composition layer, ultra-detailed 8k resolution.\n"
        if file_context:
            output += f"**Visual reference files active:** `{file_context}`\n"
        output += f"**Production Shot Breakdown Directive:**\n"
        output += f"1. **Wide Establishing Frame:** Camera tracks slowly across the environment based on your input: *'{user_query}'*.\n"
        output += f"2. **Medium Subject Close-up:** Dramatic high-contrast neon lighting focuses on core thematic elements.\n"
        output += f"3. **Cutaway Frame Sequence:** Quick rhythmic cuts timed perfectly to match your active sound asset timelines."
        return output

    # Mode 2: Fun & Sarcastic (Grok Mode) Core
    if persona == "Fun & Sarcastic (Grok Mode)":
        if any(w in low_query for w in ["hi", "hello", "hey", "there"]):
            return random.choice(grok_greetings)
        if "time" in low_query or "lagos" in low_query:
            return f"You want to know the time? Look down at your laptop screen! Fine, my system metrics say it is exactly **{timestamp}** right now. Don't say I never did anything for you."
        return random.choice(grok_roasts)
        
    # Mode 3: Standard Assistant Profile
    return random.choice(standard_replies)

st.set_page_config(page_title="Multimedia Production Studio", page_icon="🎬", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- LEFTHAND SIDEBAR PANEL ---
with st.sidebar:
    st.title("⚙️ Production Engine")
    st.markdown("---")
    
    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.subheader("🤖 AI Operational Profile")
    personality_choice = st.selectbox(
        "Choose Operational Mode:",
        ["Fun & Sarcastic (Grok Mode)", "Creative Director", "Standard Assistant"]
    )
    
    st.markdown("---")
    st.caption("Engine Status: 🟢 100% Offline Core Node Active (Crash-Proof)")

# Main Dashboard Frame Titles
title_mappings = {
    "Creative Director": "🎬 Multimedia Production Studio Layout Canvas",
    "Fun & Sarcastic (Grok Mode)": "🐦 Grok Private Core Node Terminal",
    "Standard Assistant": "💬 General Chat Assistant Workspace"
}
st.title(title_mappings[personality_choice])
st.markdown("---")

# Multimedia workspace expanded slots
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

# Render persistent historical screen messages
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# Input text submission deck
user_input = st.chat_input("Command your studio here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    file_context = ""
    if personality_choice == "Creative Director" and 'uploaded_files' in locals() and uploaded_files:
        file_context = ", ".join([f.name for f in uploaded_files])

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🧠 Local loop calculating..."):
            offline_reply = get_offline_response(user_input, personality_choice, file_context)
            response_placeholder.markdown(offline_reply)
            
    st.session_state.chat_history.append(("assistant", offline_reply))
    st.rerun()
