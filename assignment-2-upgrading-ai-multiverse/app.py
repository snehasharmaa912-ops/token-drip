import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# Environment Setup
# ----------------------------------------------------------------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="The Multiverse of Chatbots",
    page_icon="🌀",
    layout="centered"
)

# ----------------------------------------------------------------------
# Task 1: The UI Shell
# ----------------------------------------------------------------------
st.title("🌀 The Multiverse of Chatbots")
st.write(
    "Pick a personality, send a message, and get a response straight "
    "from that character's universe."
)
st.divider()

# ----------------------------------------------------------------------
# Task 2: Persona Selection
# ----------------------------------------------------------------------
PERSONAS = [
    "An expert Hacker",
    "An angry Ravi Shastri",
    "A crazy Ronaldo fan",
    "A dramatic Bollywood villain",
    "A sleep-deprived college senior"
]

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("**🧑‍🎤 Choose your persona**")
with col2:
    personality = st.selectbox("Who do you want to talk to?", PERSONAS, label_visibility="collapsed")

# ----------------------------------------------------------------------
# Task 3: Message Input
# ----------------------------------------------------------------------
user_message = st.text_input("💬 Your message", placeholder="Type something to send into the multiverse...")

# ----------------------------------------------------------------------
# Task 4: The Action Gate
# ----------------------------------------------------------------------
send = st.button("🚀 SEND", use_container_width=True)

st.divider()

# ----------------------------------------------------------------------
# Task 5: Conditional Routing + AI Response
# ----------------------------------------------------------------------
if send:
    # Strip whitespace so entries like "   " don't count as valid input
    clean_message = user_message.strip()

    if clean_message == "":
        st.warning("⚠️ Please type a message before sending.")
    else:
        # Build the persona-aware prompt for the model
        ai_instructions = (
            f"You are acting as {personality}. "
            f"Respond to this message in character: {clean_message}"
        )

        with st.spinner("Connecting to the multiverse... 🌀"):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_instructions
            )

        # Success case — display the AI's in-character response
        st.success("✅ Message received!")
        st.markdown(f"**{personality} says:**")
        st.info(response.text)

        # Extra detail panel with computed metrics
        char_count = len(clean_message)
        token_count = char_count // 4

        with st.expander("🔍 View transmission details"):
            m1, m2, m3 = st.columns(3)
            m1.metric("Persona", personality.split()[0])
            m2.metric("Character Count", char_count)
            m3.metric("Estimated Tokens", token_count)
