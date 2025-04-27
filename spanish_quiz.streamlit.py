import streamlit as st
import random

# Load the dictionary
def load_dictionary(filename):
    words = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t", 2)
            if len(parts) >= 2:
                words.append(parts)
    return words

# Initialize session state
if "words" not in st.session_state:
    st.session_state.words = load_dictionary("ichebnik.verbs.all.con_ej.txt")
    random.shuffle(st.session_state.words)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.current_answer = ""

# Function to process the answer
def submit_answer():
    current = st.session_state.words[st.session_state.index]
    correct_answer = current[0]

    if st.session_state.current_answer.strip() == correct_answer:
        feedback = f"<span style='color:green;'>✅ Correct! +1 point (Total: {st.session_state.score + 1})</span>"
        st.session_state.score += 1
        st.session_state.history.append(
            f"<b>{current[1]}</b><br><pre>{st.session_state.current_extra}</pre>➔ {st.session_state.current_answer.strip()} {feedback}<br><br>"
        )
        st.session_state.index += 1
    else:
        feedback = f"<span style='color:red;'>❌ Wrong! (Correct answer: {correct_answer}) -1 point (Total: {st.session_state.score - 1})</span>"
        st.session_state.score -= 1
        st.session_state.history.append(
            f"<b>{current[1]}</b><br><pre>{st.session_state.current_extra}</pre>➔ {st.session_state.current_answer.strip()} {feedback}<br><br>"
        )

    st.session_state.current_answer = ""  # clear the input
    st.rerun()

st.title("📚 Spanish Quiz - Terminal Mode")

# Check if the quiz is finished
if st.session_state.index >= len(st.session_state.words):
    st.success("🎉 You've finished the quiz!")
    st.write(f"Final Score: {st.session_state.score}")
else:
    current = st.session_state.words[st.session_state.index]

    # Prepare extra text
    if len(current) > 2:
        extra = current[2].replace(current[0], "_______")
        extra_parts = extra.split("  -- ")
        extra_text = "\n -- ".join(extra_parts[1:]) if len(extra_parts) > 1 else ""
    else:
        extra_text = ""

    st.session_state.current_extra = extra_text

    # Show full history first (terminal style)
    for entry in st.session_state.history:
        st.markdown(entry, unsafe_allow_html=True)

    # Show current question
    st.markdown(f"**{current[1]}**")
    if extra_text:
        st.markdown(f"<pre>{extra_text}</pre>", unsafe_allow_html=True)

    # Input field that triggers on Enter
    st.text_input(
        "Type your answer here:",
        key="current_answer",
        on_change=submit_answer,
    )
