import streamlit as st
from chatbot.chatbot_engine import search
from chatbot.context_handler import get_history_summary, build_prediction_context
from database.db import save_chat, get_chat_history

OFF_TOPIC = (
    "I am designed to answer questions about air quality, pollution, "
    "health advice, and this AI prediction system. "
    "I cannot help with unrelated topics."
)

def get_answer(question: str):
    result, score = search(question)

    if result is None:
        return OFF_TOPIC

    answer = result["answer"]

    if "HISTORY_CONTEXT" in answer:
        answer = get_history_summary()

    why_keywords = ["why", "reason", "cause", "explain prediction", "what caused"]
    if any(w in question.lower() for w in why_keywords):
        last = st.session_state.get("last_prediction", None)
        if last:
            ctx = build_prediction_context(last)
            answer = ctx + " " + answer

    return answer

def show():
    st.title("🤖 AirSense AI Assistant")
    st.caption("Ask me about pollution, health, cities, or this project.")

    st.markdown("**Quick Questions:**")
    cols = st.columns(3)
    quick = [
        "What is PM2.5?",
        "Why is Lahore polluted?",
        "What should I do if air is Hazardous?",
        "How does Random Forest work?",
        "What is my air quality trend?",
        "What is smog?"
    ]
    for i, q in enumerate(quick):
        if cols[i % 3].button(q, key=f"quick_{i}"):
            st.session_state["quick_input"] = q

    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        history = get_chat_history()
        for _, row in history.iterrows():
            st.session_state.messages.append({"role": row["role"], "content": row["message"]})

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your question here...")
    if "quick_input" in st.session_state:
        user_input = st.session_state.pop("quick_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        save_chat("user", user_input)
        with st.chat_message("user"):
            st.write(user_input)

        answer = get_answer(user_input)

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_chat("assistant", answer)
        st.rerun()