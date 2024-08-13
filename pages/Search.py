import streamlit as st
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
api_key = os.getenv("GOOGLE_API_KEY")

def run_fetch(query):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_reddit_data(query))

def handle_query(query):
    chain = get_qa_chain()
    response = chain(query)
    st.session_state['history'].append((query, response['result']))
    return response['result']

def handle_youtube_search(api_key, query):
    results = search_youtube(api_key, query)
    return results

def handle_reddit_search(query):
    urls = run_fetch(query)
    return urls

def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)
    
    with open(temp_audio_file, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    
    os.remove(temp_audio_file)

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

def search_page():
    st.markdown("<p class='ask-question-text'>Enter your query:</p>", unsafe_allow_html=True)
    user_query = st.text_input("", "", key="user_query")

    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    if st.button("Submit Query", key="submit_query", use_container_width=True):
        handle_search(user_query)
    st.markdown("</div>", unsafe_allow_html=True)
