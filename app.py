import streamlit as st

st.set_page_config(page_title="Belajar Mandarin", layout="wide", page_icon="🇨🇳")

# 专门针对印尼人的中文学习界面
LANG_DICT = {
    "Bahasa Indonesia": {
        "title": "Selamat Datang di Platform Belajar Bahasa Mandarin! 🚀",
        "subtitle": "Teman setia Anda untuk menguasai Bahasa Mandarin dengan mudah.",
        "features": "Apa yang ingin Anda pelajari hari ini?",
        "card_1": "🗣️ Pinyin & Nada (Tones)",
        "card_2": "🗂️ Kartu Kosakata (Flashcards)",
        "card_3": "💬 Percakapan Sehari-hari",
        "btn": "Buka"
    },
    "English": {
        "title": "Welcome to Chinese Learning Platform! 🚀",
        "subtitle": "Your friendly companion to master Mandarin Chinese.",
        "features": "What do you want to learn today?",
        "card_1": "🗣️ Pinyin & Tones",
        "card_2": "🗂️ Vocabulary Flashcards",
        "card_3": "💬 Daily Conversations",
        "btn": "Open"
    }
}

selected_lang = st.sidebar.selectbox("Pilih Bahasa Pengantar / Language", ["Bahasa Indonesia", "English"])
text = LANG_DICT[selected_lang]

st.title(text["title"])
st.subheader(text["subtitle"])
st.write("---")
st.markdown(f"### {text['features']}")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.write(text["card_1"])
        st.button(text["btn"], key="btn1")
with col2:
    with st.container(border=True):
        st.write(text["card_2"])
        st.button(text["btn"], key="btn2")
with col3:
    with st.container(border=True):
        st.write(text["card_3"])
        st.button(text["btn"], key="btn3")