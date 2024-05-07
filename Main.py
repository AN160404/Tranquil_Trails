import streamlit as st
from helper import get_qa_chain, create_vector_db

# Set page title and background color
st.set_page_config(
    page_title="TRANQUIL TRAILS🍀",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define colors inspired by Indian culture
background_color = "#F2EFEA"  # Light beige
accent_color = "#FF6B6B"  # Coral red
text_color = "#1A1A1D"  # Charcoal black

# Set page background color
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {background_color};
        color: {text_color};
    }}
    .stTextInput>div>div>input {{
        background-color: {background_color};
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title with Indian-inspired font and centered alignment
st.markdown(
    "<h1 style='text-align: center; font-size: 50px; font-weight: bold; font-family: Poppins, sans-serif; color: #FF6B6B;'>TRANQUIL Trails</h1>",
    unsafe_allow_html=True
)

# Additional line below the title
st.markdown(
    "<p style='text-align: center; font-size: 18px; font-family: Georgia, serif;'>Uniting scenic travel and mindful cuisine to nurture body, mind, and spirit in calm locales.</p>",
    unsafe_allow_html=True
)

# Input field for questions with larger font size and width using markdown
st.markdown("<p style='font-size: 20px; width: 90%;'>Ask a Question:</p>", unsafe_allow_html=True)
question = st.text_input("", key="question_input")

if question:
    # Fetch response
    chain = get_qa_chain()
    response = chain(question)

    # Display answer
    st.header("Answer")
    st.markdown(f"<p style='font-size: 18px;'>{response['result']}</p>", unsafe_allow_html=True)

# Button to create knowledgebase
btn = st.button("Create Knowledgebase", key="create_kb")
if btn:
    create_vector_db()
