import streamlit as st

def history_page():
    st.subheader("Conversation History")
    if 'history' in st.session_state:
        for idx, (q, ans) in enumerate(st.session_state['history'], start=1):
            st.markdown(f"**Q{idx}:** {q}", unsafe_allow_html=True)
            st.markdown(f"**A{idx}:** {ans}", unsafe_allow_html=True)
    else:
        st.write("No history available.")
