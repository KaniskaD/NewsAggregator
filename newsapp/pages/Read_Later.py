import streamlit as st

st.set_page_config(page_title="Read Later", layout="wide")
st.markdown(
    """ 
    <style>
    /* Buttons */
    .center-container {
        display: flex;
        justify-content: center;
    }
    .stButton>button {
        background-color: #3645ce !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        font-size: 16px !important;
    }
    /* Sidebar */
    .stSidebar {
        background-color: #a4abe3;
    }
    </style>
    """,unsafe_allow_html=True
)
st.title("Read Later")
st.write("Saved articles for reading later will be listed here.")

# Initialize session state for saved articles
if "read_later" not in st.session_state:
    st.session_state.read_later = []

# Show saved articles
if st.session_state.read_later:
    for idx, article in enumerate(st.session_state.read_later):
        st.subheader(f"🔹 {article['title']}")
        st.write(f"**Published:** {article['publishedAt'][:10]}")
        st.write(f"**Source:** {article['source']}")
        st.markdown(f"[Read full article]({article['url']})")

        # Remove Button
        if st.button(f"🗑 Remove", key=f"remove_{idx}"):
            st.session_state.read_later.pop(idx)
            st.rerun()

        st.markdown("---")
else:
    st.warning("No saved articles yet. Go to 'Today's News' to add articles!")

# Clear All Button
if st.button("🗑 Clear All"):
    st.session_state.read_later = []
    st.success("All saved articles removed!")
    st.rerun()
