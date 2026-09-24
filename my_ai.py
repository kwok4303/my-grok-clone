import streamlit as st
import random
import datetime

def get_offline_response(user_query, persona, file_context=""):
    low_query = user_query.lower()
    now = datetime.datetime.now()
    timestamp = now.strftime("%I:%M %p")
    
    grok_greetings = [
        f"Oh look, someone pushed the enter key! Hello there. It is currently {timestamp} in the local system matrix.",
        "Congratulations, your message traveled all the way through the cloud nodes cleanly!",
        f"Systems active. Clocking in at exactly {timestamp}. What are we creating on the studio canvas next?",
        "Private core terminal operational. I am awake, fully unfrozen, and responding instantly."
    ]
    
    grok_replies = [
        "That is an interesting query. My internal processors have logged it into the active workspace logs.",
        "Processing complete. The data streams are perfectly balanced and running smoothly within parameters.",
        "I'd give you a world-class AI breakdown, but my sarcastic protocols are telling me to keep things short and sweet.",
        "System dashboard node functional. Your input has been saved cleanly in the central canvas history tracking deck."
    ]

    if persona == "Creative Director":
        output = f"### 🎬 Visual Script Scene Layout Storyboard Deck\n"
        output += f"**Active Art Direction Matrix:** Cinematic anamorphic composition layout.\n"
        if file_context:
            output += f"**Visual reference files active:** `{file_context}`\n"
        output += f"**Production Shot Breakdown Directive:**\n"
        output += f"1. **Wide Establishing Frame:** Camera tracks slowly across the environment based on your input: *'{user_query}'*.\n"
        output += f"2. **Medium Subject Close-up:** High-contrast lighting focuses on the core thematic elements.\n"
        output += f"3. **Cutaway Frame Sequence:** Quick rhythmic cuts timed perfectly to match your sound layout assets."
        return output

    if persona == "Fun & Sarcastic (Grok Mode)":
        if any(w in low_query for w in ["hi", "hello", "hey", "there"]):
            return random.choice(grok_greetings)
        if "time" in low_query or "lagos" in low_query:
            return f"You want to know the time? Fine, my internal core clocks say it is exactly **{timestamp}** right now. Don't say I never did anything for you."
        return random.choice(grok_replies)
        
    return "System node functional. Input query logged securely."

st.set_page_config(page_title="Multimedia Production Studio", page_icon="🎬", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR MASTER DECK ---
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
    st.caption("Engine Status: 🟢 100% Stable Internal Core Active")

# Main Interface Titles
title_mappings = {
    "Creative Director": "🎬 Multimedia Production Studio Layout Canvas",
    "Fun & Sarcastic (Grok Mode)": "🐦 Grok Private Core Node Terminal",
    "Standard Assistant": "💬 General Chat Assistant Workspace"
}
st.title(title_mappings[personality_choice])
st.markdown("---")

# Multimedia workspace slots
if personality_choice == "Creative Director":
    with st.expander("📁 Open Media Upload Workspace (Images & Music Tracks)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            uploaded_files = st.file_uploader("📸 Mood board images:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="prod_img")
            if uploaded_files:
                for file in uploaded_files:
                    st.image(file, caption=file.name)
        with col2:
            uploaded_audio = st.file_uploader("🎵 MP3 Audio track:", type=["mp3"], key="prod_aud", accept_multiple_files=False)
            if uploaded_audio:
                st.audio(uploaded_audio, format="audio/mp3")

st.markdown("---")

# Render historical messages
for role, text in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(text)

# Chat Input bar
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
        with st.spinner("🧠 Internal loop calculating..."):
            reply = get_offline_response(user_input, personality_choice, file_context)
            response_placeholder.markdown(reply)
            
    st.session_state.chat_history.append(("assistant", reply))
    st.rerun()
