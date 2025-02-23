import streamlit as st
import requests

# Set GNews API Key
GNEWS_API_KEY = "30a594ce31cb03e5764697ef4f434ea2"

st.set_page_config(page_title="Follow Sources", layout="wide")

# Inject custom CSS for styling
st.markdown(
    """
    <style>
        /* General Background & Text Colors */
        body, .stApp {
            background-color: #fbfbfe;
            color: #050315;
        }
        
        /* Sidebar */
        .stSidebar {
            background-color: #a4abe3 !important;
        }

        /* Headings */
        h1, h2, h3 {
            color: #3865ac;
            text-align: center;
        }
        
        /* Category Cards */
        .category-card {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
            text-align: center;
            height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
        }
        .category-card:hover {
            transform: scale(1.05);
        }
        .category-card img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 10px;
        }
        .category-title {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }
        .stButton>button {
            margin-top: 10px;
            border: 2px solid transparent;
            color: black;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .stButton>button:hover {
            color: #3645ce !important;
            border-color: #3645ce !important;
        }
        
        .stButton>button:active {
            background-color: #3645ce !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Define news categories with images
news_categories = {
    "Sports": {
        "image": "https://www.york.ac.uk/media/study-new/undergraduate/sports-800-a.jpg",
        "gnews_category": "sports"
    },
    "Technology": {
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiZpiBhcf_hRwa3au0EgTUCQWVxsie4bm7sQ&s",
        "gnews_category": "technology"
    },
    "Business": {
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0iXiVHxJdepZ9PormoKMWyP-9oWCnqkXrkw&s",
        "gnews_category": "business"
    },
    "Entertainment": {
        "image": "https://media.licdn.com/dms/image/v2/C5112AQEJSWWLM3Dfew/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1558698380931?e=2147483647&v=beta&t=HUxgol0YCqqtE8QXZFuO3XTvFQxohFb-hQsqShqU6NY",
        "gnews_category": "entertainment"
    },
    "Health": {
        "image": "https://www.oecd.org/adobe/dynamicmedia/deliver/dm-aid--cd32a437-49ab-47f3-abec-a6022d2aa510/future-of-health-systems-shutterstock-2256248491.jpg?preferwebp=true&quality=80",
        "gnews_category": "health"
    },
    "Science": {
        "image": "https://www.oecd.org/adobe/dynamicmedia/deliver/dm-aid--81da1bba-5e45-46df-9741-33c6113a84d1/a8d820bd-en.jpg?preferwebp=true&quality=80",
        "gnews_category": "science"
    },
}

# Initialize session state
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "followed_sources" not in st.session_state:
    st.session_state.followed_sources = set()

def fetch_sources(category):
    """Fetch unique news sources from GNews API for the selected category."""
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&apikey={GNEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return sorted(set(article["source"]["name"] for article in articles if "source" in article))
    return []

# Display Categories as Clickable Cards
if st.session_state.selected_category is None:
    st.title("Follow News Sources")
    st.write("### Select a Category to View News Sources")

    columns = st.columns(3)  # 3 Column Grid Layout

    for idx, (category, details) in enumerate(news_categories.items()):
        with columns[idx % 3]:
            st.markdown(
                f"""
                <div class="category-card">
                    <img src="{details['image']}" width="100%" style="border-radius: 10px;">
                    <div class="category-title">{category}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"View {category}", key=f"btn_{category}"):
                st.session_state.selected_category = category
                st.rerun()

# Show News Sources when a Category is Selected
else:
    category = st.session_state.selected_category
    st.subheader(f"News Sources for {category}")

    sources = fetch_sources(news_categories[category]["gnews_category"])

    if sources:
        for source in sources:
            followed = source in st.session_state.followed_sources
            button_label = "Unfollow" if followed else "Follow"

            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🔹 {source}")

            with col2:
                if st.button(button_label, key=source):
                    if followed:
                        st.session_state.followed_sources.remove(source)
                    else:
                        st.session_state.followed_sources.add(source)
                    st.rerun()
    else:
        st.warning("No sources found. Try another category.")

    if st.button("⬅ Back to Categories"):
        st.session_state.selected_category = None
        st.rerun()

st.write("### Followed Sources")
if st.session_state.followed_sources:
    st.write(", ".join(st.session_state.followed_sources))
else:
    st.warning("You haven't followed any sources yet.")

if st.button("Save Preferences"):
    st.success("Your sources have been updated!")
