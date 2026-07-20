"""
Visual Novel Engine - MirAI "AI Builder" Track Capstone
A choose-your-own-adventure engine that orchestrates three pipelines:
  - Gemini (stateful structured-JSON story generation)
  - Pollinations (scene art generation)
  - gTTS (narration audio)
"""

import streamlit as st
import os
import json
import requests
from io import BytesIO
from google import genai
from google.genai import types
from dotenv import load_dotenv
from gtts import gTTS

# ----------------------------------------------------------------------
# Environment Setup
# ----------------------------------------------------------------------
load_dotenv()

# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Visual Novel Engine",
    page_icon="📖",
    layout="centered"
)

# ----------------------------------------------------------------------
# Phase 1: Cached Gemini Client
# ----------------------------------------------------------------------
@st.cache_resource
def get_client():
    """Create and cache a single Gemini client for the app's lifetime."""
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

# ----------------------------------------------------------------------
# Sidebar: Story Settings
# ----------------------------------------------------------------------
st.sidebar.header("📚 Story Settings")

genre = st.sidebar.selectbox(
    "🎭 Story Genre",
    ["Fantasy Adventure", "Cyberpunk Thriller", "Horror Mystery", "Sci-Fi Odyssey", "Mythological Epic"]
)

art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    ["Anime", "Realistic", "Watercolor", "Pixel Art", "Cyberpunk Neon"]
)

restart = st.sidebar.button("🔄 Restart Story", use_container_width=True)

# ----------------------------------------------------------------------
# System Prompt: Force Structured JSON Output
# ----------------------------------------------------------------------
SYSTEM_PROMPT = (
    f"You are the narrator of an interactive {genre} visual novel. "
    "Every reply you send must be ONLY a raw JSON object, no markdown fences, "
    "no commentary, with EXACTLY these three keys:\n"
    "1. \"story_text\": a vivid narrative paragraph (4-6 sentences) continuing the story.\n"
    "2. \"image_prompt\": a heavily detailed, comma-separated visual prompt describing the "
    f"current scene, written for an AI image generator in a {art_style} art style.\n"
    "3. \"options\": a JSON array of 2 to 3 short, distinct strings describing what the "
    "protagonist can do next.\n"
    "Never include any text outside the JSON object."
)

# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
if "chat" not in st.session_state or restart:
    st.session_state.chat = client.chats.create(
        model="gemini-flash-latest",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json"
        )
    )
    st.session_state.current = None
    st.session_state.turn_count = 0

# ----------------------------------------------------------------------
# Helper: Parse Gemini's JSON reply safely
# ----------------------------------------------------------------------
def parse_scene(raw_text):
    """Parse Gemini's raw string response into a scene dictionary, tolerating
    stray markdown fences the model sometimes adds despite instructions."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("\n", 1)[-1] if cleaned.lower().startswith("json") else cleaned
    return json.loads(cleaned)

# ----------------------------------------------------------------------
# Helper: Fetch scene art from Pollinations (fails gracefully)
# ----------------------------------------------------------------------
def fetch_scene_image(image_prompt):
    """Download a Pollinations image for the given prompt. Returns image bytes
    or None if the image server is unavailable."""
    try:
        url = f"https://image.pollinations.ai/prompt/{image_prompt}?width=768&height=512&nologo=true"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.content
    except Exception:
        st.toast("🖼️ Image server is busy, skipping visual...")
        return None

# ----------------------------------------------------------------------
# Helper: Generate TTS narration (fails gracefully)
# ----------------------------------------------------------------------
def generate_narration(story_text):
    """Convert story_text to speech using gTTS. Returns audio bytes or None."""
    try:
        tts = gTTS(text=story_text, lang="en")
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer.read()
    except Exception:
        st.toast("🔊 Narration engine is busy, skipping audio...")
        return None

# ----------------------------------------------------------------------
# Helper: Send a move to Gemini and build the next scene
# ----------------------------------------------------------------------
def advance_story(user_move):
    """Send the player's move to Gemini, parse the reply, generate art + audio,
    and store the resulting scene in session state."""
    with st.spinner("✍️ Writing the next chapter..."):
        try:
            response = st.session_state.chat.send_message(user_move)
            scene = parse_scene(response.text)
        except Exception:
            st.toast("⚠️ The storyteller stumbled, please try that choice again...")
            return

    scene["image_bytes"] = fetch_scene_image(scene.get("image_prompt", ""))
    scene["audio_bytes"] = generate_narration(scene.get("story_text", ""))

    st.session_state.current = scene
    st.session_state.turn_count += 1

# ----------------------------------------------------------------------
# The UI Shell
# ----------------------------------------------------------------------
st.title("📖 Visual Novel Engine")
st.write("An AI-narrated, choose-your-own-adventure story that writes, paints, and narrates itself as you play.")
st.divider()

with st.expander("📊 Session Stats"):
    col1, col2, col3 = st.columns(3)
    col1.metric("Genre", genre)
    col2.metric("Art Style", art_style)
    col3.metric("Chapters", st.session_state.turn_count)

# ----------------------------------------------------------------------
# Kick off the story on first load
# ----------------------------------------------------------------------
if st.session_state.current is None:
    advance_story("Begin the story with an opening scene that sets up the world and the protagonist.")

# ----------------------------------------------------------------------
# Phase 4: Render the Current Scene (persists via session_state)
# ----------------------------------------------------------------------
scene = st.session_state.current

if scene:
    if scene.get("image_bytes"):
        st.image(scene["image_bytes"], use_container_width=True)

    st.markdown(f"### Chapter {st.session_state.turn_count}")
    st.write(scene.get("story_text", ""))

    if scene.get("audio_bytes"):
        st.audio(scene["audio_bytes"], format="audio/mp3")

    st.divider()

    # --------------------------------------------------------------
    # Phase 3: Dynamic Buttons Generated from the AI's options list
    # --------------------------------------------------------------
    st.markdown("**What do you do?**")
    options = scene.get("options", [])

    for i, option in enumerate(options):
        if st.button(option, key=f"option_{st.session_state.turn_count}_{i}", use_container_width=True):
            advance_story(option)
            st.rerun()
else:
    st.error("The story could not be generated. Please check your connection and try again.")
    if st.button("🔁 Retry"):
        advance_story("Begin the story with an opening scene that sets up the world and the protagonist.")
        st.rerun()
