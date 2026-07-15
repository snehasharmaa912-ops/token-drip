import streamlit as st
import random

# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered"
)

# ----------------------------------------------------------------------
# The UI Shell
# ----------------------------------------------------------------------
st.title("🎨 AI Image Studio")
st.write("Describe your vision, pick a style, and let the studio bring it to life.")
st.divider()

# ----------------------------------------------------------------------
# Sidebar Settings
# ----------------------------------------------------------------------
st.sidebar.header("⚙️ Studio Settings")

art_style = st.sidebar.selectbox(
    "🎭 Art Style",
    ["Realistic", "Anime", "Cyberpunk", "Watercolor", "Pixel Art", "Fantasy"]
)

width = st.sidebar.slider("📏 Width", min_value=256, max_value=1024, value=512, step=64)
height = st.sidebar.slider("📐 Height", min_value=256, max_value=1024, value=512, step=64)

# Task 3: Magic Enhance toggle
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# ----------------------------------------------------------------------
# Prompt Input
# ----------------------------------------------------------------------
prompt = st.text_input("💬 Describe your image", placeholder="A dragon flying over a neon city...")

# ----------------------------------------------------------------------
# Task 4: Surprise Me prompt bank
# ----------------------------------------------------------------------
SURPRISE_PROMPTS = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A wizard cat brewing potions in a treehouse",
    "A steampunk train flying through the clouds",
    "A bioluminescent jungle at midnight"
]

col1, col2 = st.columns(2)
with col1:
    generate = st.button("🚀 Generate", use_container_width=True)
with col2:
    surprise = st.button("🎲 Surprise Me!", use_container_width=True)

st.divider()

# ----------------------------------------------------------------------
# Image Generation Logic
# ----------------------------------------------------------------------
final_prompt = None

if generate and prompt.strip() != "":
    final_prompt = prompt.strip()

if surprise:
    final_prompt = random.choice(SURPRISE_PROMPTS)
    st.info(f"🎲 Surprise prompt: **{final_prompt}**")

if generate and prompt.strip() == "" and not surprise:
    st.warning("⚠️ Please describe an image, or click Surprise Me!")

if final_prompt:
    full_prompt = f"{final_prompt}, {art_style} style"

    # Task 3: secretly boost the prompt if Magic Enhance is on
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    # Task 1: actually pass width & height to the API via URL parameters
    url = f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}"

    with st.spinner("🎨 Painting your masterpiece..."):
        st.image(url, caption=full_prompt, use_container_width=True)

        # Task 2: correct, dynamic file extension
        st.download_button(
            label="⬇️ Download Image",
            data=url,
            file_name=f"{art_style}_image.png",
            mime="image/png"
        )
