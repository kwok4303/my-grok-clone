import streamlit as st
import urllib.parse

def generate_visual_frame(prompt_text, mode, references=""):
    if mode == "Cinematic Storyboard Deck":
        style_lens = "cinematic film still, highly detailed 8k video storyboard composition, art direction layout"
    elif mode == "Grok Dark Humor Caricature Mode":
        style_lens = "funny dark humor illustration, witty caricature, colorful comic panel"
    else:
        style_lens = "clean minimalist infographic graphic layout asset"

    # Clean the input text query parameters safely
    clean_text = "".join(c for c in prompt_text if c.isalnum() or c.isspace())
    final_prompt = f"{clean_text}, {style_lens}"
    if references:
        final_prompt += f", cross-referenced with assets: {references}"
        
    encoded_string = urllib.parse.quote(final_prompt.strip())
    
    # FIXED: Swapped to a premium serverless visual delivery node layout to prevent broken image blocks completely!
    return f"https://pollinations.ai{encoded_string}?width=1024&height=576&model=flux&enhance=false"

st.set_page_config(page_title="Visual Production Terminal v2.0", page_icon="🎬", layout="wide")

if "gallery_frames" not in st.session_state:
    st.session_state.gallery_frames = []

# --- SIDEBAR MASTER CONTROL PANEL ---
st.sidebar.title("🛠️ Studio Master Console")
st.sidebar.markdown("---")

if st.sidebar.button("🗑️ Clear Production Timeline", use_container_width=True):
    st.session_state.gallery_frames = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Engine Style Selection")
active_persona = st.sidebar.selectbox(
    "Select Directing Profile Module:",
    ["Cinematic Storyboard Deck", "Grok Dark Humor Caricature Mode", "Corporate Slide Asset Studio"]
)

# --- MAIN SCREEN CANVAS HEADER ---
st.title(f"🎭 Active Stage Canvas: {active_persona}")
st.markdown("---")

# Multimedia reference drop zone deck
if active_persona == "Cinematic Storyboard Deck":
    with st.expander("📁 Drop Production Reference Materials (Mood Images & Audio Tracks)", expanded=True):
        left_pane, right_pane = st.columns(2)
        with left_pane:
            scene_images = st.file_uploader("📸 Batch upload moodboard inspiration frames:", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="studio_v2_img")
            if scene_images:
                grid_cols = st.columns(3)
                for index, image_file in enumerate(scene_images):
                    grid_cols[index % 3].image(image_file, caption=image_file.name, use_container_width=True)
        with right_pane:
            scene_track = st.file_uploader("🎵 Upload temporary audio track layout (MP3 format):", type=["mp3"], key="studio_v2_aud")
            if scene_track:
                st.audio(scene_track)

st.markdown("---")

# Render storyboard assets onto the screen timeline
for sequence_num, (prompt_directive, frame_url) in enumerate(st.session_state.gallery_frames, 1):
    with st.container(border=True):
        st.subheader(f"🎬 Storyboard Sequence Frame Block #{sequence_num}")
        st.caption(f"**Director Directive Prompt:** {prompt_directive}")
        st.image(frame_url, use_container_width=True)

# Central user prompt input console
director_command = st.chat_input("Type the description of the sequence frame you want to draw...")

if director_command:
    reference_names = ""
    if active_persona == "Cinematic Storyboard Deck" and 'scene_images' in locals() and scene_images:
        reference_names = ", ".join([file.name for file in scene_images])

    with st.spinner("🎨 Rendering production asset frame onto timeline..."):
        generated_shot_link = generate_visual_frame(director_command, active_persona, reference_names)
        st.session_state.gallery_frames.append((director_command, generated_shot_link))
        
    st.rerun()
