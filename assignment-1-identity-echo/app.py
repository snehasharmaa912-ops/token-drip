import streamlit as st

# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Echo Chamber 9000",
    page_icon="🛰️",
    layout="centered"
)

CHARS_PER_TOKEN = 4  


def estimate_tokens(text: str, chars_per_token: int = CHARS_PER_TOKEN) -> int:
    return len(text) 


# ----------------------------------------------------------------------
# Task 1: The UI Shell
# ----------------------------------------------------------------------
st.title("🛰️ Echo Chamber 9000")
st.write(
    "Transmit a message into the void. Fill in your details below, "
    "hit **Transmit**, and the system will echo it back — along with "
    "a live estimate of its token footprint."
)
st.divider()

# ----------------------------------------------------------------------
# Task 2: Multi-Data Collection
# ----------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    user_name = st.text_input("👤 Name", placeholder="Enter your name")
with col2:
    user_message = st.text_input("💬 Message", placeholder="Type your message")

# ----------------------------------------------------------------------
# Task 3: The Action Gate
# ----------------------------------------------------------------------
transmit = st.button("🚀 Transmit", use_container_width=True)

st.divider()

# ----------------------------------------------------------------------
# Task 4 & 5: Conditional Routing + Formatted Output
# ----------------------------------------------------------------------
if transmit:
    clean_name = user_name.strip()
    clean_message = user_message.strip()

    if clean_name == "":
        st.error("⚠️ Please provide your name.")
    elif clean_message == "":
        st.warning("⚠️ Please type a message to transmit.")
    else:
        st.success(
            f"✅ Transmission successful! Greetings, **{clean_name}**. "
            f"We received your message: _{clean_message}_"
        )

        # Token Cost Estimator
        char_count = len(clean_message)
        word_count = len(clean_message.split())
        token_count = estimate_tokens(clean_message)

        st.info(
            f"📊 System Check: Your message will consume approximately "
            f"**{token_count} tokens** from our context window."
        )

        # Extra detail panel with all computed metrics
        with st.expander("🔍 View transmission details"):
            m1, m2, m3 = st.columns(3)
            m1.metric("Character Count", char_count)
            m2.metric("Word Count", word_count)
            m3.metric("Estimated Tokens", token_count)
