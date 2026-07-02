import streamlit as st

def show():
    st.title("ℹ️ About This Project")

    st.markdown("""
    ## 🌫️ AirSense Pakistan
    **AI-Powered Air Quality Decision Support System**

    ---

    ### 🎯 Project Purpose
    AirSense Pakistan predicts air quality categories from pollution sensor data
    using machine learning. It provides health recommendations, historical analysis,
    city comparisons, and an intelligent AI assistant — all running completely offline.

    ---

    ### 🤖 Machine Learning
    | Component | Detail |
    |-----------|--------|
    | Algorithm | Random Forest Classifier |
    | Also Compared | Decision Tree, Logistic Regression, KNN |
    | Features | PM2.5, PM10, NO2, SO2, CO, Temperature, Humidity, Proximity to Industrial Areas, Population Density |
    | Output | Good / Moderate / Poor / Hazardous |
    | Evaluation | Accuracy, Precision, Recall, F1, Confusion Matrix |
    | Validation | 5-Fold Cross Validation |

    ---

    ### 📦 Technology Stack
    | Layer | Technology |
    |-------|-----------|
    | Frontend | Streamlit |
    | ML Library | Scikit-learn |
    | Charts | Plotly |
    | Database | SQLite |
    | AI Chatbot | TF-IDF + Knowledge Base |
    | Model Storage | Pickle |

    ---

    ### 🗂️ Modules
    1. **Live Prediction** — Enter sensor values, get instant AQI prediction
    2. **Explainable AI** — Feature importance shows why the model predicted that result
    3. **History Tracking** — Every prediction saved with trends and graphs
    4. **City Baselines** — Compare pollution levels across Pakistani cities
    5. **AI Assistant** — Offline chatbot answering air quality questions
    6. **Model Analytics** — Full evaluation metrics and confusion matrix

    ---

    ### 👨‍💻 Team
    Ahmad Aziz (Team Lead) · Muhammad Ali · Huzaifa · Muhammad Fahad
    4th Semester — Artificial Intelligence
    """)