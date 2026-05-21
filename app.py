import streamlit as st

# 设置网页标题和图标
st.set_page_config(page_title="Belajar Mandarin / Learn Chinese", layout="wide", page_icon="🇨🇳")

# 定义多语言翻译字典 (英语 / 印尼语)
LANG_DICT = {
    "English": {
        "title": "Welcome to Chinese Learning Platform! 🚀",
        "subtitle": "Your friendly companion to master Mandarin Chinese.",
        "choose_lang": "Choose your explanation language:",
        "features": "What do you want to learn today?",
        "card_1": "🗣️ Pinyin & Tones",
        "card_2": "🗂️ Vocabulary Flashcards",
        "card_3": "💬 Daily Conversations"
    },
    "Bahasa Indonesia": {
        "title": "Selamat Datang di Platform Belajar Bahasa Mandarin! 🚀",
        "subtitle": "Teman setia Anda untuk menguasai Bahasa Mandarin dengan mudah.",
        "choose_lang": "Pilih bahasa pengantar:",
        "features": "Apa yang ingin Anda pelajari hari ini?",
        "card_1": "🗣️ Pinyin & Nada",
        "card_2": "🗂️ Kartu Kosakata (Flashcards)",
        "card_3": "💬 Percakapan Sehari-hari"
    }
}

# 在侧边栏让用户选择语言
selected_lang = st.sidebar.selectbox("Language / Bahasa", ["English", "Bahasa Indonesia"])

# 根据选择的语言，获取对应的文字内容
text = LANG_DICT[selected_lang]

# --- 网页前端界面渲染 ---
st.title(text["title"])
st.subheader(text["subtitle"])

st.write("---")

st.markdown(f"### {text['features']}")

# 创建三列布局，展示未来的功能板块
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.write(text["card_1"])
        st.button("Buka / Open", key="btn1")

with col2:
    with st.container(border=True):
        st.write(text["card_2"])
        st.button("Buka / Open", key="btn2")

with col3:
    with st.container(border=True):
        st.write(text["card_3"])
        st.button("Buka / Open", key="btn3")