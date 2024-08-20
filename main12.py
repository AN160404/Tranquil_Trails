import streamlit as st

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
        st.write("# Search Tool Content")
        
    elif tool_page == "History":
        st.write("# History Tool Content")

if __name__ == "__main__":
    main()
