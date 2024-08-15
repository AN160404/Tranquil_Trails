import streamlit as st
import asyncio
from app import get_qa_chain, create_vector_db
from review import search_youtube
from reddit import fetch_reddit_data
from gtts import gTTS
import os
import google.generativeai as genai
from dotenv import load_dotenv



def search_page():
    load_dotenv()
    api_key = os.getenv("api_key")
    
    # Initialize the 'history' key in st.session_state if it doesn't exist
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Function to run the fetch_reddit_data coroutine
    def run_fetch(query):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(fetch_reddit_data(query))

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

    # Function to handle search queries
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
                st.write("Here's the response for debugging purposes:")
                st.write(results)  # Outputting the results for debugging

        elif "reviews" in query.lower():
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
            st.markdown(f"<p style='font-size: 18px; font-family: Poppins, sans-serif; color: #4B4B4B; margin-bottom: 20px;'>{response}</p>", unsafe_allow_html=True)
            text_to_audio(response)
            st.session_state['history'].append((query, response))

    # Add custom header
    st.markdown(
        """
        <h1 style='font-family: "Playfair New Zealand", serif; 
                   font-weight: 400; 
                   font-size: 50px; 
                   color: #FF6B6B; 
                   text-align: center;'>TRANQUIL TRAILS</h1>
        """, 
        unsafe_allow_html=True
    )
    
    # Add the search input box with description text below
    st.markdown("<p class='ask-question-text' style='font-size: 18px; font-family: Poppins, sans-serif; color: #4B4B4B; margin-bottom: 20px;'>Enter your query:</p>", unsafe_allow_html=True)
    user_query = st.text_input("", "", key="user_query")
    
    # Add examples below the search bar
    st.markdown(
        """
        <p style='font-size: 18px; font-family: "Poppins", sans-serif; color: #4B4B4B; margin-bottom: 20px;'>
        Examples:\n
        "Explain Spirituality of Goa in detail.",\n
        "Give a tour itinerary of Kashmir keeping in mind to experience every spiritual practice done over there",\n
        "Give some youtube vlogs for visit to Golden Temple."
        </p>
        """, 
        unsafe_allow_html=True
    )

    # Handle the search query submission
    if st.button("Submit Query", key="submit_query", use_container_width=True):
        handle_search(user_query)


search_page()

