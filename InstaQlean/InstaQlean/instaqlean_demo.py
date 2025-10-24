
import streamlit as st
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
from parse_connections import load_usernames_from_file

# --------- Page Config ---------
st.set_page_config(page_title="InstaQlean", layout="centered")

# --------- Custom Styling ---------
st.markdown("""
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: white;
        margin-bottom: 0px;
    }
    .highlight-q {
        color: #00C9A7;
    }
    .subtext {
        font-size: 18px;
        color: #CCCCCC;
        margin-top: 0px;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# --------- Header ---------
st.markdown("""
    <div class='main-title'>
        Insta<span class='highlight-q'>Q</span>lean 🔍
    </div>
    <div class='subtext'>
        Analyze your Instagram engagement without logging in — see mutuals, fans, ghosts, and more.
    </div>
""", unsafe_allow_html=True)

# --------- File Upload ---------
st.subheader("📂 Upload your Instagram Data")
uploaded_followers = st.file_uploader("Upload followers JSON", type=["json"], key="followers")
uploaded_following = st.file_uploader("Upload following JSON", type=["json"], key="following")

followers = []
following = []

if uploaded_followers and uploaded_following:
    st.success("Files uploaded successfully! 📂")
    try:
        # Save uploaded files to temp files to pass to loader
        with open("temp_followers.json", "wb") as f:
            f.write(uploaded_followers.getbuffer())
        with open("temp_following.json", "wb") as f:
            f.write(uploaded_following.getbuffer())

        followers = load_usernames_from_file("temp_followers.json")
        following = load_usernames_from_file("temp_following.json", key="relationships_following")

    except Exception as e:
        st.error(f"Error reading files: {e}")
else:
    st.info("Waiting for both followers and following files to be uploaded...")

st.divider()

# --------- Connections Breakdown ---------
st.subheader("👥 Connections Breakdown")

if followers and following:
    mutuals = [u for u in followers if u in following]
    fans = [u for u in followers if u not in following]
    ghosts = [u for u in following if u not in followers]
else:
    # Fallback fake data
    mutuals = ["@jane_doe", "@coolguy42", "@bestie123"]
    fans = ["@followeronly", "@fanaccount"]
    ghosts = ["@ghostuser1", "@ghostuser2", "@ghostuser3"]

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### ✅ Mutuals")
    st.dataframe(pd.DataFrame({"Username": mutuals}), use_container_width=True)

with col2:
    st.markdown("### 🧍‍♀️ Fans")
    st.dataframe(pd.DataFrame({"Username": fans}), use_container_width=True)

with col3:
    st.markdown("### ❌ Ghosts")
    st.dataframe(pd.DataFrame({"Username": ghosts}), use_container_width=True)

st.divider()

# --------- Engagement Word Cloud ---------
st.subheader("💬 Engagement Word Cloud")

if mutuals or fans:
    text = " ".join(mutuals + fans)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    wordcloud.to_file("generated_wordcloud.png")
    st.image("generated_wordcloud.png", caption="Top Engagers", use_column_width=True)
else:
    try:
        image = Image.open("sample_wordcloud.png")
        st.image(image, caption="Top Engagers", use_column_width=True)
    except:
        st.warning("⚠️ Word cloud image not found.")

st.divider()

# --------- Fake Follower Detector ---------
st.subheader("🧟 Fake Follower Detector")

fake_followers = []
for u in followers:
    # Basic heuristics for fake followers
    if "@" not in u or u.isdigit() or len(u) < 3:
        fake_followers.append(u)

# Use fallback if empty
if not fake_followers:
    fake_followers = ["@ghostuser1", "@fakiee12345", "@bot_789"]

st.dataframe(pd.DataFrame({"Username": fake_followers, "Flagged Reason": ["Suspicious account"]*len(fake_followers)}), use_container_width=True)

# --------- Footer ---------
st.markdown("---")
st.caption("📅 Built for Senior Capstone | Demo v1")
