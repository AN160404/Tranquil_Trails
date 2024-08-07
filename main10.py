import streamlit as st
import asyncio
from reddit import fetch_reddit_data
from helper3 import get_qa_chain, create_vector_db
from review import search_youtube
import os
import google.generativeai as genai
from gtts import gTTS
from hello import api_key

# Define a function to run the fetch_reddit_data coroutine
def run_fetch(query):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_reddit_data(query))

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
        margin-bottom: 0px !important;
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
    h2 {
        font-family: 'Playfair New Zealand', serif;
        font-weight: 400;
        font-size: 30px;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 10px;
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

# Function to handle the query and update history
def handle_query(query):
    chain = get_qa_chain()
    response = chain(query)
    st.session_state['history'].append((query, response['result']))  # Assuming response returns a dictionary with 'result' key
    return response['result']

# Function to handle YouTube search
def handle_youtube_search(api_key, query):
    results = search_youtube(api_key, query)
    return results

# Function to handle Reddit search
def handle_reddit_search(query):
    urls = run_fetch(query)
    return urls

# Function to convert text to audio and display it
def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)
    
    # Read the audio file and stream it
    with open(temp_audio_file, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    
    # Clean up the temporary audio file
    os.remove(temp_audio_file)

# Text input for the user's question
st.markdown("<p class='ask-question-text'>Ask a Question:</p>", unsafe_allow_html=True)
question = st.text_input("", "", key="question_input")

# Container for the submit button
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    submit_clicked = st.button("Submit", key="submit", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if submit_clicked:
    create_vector_db()
    if question:
        response = handle_query(question)
        st.header("Answer")
        st.markdown(f"<p style='font-size: 18px;'>{response}</p>", unsafe_allow_html=True)

        # Convert response text to audio and play it
        text_to_audio(response)

# Button to toggle conversation history display
history_button_label = "History" if not st.session_state['show_history'] else "Hide History"
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

# YouTube Search Functionality
st.header("YouTube Search")

def youtube_search():
    api_key = 'AIzaSyAYvoBvpWrvCrH5QTk0NGq11p5PUMtWevcABC'  # Replace with your actual API key

    # Get search query from user
    query = st.text_input("Enter search query for YouTube:", key="youtube_query")

    # Container for the Fetch YouTube Links button
    with st.container():
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        fetch_youtube_clicked = st.button("Fetch YouTube Links", key="fetch_youtube", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if fetch_youtube_clicked:
        if query:
            # Get search results
            results = handle_youtube_search(api_key, query)

            # Display the results
            if results:
                st.write(f"Top {len(results)} results for '{query}':")
                for i, result in enumerate(results, start=1):
                    st.write(f"**Result {i}:**")
                    st.write(f"**Title:** {result['title']}")
                    st.write(f"**Description:** {result['description']}")
                    st.write(f"[Watch Video]({result['video_url']})")
                    st.image(result['thumbnail_url'])
                    st.write("---")
            else:
                st.warning("No results found.")
        else:
            st.warning("Please enter a search query.")

youtube_search()

# Reddit Search Functionality
st.header("Reddit Search")

# Text input for Reddit search query
reddit_query = st.text_input("Enter search query for Reddit:", key="reddit_query")

# Container for the Fetch Reddit Data button
with st.container():
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    fetch_reddit_clicked = st.button("Fetch Reddit Data", key="fetch_reddit", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if fetch_reddit_clicked:
    if reddit_query:
        # Show a spinner while fetching data
        with st.spinner("Fetching Reddit data, please wait..."):
            urls = handle_reddit_search(reddit_query)

        # Display the results
        if urls:
            st.write(f"Top results for '{reddit_query}':")
            st.write("Post URLs:")
            for url in urls:
                st.write(url)
        else:
            st.warning("No results found.")
    else:
        st.warning("Please enter a search query.")

# Image Description Generator Functionality
st.header("Image Description Generator")

st.markdown("<p><i>\"Upload an image to get a description and listen to the generated text.\"</i></p>", unsafe_allow_html=True)

# Step 1: Authenticate and configure the API
os.environ['api_key'] = api_key
if not api_key:
    st.error("API key not found. Please set the environment variable 'GOOGLE_GENAI_API_KEY'.")
    st.stop()

genai.configure(api_key=api_key)

# Step 2: Allow user to upload an image
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", width=400)  # Adjust the width as needed

    # Read the image data
    image_data = uploaded_file.read()

    # Define the image object as required by the API
    image1 = {
        'mime_type': uploaded_file.type,
        'data': image_data
    }

    # Define the prompt
    prompt = "Guess this place and give a detailed description for this place"

    # Choose a model that's appropriate for your use case.
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate content (Assuming the model supports image input in this manner)
    response = model.generate_content([prompt, image1])

    # Extract the text from the response object
    generated_text = response.text  # Adjust this if 'text' is not the correct attribute

    # Display the generated text
    st.markdown("### Generated Description")
    st.markdown(f"<p>{generated_text}</p>", unsafe_allow_html=True)

    # Convert the generated text to audio and play it
    text_to_audio(generated_text)
