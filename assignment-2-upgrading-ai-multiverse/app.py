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
# Task 1: Initialize the Memory Vault
# ----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------------------------
# The UI Shell
# ----------------------------------------------------------------------
st.title("🌀 The Multiverse of Chatbots")
st.write(
    "Pick a personality, send a message, and get a response straight "
    "from that character's universe. This chatbot now remembers your "
    "conversation. 🧠"
)
st.divider()

# ----------------------------------------------------------------------
# Persona Selection
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

st.divider()

# ----------------------------------------------------------------------
# Task 2: Render the Chat History
# ----------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ----------------------------------------------------------------------
# Task 3 & 4: Chat Input, Memory Saving, and AI Response
# ----------------------------------------------------------------------
if user_message := st.chat_input("Say something..."):
    # Save and display the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.write(user_message)

    # Build the persona-aware prompt for the model
    ai_instructions = (
        f"You are acting as {personality}. "
        f"Respond to this message in character: {user_message}"
    )

    with st.chat_message("assistant"):
        with st.spinner("Connecting to the multiverse... 🌀"):
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=ai_instructions
            )
            st.write(response.text)

    # Save the AI's response to the vault
    st.session_state.messages.append({"role": "assistant", "content": response.text})
