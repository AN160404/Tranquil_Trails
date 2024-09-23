import streamlit as st
from app import get_qa_chain, create_vector_db  # Import the necessary functions from app.py
from review import search_youtube
from gtts import gTTS
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd

def main():
    st.set_page_config(page_title="Tranquil Trails", layout="wide")
    
    # Header
    st.title("TRANQUIL TRAILS")
    
    # Sidebar sections
    st.sidebar.write("**Reports**")
    page = st.sidebar.radio("", ["Dashboard", "Bug reports", "System alerts"], index=0)
    
    st.sidebar.write("**Tools**")
    tool_page = st.sidebar.radio("", ["Search", "History"], index=0)
    
    # Content based on sidebar selection
    if page == "Dashboard":
        st.write("# Dashboard Content")
        
    elif page == "Bug reports":
        st.write("# Bug Reports Content")
        
    elif page == "System alerts":
        st.write("# System Alerts Content")
        
    if tool_page == "Search":
        search_page()  # Call the search page function when "Search" is selected
        
    elif tool_page == "History":
        st.write("# History Tool Content")

def search_page():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    def save_query_with_suggestions(query, suggestions):
        file_path = "unknown_queries.xlsx"
        engine = 'openpyxl'
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path, engine=engine)
            except Exception as e:
                print(f"Error reading the Excel file: {e}")
                df = pd.DataFrame(columns=["Query", "Suggestions"])
        else:
            df = pd.DataFrame(columns=["Query", "Suggestions"])
            
        new_data = pd.DataFrame({"Query": [query], "Suggestions": [suggestions]})
        df = pd.concat([df, new_data], ignore_index=True)
        
        try:
            df.to_excel(file_path, index=False, engine=engine)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving the Excel file: {e}")

    def handle_query(query):
        try:
            chain = get_qa_chain()
            response = chain.invoke(query)
            return response
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return f"Error in processing the query: {str(e)}"

    def handle_youtube_search(api_key, query):
        results = search_youtube(api_key, query)
        return results

    def text_to_audio(text):
        tts = gTTS(text=text, lang='en')
        temp_audio_file = "temp_audio.mp3"
        tts.save(temp_audio_file)
        
        with open(temp_audio_file, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
        
        os.remove(temp_audio_file)

    def handle_search(query):
        # Ensure vector DB is created before processing
        create_vector_db()  # Call the create_vector_db function here

        if "reddit" in query.lower() or "reviews" in query.lower():
            st.write("I don't know.")
        elif "youtube" in query.lower():
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
        else:
            # Use the QA chain to handle regular queries
            response = handle_query(query)
            st.header("Answer")
            st.markdown(f"<p style='font-size: 18px; font-family: Poppins, sans-serif; color: #4B4B4B; margin-bottom: 20px;'>{response}</p>", unsafe_allow_html=True)
            text_to_audio(response)
            st.session_state['history'].append((query, response))

            if response.lower().strip() == "i don't know.":
                suggestions = st.text_input("I don't know the answer. Please help expand our data.")
            
            if st.button("Submit Suggestions"):
                save_query_with_suggestions(str(query), str(suggestions))
                st.success("Your suggestions have been saved.")

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
    st.markdown("<p style='text-align:center; font-size: 25px;'><i>\"Uniting scenic travel and mindful cuisine to nurture body, mind, and spirit in calm locales.\"</i></p>", unsafe_allow_html=True)

    
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

if __name__ == "__main__":
    main()
