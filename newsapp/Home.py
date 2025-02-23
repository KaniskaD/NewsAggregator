import streamlit as st

st.set_page_config(page_title="Personalized News", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Background & Text Colors */
        body, .stApp {
            background-color: #f9f9fd;
            color: #03040a;
        }
        /* Headings */
        h1 {
            color: #3746cf;
            text-align: center;
        }
        /* Centered Description */
        .description {
            text-align: center;
            font-size: 18px;
            color: #03040a;
            margin-bottom: 20px;
        }
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
    """,
    unsafe_allow_html=True
)

st.title("Welcome to Personalized News Aggregator")

# Centered Description
st.markdown('<p class="description">Get real-time, customized news updates from sources you trust. Follow topics that interest you and stay informed!</p>', unsafe_allow_html=True)

# Centered Button
col1, col2, col3, col4 = st.columns([1, 2, 4, 1])
with col3:
    if st.button("Start Exploring"):
        st.switch_page("newsapp/pages/Follow_Sources.py")
