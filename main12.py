import streamlit as st
# Set up the page configuration
st.set_page_config(
    page_title="TRANQUIL TRAILS Q&A",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import asyncio
from reddit import fetch_reddit_data
from app import get_qa_chain, create_vector_db
from review import search_youtube
import os
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the API key is available
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key is missing. Please check your .env file.")


# Define a function to run the fetch_reddit_data coroutine
def run_fetch(query):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_reddit_data(query))

# Define theme colors and apply custom styles to the page
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+New+Zealand&display=swap" rel="stylesheet">
    <style>
    .descriptive-text{
    text-align:center;
    }
    .ask-question-text{
     margin:0px;
    }
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
        text-align: left;
    }
    .stButton>button {
        color: #F2EFEA;
        background-color: #FF6B6B;
        border-radius: 5px;
        padding: 10px;
        font-size: 18px;
    }
    .stButton.full-width > button {
        width: 100%;
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
        margin-bottom: 20px;
    }
    .button-container {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for conversation history and show/hide toggle
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

# Page navigation using selectbox
selected_page = st.sidebar.selectbox("Navigate", ["About", "Search", "Image Search", "History"])

# Function to handle the Q&A chain
def handle_query(query):
    chain = get_qa_chain()
    response = chain(query)
    st.session_state['history'].append((query, response['result']))
    return response['result']

# Function to handle YouTube search
def handle_youtube_search(api_key, query):
    results = search_youtube(api_key, query)
    return results

# Function to handle Reddit search
def handle_reddit_search(query):
    urls = run_fetch(query)
    return urls

# Function to convert text to audio
def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)
    
    with open(temp_audio_file, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    
    os.remove(temp_audio_file)

# Function to handle the image description generation
def generate_image_description(image_data, model, prompt="Guess this place and give a detailed description for this place"):
    image1 = {'mime_type': 'image/jpeg', 'data': image_data}
    response = model.generate_content([prompt, image1])
    return response.text

# Function to handle the search queries
def handle_search(query):
    create_vector_db()

    if "youtube" in query.lower():
        youtube_api_key = 'AIzaSyAYvoBvpWrvCrH5QTk0NGq11p5PUMtWevc'
        try:
            results = handle_youtube_search(youtube_api_key, query)
            if results:
                st.write(f"Top {len(results)} results for '{query}':")
                for i, result in enumerate(results, start=1):
                    st.write(f"**Result {i}:**")
                    st.write(f"**Title:** {result['title']}")
                    st.write(f"**Description:** {result['description']}")
                    st.write(f"[Watch Video]({result['video_url']})")
                    st.image(result['thumbnail_url'])
                    st.write("---")
                st.session_state['history'].append((query, f"YouTube results for '{query}'"))
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"An error occurred during YouTube search: {e}")

    elif "reddit" in query.lower():
        urls = handle_reddit_search(query)
        if urls:
            st.write(f"Top results for '{query}':")
            st.write("Post URLs:")
            for url in urls:
                st.write(url)
            st.session_state['history'].append((query, f"Reddit results for '{query}'"))
        else:
            st.warning("No results found.")

    else:
        response = handle_query(query)
        st.header("Answer")
        st.markdown(f"<p style='font-size: 18px;'>{response}</p>", unsafe_allow_html=True)
        text_to_audio(response)
        st.session_state['history'].append((query, response))

# Function to handle image description
def handle_image_description(uploaded_file):
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", width=400)
        image_data = uploaded_file.read()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        generated_text = generate_image_description(image_data, model)
        st.markdown("### Generated Description")
        st.markdown(f"<p>{generated_text}</p>", unsafe_allow_html=True)
        text_to_audio(generated_text)

# Page content based on selected option
if selected_page == "About":
    st.markdown("<h2>About</h2>", unsafe_allow_html=True)
    st.markdown("This app helps you explore various content including YouTube videos, Reddit posts, and image descriptions.")

elif selected_page == "Search":
    st.markdown("<p class='ask-question-text'>Enter your query:</p>", unsafe_allow_html=True)
    user_query = st.text_input("", "", key="user_query")

    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("Submit Query", key="submit_query", use_container_width=True):
        handle_search(user_query)
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_page == "Image Search":
    st.markdown("<p class='ask-question-text'>Upload Image:</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        handle_image_description(uploaded_file)

elif selected_page == "History":
    st.subheader("Conversation History")
    for idx, (q, ans) in enumerate(st.session_state['history'], start=1):
        st.markdown(f"**Q{idx}:** {q}", unsafe_allow_html=True)
        st.markdown(f"**A{idx}:** {ans}", unsafe_allow_html=True)
