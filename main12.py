import streamlit as st

# Define a function to render the main app
def main():
    st.title("Tranquil Trails")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigate",
        ["About", "Search", "Image Search", "History"]
    )
    
    if page == "About":
        st.write("## About")
        st.write("This app helps you explore various content including YouTube videos, Reddit posts, and image descriptions.")
        
    elif page == "Search":
        from pages.search import search_page
        search_page()
        
    elif page == "Image Search":
        from pages.image_search import image_search_page
        image_search_page()
        
    elif page == "History":
        from pages.history import history_page
        history_page()

if __name__ == "__main__":
    main()
