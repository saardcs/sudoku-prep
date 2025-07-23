import streamlit as st
import qrcode
import io
import streamlit.components.v1 as components

st.set_page_config(page_title="Sudoku Prep", layout="centered")
st.title("Sudoku Prep")

# Sidebar with QR code
st.sidebar.header("Scan This QR Code to View Menu Online")

qr_link = "https://sudoku-prep.streamlit.app"  # Replace with your actual URL
qr = qrcode.make(qr_link)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)

st.sidebar.image(buf, width=300, caption=qr_link)

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
    
    nickname = st.text_input("Enter your nickname:")
    roll_number = st.text_input("Enter your roll number:")
    
    if st.button("Submit Score"):
        if nickname.strip() and roll_number.strip():
            import gspread
            from google.oauth2.service_account import Credentials

            # Set up creds and open your sheet
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
            # Load credentials from Streamlit secrets
            service_account_info = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        
            client = gspread.authorize(creds)
            import datetime
        
            # Timestamp for filenames and sheets
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            try:
                sheet = client.open("Review").worksheet("Sudoku")
            except gspread.WorksheetNotFound:
                st.error("Worksheet not found. Please check your Google Sheet.")

            row = [roll_number.strip(), nickname.strip(), timestamp]
            sheet.append_row(row)
            st.success("✅ Score submitted!")
            # if st.button("🔁 Start Over"):
            #     st.session_state.index = 0
            #     st.session_state.score = 0
            #     st.session_state.correct_factors = False
            #     st.session_state.correct_gcd = None
            #     st.rerun()
        else:
            st.warning("Please enter your nickname and roll number.")
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
