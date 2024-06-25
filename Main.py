import streamlit as st
from helper3 import get_qa_chain, create_vector_db

# Set up the page configuration with an aesthetic that follows an Indian-inspired theme
st.set_page_config(
    page_title="TRANQUIL TRAILS Q&A",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define theme colors
background_color = "#F2EFEA"  # Light beige
accent_color = "#FF6B6B"  # Coral red
text_color = "#1A1A1D"  # Charcoal black
button_color = "#FF6B6B"  # Coral red
button_color_grey = "#A9A9A9"  # Grey
description_color = "#4B4B4B"  # Darker grey for visibility

# Apply custom styles to the page for aesthetics
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+New+Zealand&display=swap" rel="stylesheet">
    <style>
    .reportview-container {
        background-color: #F2EFEA;
        color: #1A1A1D;
    }
    .stTextInput>div>div>input {
        background-color: #F2EFEA;
        color: #1A1A1D;
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        margin-bottom: 0px !important; /* Remove bottom margin */
        text-align: left; /* Align text input to the left */
    }
    .stButton>button {
        color: #F2EFEA;
        background-color: #FF6B6B;
        border-radius: 5px;
    }
    .stButton>button.submit-button {
        background-color: #FF6B6B;
    }
    .stButton>button.history-button {
        background-color: #FF6B6B;
    }
    .stButton>button.history-button-toggled {
        background-color: #A9A9A9;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    h1 {
        font-family: 'Playfair New Zealand', serif;
        font-weight: 400;
        font-size: 50px;
        color: #FF6B6B;
        text-align: center;
    }
    p {
        font-size: 18px;
        font-family: 'Poppins', sans-serif;
        color: #4B4B4B;
        margin-bottom: 20px; /* Adjust margin bottom for descriptive text */
    }
    .descriptive-text {
        text-align: center; /* Center justify the descriptive text */
        margin-bottom: 20px; /* Add margin bottom to the descriptive text */
        font-size:20px;
    }
    .ask-question-text {
        text-align: left; /* Align ask question text to the left */
        margin-bottom: 0px; /* Adjust margin bottom for ask question text */
        font-size:15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the page title and description
st.markdown("<h1>TRANQUIL TRAILS</h1>", unsafe_allow_html=True)
st.markdown("<p class='descriptive-text'><i>\"Uniting scenic travel and mindful cuisine to nurture body, mind, and spirit in calm locales.\"</i></p>", unsafe_allow_html=True)

# Initialize session state for conversation history if it does not exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Initialize session state for showing/hiding conversation history
if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

# Text input for the user's question
st.markdown("<p class='ask-question-text'>Ask a Question:</p>", unsafe_allow_html=True)
question = st.text_input("", "", key="question_input")

# Function to handle the query and update history
def handle_query(query):
    chain = get_qa_chain()
    response = chain(query)
    st.session_state['history'].append((query, response['result']))  # Assuming response returns a dictionary with 'result' key
    return response['result']

# Container for the submit button
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("Submit", key="submit", use_container_width=True):
        response = handle_query(question)
        st.header("Answer")
        st.markdown(f"<p style='font-size: 18px;'>{response}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Button to toggle conversation history display
history_button_label = "History" if st.session_state['show_history'] else "History"
history_button_class = "history-button-toggled" if st.session_state['show_history'] else "history-button"

# Container for the history button below the answer
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button(history_button_label, key="toggle_history", use_container_width=True):
        st.session_state['show_history'] = not st.session_state['show_history']
    st.markdown("</div>", unsafe_allow_html=True)

# Display the conversation history if the state is True
if st.session_state['show_history']:
    st.subheader("Conversation History")
    for idx, (q, ans) in enumerate(st.session_state['history'], start=1):
        st.markdown(f"**Q{idx}:** {q}", unsafe_allow_html=True)
        st.markdown(f"**A{idx}:** {ans}", unsafe_allow_html=True)
