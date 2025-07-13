import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sudoku Prep", layout="centered")
st.title("Sudoku Prep")

# Session state to track which puzzle we’re on
if "puzzle_index" not in st.session_state:
    st.session_state.puzzle_index = 0

# Correct solutions hardcoded
solutions = [
    [  # Puzzle 1
        [2, 1, 5, 6, 4, 3],
        [3, 4, 6, 1, 5, 2],
        [1, 2, 3, 5, 6, 4],
        [6, 5, 4, 2, 3, 1],
        [4, 6, 2, 3, 1, 5],
        [5, 3, 1, 4, 2, 6]
    ],
    [  # Puzzle 2
        [5, 1, 4, 3, 6, 2],
        [3, 6, 2, 5, 1, 4],
        [1, 4, 3, 6, 2, 5],
        [6, 2, 5, 4, 3, 1],
        [2, 5, 6, 1, 4, 3],
        [4, 3, 1, 2, 5, 6]
    ]
]

# Use separate components for each puzzle
if st.session_state.puzzle_index == 0:
    sudoku = components.declare_component("sudoku1", path="sudoku1")
elif st.session_state.puzzle_index == 1:
    sudoku = components.declare_component("sudoku2", path="sudoku2")
else:
    st.balloons()
    st.success("🎉 All puzzles completed!")
    st.stop()

# Show Sudoku
board = sudoku()

# Check button
if board and st.button("Check Solution"):
    correct = solutions[st.session_state.puzzle_index]
    is_correct = board == correct

    if is_correct:
        st.success("✅ Correct!")
        st.session_state.puzzle_index += 1
        st.rerun()
    else:
        st.error("❌ Incorrect. Try again.")
