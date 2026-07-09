import streamlit as st
import math

# -----------------------------------------------------------
# Page Config
# -----------------------------------------------------------
st.set_page_config(
    page_title="NeoCalc | Advanced Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------
# Session State
# -----------------------------------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = "0"
if "history" not in st.session_state:
    st.session_state.history = []
if "sci_mode" not in st.session_state:
    st.session_state.sci_mode = False

# -----------------------------------------------------------
# Styling
# -----------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Space+Grotesk:wght@400;600&display=swap');

.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

h1, h2, h3, .title-text {
    font-family: 'Orbitron', sans-serif !important;
}

.calc-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #a18cd1, #fbc2eb);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
    margin-bottom: 0;
}

@keyframes shine {
    0% {background-position: 0% 50%;}
    100% {background-position: 300% 50%;}
}

.subtitle {
    text-align: center;
    color: #a0a0c0;
    font-family: 'Space Grotesk', sans-serif;
    margin-top: -8px;
    margin-bottom: 20px;
    letter-spacing: 2px;
    font-size: 0.85rem;
}

.display-box {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 20px 25px;
    margin-bottom: 18px;
    box-shadow: 0 0 25px rgba(79, 172, 254, 0.25), inset 0 0 20px rgba(255,255,255,0.03);
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-10px);}
    to {opacity: 1; transform: translateY(0);}
}

.expr-text {
    color: #9d9dc0;
    font-family: 'Space Grotesk', monospace;
    font-size: 1rem;
    min-height: 22px;
    text-align: right;
    overflow-x: auto;
    white-space: nowrap;
}

.result-text {
    color: #ffffff;
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    text-align: right;
    text-shadow: 0 0 15px rgba(79, 172, 254, 0.6);
    overflow-x: auto;
    white-space: nowrap;
}

div.stButton > button {
    width: 100%;
    height: 58px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    color: #eaeaff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.04);
    background: linear-gradient(135deg, rgba(79,172,254,0.35), rgba(161,140,209,0.35));
    box-shadow: 0 0 20px rgba(79, 172, 254, 0.55);
    border-color: rgba(79,172,254,0.6);
}

div.stButton > button:active {
    transform: scale(0.96);
}

.history-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #4facfe;
    padding: 8px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    font-family: 'Space Grotesk', sans-serif;
    color: #c8c8e8;
    font-size: 0.85rem;
    animation: fadeIn 0.4s ease;
}

.op-btn button { background: rgba(79,172,254,0.18) !important; }
.eq-btn button {
    background: linear-gradient(135deg, #4facfe, #a18cd1) !important;
    color: white !important;
    font-weight: 700 !important;
}
.clear-btn button { background: rgba(255,90,90,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Header
# -----------------------------------------------------------
st.markdown('<div class="calc-title">🧮 NeoCalc</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ADVANCED SCIENTIFIC CALCULATOR • MIRAI INTERNSHIP PROJECT</div>', unsafe_allow_html=True)

st.session_state.sci_mode = st.toggle("Scientific Mode", value=st.session_state.sci_mode)

# -----------------------------------------------------------
# Display
# -----------------------------------------------------------
st.markdown(f"""
<div class="display-box">
    <div class="expr-text">{st.session_state.expression if st.session_state.expression else "&nbsp;"}</div>
    <div class="result-text">{st.session_state.result}</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Core Logic
# -----------------------------------------------------------
def press(key):
    if key == "C":
        st.session_state.expression = ""
        st.session_state.result = "0"
    elif key == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
    elif key == "=":
        try:
            safe_expr = (
                st.session_state.expression
                .replace("×", "*")
                .replace("÷", "/")
                .replace("^", "**")
                .replace("√", "math.sqrt")
                .replace("π", "math.pi")
                .replace("e", "math.e")
            )
            value = eval(safe_expr, {"__builtins__": {}}, {"math": math})
            rounded = round(value, 8)
            st.session_state.result = str(rounded)
            st.session_state.history.insert(
                0, f"{st.session_state.expression} = {rounded}"
            )
            st.session_state.history = st.session_state.history[:8]
            st.session_state.expression = str(rounded)
        except Exception:
            st.session_state.result = "Error"
    else:
        st.session_state.expression += key

# -----------------------------------------------------------
# Keypad Layout
# -----------------------------------------------------------
if st.session_state.sci_mode:
    rows = [
        ["sin(", "cos(", "tan(", "√("],
        ["log(", "(", ")", "^"],
        ["π", "e", "%", "C"],
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["0", ".", "⌫", "+"],
    ]
else:
    rows = [
        ["C", "⌫", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "=", ""],
    ]

for row in rows:
    cols = st.columns(len(row))
    for col, key in zip(cols, row):
        if key == "":
            continue
        with col:
            wrapper_class = ""
            if key in ["÷", "×", "-", "+", "^", "%"]:
                wrapper_class = "op-btn"
            elif key == "=":
                wrapper_class = "eq-btn"
            elif key in ["C", "⌫"]:
                wrapper_class = "clear-btn"

            if wrapper_class:
                st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(key, key=f"btn_{key}_{row.index(key)}"):
                press(key)
                st.rerun()
            if wrapper_class:
                st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.sci_mode:
    if st.button("=", key="sci_equals", use_container_width=True):
        press("=")
        st.rerun()

# -----------------------------------------------------------
# History Panel
# -----------------------------------------------------------
if st.session_state.history:
    st.markdown("#### 📜 History")
    for item in st.session_state.history:
        st.markdown(f'<div class="history-item">{item}</div>', unsafe_allow_html=True)
