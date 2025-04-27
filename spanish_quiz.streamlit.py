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
    st.session_state.history = []  # For terminal-style display

st.title("📚 Spanish Quiz - Terminal Mode")

# Check if the quiz is finished
if st.session_state.index >= len(st.session_state.words):
    st.success("🎉 You've finished the quiz!")
    st.write(f"Final Score: {st.session_state.score}")
else:
    current = st.session_state.words[st.session_state.index]

    # Prepare the extra context
    if len(current) > 2:
        extra = current[2].replace(current[0], "_______")
        extra_parts = extra.split("  -- ")
        extra_text = "\n -- ".join(extra_parts[1:])
    else:
        extra_text = ""

    # Show the full history
    for entry in st.session_state.history:
        st.markdown(entry, unsafe_allow_html=True)

    # Show the current question
    st.markdown(f"**{current[1]}**")
    if extra_text:
        st.markdown(f"<pre>{extra_text}</pre>", unsafe_allow_html=True)

    answer = st.text_input("Type your answer here:")

    if st.button("Submit"):
        if answer.strip() == current[0]:
            feedback = f"<span style='color:green;'>✅ Correct! +1 point (Total: {st.session_state.score + 1})</span>"
            st.session_state.score += 1
            st.session_state.history.append(f"<b>{current[1]}</b> ➔ {answer.strip()} {feedback}")
            st.session_state.index += 1
        else:
            feedback = f"<span style='color:red;'>❌ Wrong! (Correct answer: {current[0]}) -1 point (Total: {st.session_state.score - 1})</span>"
            st.session_state.score -= 1
            st.session_state.history.append(f"<b>{current[1]}</b> ➔ {answer.strip()} {feedback}")
            # Optionally, you can append the wrong answers somewhere

        st.experimental_rerun()  # Refresh to simulate terminal scroll


