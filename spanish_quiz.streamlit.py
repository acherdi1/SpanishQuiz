import streamlit as st
import random

# Load dictionary
def load_dictionary(filename):
    words = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t", 2)
            if len(parts) >= 2:
                words.append(parts)
    return words

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.words = load_dictionary("ichebnik.verbs.all.con_ej.txt")
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.answer_submitted = False
    st.session_state.input_text_value = ""
    st.session_state.initialized = True

# Random order toggle
random_order = st.toggle("Random Order?", value=True)

# If random order toggled, reset
if "randomized" not in st.session_state or st.session_state.randomized != random_order:
    st.session_state.words = load_dictionary("ichebnik.verbs.all.con_ej.txt")
    if random_order:
        random.shuffle(st.session_state.words)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.randomized = random_order

st.title("📚 Spanish Quiz - Terminal Mode")

# Function to submit answer
def submit_answer():
    st.session_state.answer_submitted = True

# Check if finished
if st.session_state.index >= len(st.session_state.words):
    st.success("🎉 You've finished the quiz!")
    st.write(f"Final Score: {st.session_state.score}")
else:
    current = st.session_state.words[st.session_state.index]

    # Prepare extra
    if len(current) > 2:
        extra = current[2].replace(current[0], "_______")
        extra_parts = extra.split("  -- ")
        extra_text = "\n -- ".join(extra_parts[1:]) if len(extra_parts) > 1 else ""
    else:
        extra_text = ""

    # Show history (terminal style)
    for entry in st.session_state.history:
        st.markdown(entry, unsafe_allow_html=True)

    # Show question
    st.markdown(f"**{current[1]}**")
    if extra_text:
        st.markdown(f"<pre>{extra_text}</pre>", unsafe_allow_html=True)

    # Input box
    input_text = st.text_input(
        "Type your answer here:",
        value=st.session_state.input_text_value,
        key="input_text_value",
        on_change=submit_answer,
    )

    if st.session_state.answer_submitted:
        correct_answer = current[0]
        user_answer = st.session_state.input_text_value.strip()

        if user_answer == correct_answer:
            feedback = f"<span style='color:green;'>✅ Correct! +1 point (Total: {st.session_state.score + 1})</span>"
            st.session_state.score += 1
            st.session_state.history.append(
                f"<b>{current[1]}</b><br><pre>{extra_text}</pre>➔ {user_answer} {feedback}<br><br>"
            )
            st.session_state.index += 1
        else:
            feedback = f"<span style='color:red;'>❌ Wrong! (Correct answer: {correct_answer}) -1 point (Total: {st.session_state.score - 1})</span>"
            st.session_state.score -= 1
            st.session_state.history.append(
                f"<b>{current[1]}</b><br><pre>{extra_text}</pre>➔ {user_answer} {feedback}<br><br>"
            )

        # Reset input properly
        st.session_state.input_text_value = ""
        st.session_state.answer_submitted = False
        st.rerun()
