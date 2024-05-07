import streamlit as st
from helper3 import get_qa_chain, create_vector_db

# Set up the title of the web app
st.title("Codebasics Q&A 🌱")

# Button to create the knowledge base
btn = st.button("Create Knowledgebase")
if btn:
    create_vector_db()

# Initialize session state for history if it does not exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Input for user's question
question = st.text_input("Question: ")

# Function to handle the query and update history
def handle_query(query):
    chain = get_qa_chain()
    response = chain(query)
    st.session_state['history'].append((query, response['result']))  # Assuming response is a dictionary with 'result' key
    return response['result']

# Display the response when a question is asked
if question:
    response = handle_query(question)
    st.header("Answer")
    st.write(response)

# Display the conversation history
if st.session_state['history']:
    st.subheader("Conversation History")
    for idx, (q, ans) in enumerate((st.session_state['history']), start=1):
        st.write(f"Q{idx}: {q}")
        st.write(f"A{idx}: {ans}")


