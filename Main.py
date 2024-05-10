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

# Apply custom styles to the page for aesthetics
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
    .stButton>button {{
        color: {background_color};
        background-color: {accent_color};
        border-radius: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display the page title
st.markdown(
    "<h1 style='text-align: center; font-size: 50px; font-family: Poppins, sans-serif; color: {accent_color};'>TRANQUIL TRAILS Q&A 🌱</h1>",
    unsafe_allow_html=True
)

# Button to create the knowledge base
if st.button("Create Knowledgebase", key="create_kb"):
    create_vector_db()

# Initialize session state for conversation history if it does not exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Text input for the user's question
question = st.text_input("Ask a Question:", "", key="question_input")

# Function to handle the query and update history
def handle_query(query):
    chain = get_qa_chain()
    response = chain(query)
    st.session_state['history'].append((query, response['result']))  # Assuming response returns a dictionary with 'result' key
    return response['result']

# Display the response when a question is asked
if question:
    response = handle_query(question)
    st.header("Answer")
    st.markdown(f"<p style='font-size: 18px;'>{response}</p>", unsafe_allow_html=True)

# Display the conversation history
if st.session_state['history']:
    st.subheader("Conversation History")
    for idx, (q, ans) in enumerate(st.session_state['history'], start=1):
        st.markdown(f"**Q{idx}:** {q}", unsafe_allow_html=True)
        st.markdown(f"**A{idx}:** {ans}", unsafe_allow_html=True)
