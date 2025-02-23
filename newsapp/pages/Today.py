import streamlit as st
import requests

st.set_page_config(page_title="Today's News", layout="wide")

# Custom Styling
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

st.title("Today's News")
st.write("Latest personalized news articles from your followed sources.")

# Retrieve followed sources from session state
if "followed_sources" not in st.session_state:
    st.session_state.followed_sources = set()

followed_sources = st.session_state.followed_sources

if not followed_sources:
    st.warning("You are not following any sources. Go to 'Follow Sources' to select your interests.")
else:
    st.write(f"Fetching news from: **{', '.join(followed_sources)}**")

    # GNews API Setup
    API_KEY = "30a594ce31cb03e5764697ef4f434ea2"  # Replace with your actual API key
    BASE_URL = "https://gnews.io/api/v4/search"

    all_articles = []

    for source in followed_sources:
        params = {
            "q": source,  # Fetch news related to this source
            "token": API_KEY,
            "lang": "en",
            "max": 5  # Limit to 5 articles per source
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            news_data = response.json().get("articles", [])
            all_articles.extend(news_data)
        else:
            st.error(f"⚠️ Error fetching news from {source}. Please try again later.")

    # Display News Articles
    if all_articles:
        # Initialize session state for saved articles
        if "read_later" not in st.session_state:
            st.session_state.read_later = []

        # Display News Articles
        if all_articles:
            for article in all_articles:
                st.subheader(f"{article['title']}")
                st.write(f"{article['source']['name']}, {article['publishedAt'][:10]}")
                st.markdown(f"[Read more]({article['url']})")

                # Save for Later Button
                if st.button("Save for Later", key=f"save_{article['title']}"):
                    if article not in st.session_state.read_later:
                        st.session_state.read_later.append({
                            "title": article["title"],
                            "publishedAt": article["publishedAt"],
                            "source": article["source"]["name"],
                            "url": article["url"]
                        })
                        st.success("Article saved to 'Read Later'!")

                st.markdown("---")

    else:
        st.write("No recent articles found.")

# Refresh Button
if st.button("Refresh News"):
    st.rerun()
