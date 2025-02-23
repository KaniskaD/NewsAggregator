import streamlit as st
import requests

# Set Streamlit page config
st.set_page_config(page_title="Search News", layout="wide")

st.title("Search News")

# Custom styling
st.markdown(
    """
    <style>
        body {
            background-color: #fbfbfe;
            color: #050315;
        }
        h1, h2, h3 {
            color: #0849af;
        }
        .stTextInput > div > div > input {
            background-color: #dedcff;
            color: #050315;
            border-radius: 5px;
            padding: 10px;
        }
        .stButton>button {
            background: linear-gradient(#0849af, #dedcff);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
        }
        /* Sidebar */
        .stSidebar {
            background-color: #a4abe3;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# GNews API Configuration (Replace with your actual API key)
API_KEY = "30a594ce31cb03e5764697ef4f434ea2"  # 🔹 Replace with your GNews API key
NEWS_API_URL = "https://gnews.io/api/v4/search"

# Search bar
query = st.text_input("Search for news articles")

# If the user enters a query, fetch news
if query:
    st.subheader(f"Results for: {query}")

    # API request parameters
    params = {
        "q": query,
        "token": API_KEY,
        "lang": "en",  
        "max": 5,  
        "sortby": "publishedAt"  
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])

        if articles:
            for article in articles:
                st.write(f"**[{article['title']}]({article['url']})**")
                st.write(f"{article['source']['name']} | {article['publishedAt'][:10]}")
                 
                st.write("---")
        else:
            st.write("No articles found. Try a different search.")
    else:
        st.write("Error fetching news. Please try again later.")
