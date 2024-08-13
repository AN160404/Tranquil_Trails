import streamlit as st

def main():
    st.title("Tranquil Trails")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["About", "Search", "Image Search", "History"])
    
    if page == "About":
        from pages.about import about_page
        about_page()
        
    elif page == "Search":
        from pages.Search import search_page
        search_page()
        
    elif page == "Image Search":
        from pages.image_search import image_search_page
        image_search_page()
        
    elif page == "History":
        from pages.history import history_page
        history_page()

if __name__ == "__main__":
    main()
