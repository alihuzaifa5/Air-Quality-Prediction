import streamlit as st
from database.db import init_db
import importlib.util

st.set_page_config(page_title="AirSense Pakistan", page_icon="🌫️", layout="wide")

init_db()

pages = {
    "🏠 Dashboard":        "app_pages/dashboard.py",
    "🔍 Predict":          "app_pages/prediction.py",
    "📊 History":          "app_pages/history.py",
    "🏙️ City Baselines":  "app_pages/city_baselines.py",
    "🤖 AI Assistant":     "app_pages/chatbot.py",
    "📈 Model Analytics":  "app_pages/model_analytics.py",
    "ℹ️ About":            "app_pages/about.py",
}

with st.sidebar:
    st.title("🌫️ AirSense Pakistan")
    st.markdown("---")
    choice = st.radio("Navigation", list(pages.keys()))

page_file = pages[choice]
spec = importlib.util.spec_from_file_location("page", page_file)
page = importlib.util.module_from_spec(spec)
spec.loader.exec_module(page)
page.show()