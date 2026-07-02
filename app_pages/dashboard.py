import streamlit as st
import plotly.express as px
import pandas as pd
from database.db import get_predictions
from config import CITY_BASELINES

def show():
    st.title("🏠 AirSense Dashboard")

    df = get_predictions()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Predictions", len(df) if not df.empty else 0)
    with col2:
        st.metric("Latest Prediction", df.iloc[0]["prediction"] if not df.empty else "None yet")
    with col3:
        hazardous = len(df[df["prediction"] == "Hazardous"]) if not df.empty else 0
        st.metric("Hazardous Days", hazardous)
    with col4:
        good = len(df[df["prediction"] == "Good"]) if not df.empty else 0
        st.metric("Good Days", good)

    st.markdown("---")

    if df.empty:
        st.info("No predictions yet. Go to the Predict page to get started.")
        return

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Prediction Distribution")
        counts = df["prediction"].value_counts().reset_index()
        counts.columns = ["Category", "Count"]
        color_map = {"Good": "#00e400", "Moderate": "#ffff00", "Poor": "#ff7e00", "Hazardous": "#7e0023"}
        fig_pie = px.pie(counts, values="Count", names="Category", color="Category", color_discrete_map=color_map)
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("📈 Recent Trend")
        recent = df.head(10).copy().iloc[::-1]
        label_order = {"Good": 0, "Moderate": 1, "Poor": 2, "Hazardous": 3}
        recent["level"] = recent["prediction"].map(label_order)
        fig_trend = px.line(recent, x="timestamp", y="level", markers=True,
                             labels={"timestamp": "Date", "level": "AQI Level"})
        fig_trend.update_yaxes(tickvals=[0, 1, 2, 3], ticktext=["Good", "Moderate", "Poor", "Hazardous"])
        fig_trend.update_layout(height=300)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    st.subheader("🏙️ City Baseline Overview")

    city_data = [{"City": c, "PM2.5": v["PM2.5"], "PM10": v["PM10"]} for c, v in CITY_BASELINES.items()]
    city_df = pd.DataFrame(city_data)
    fig_city = px.bar(city_df, x="City", y=["PM2.5", "PM10"], barmode="group",
                       color_discrete_map={"PM2.5": "#e53935", "PM10": "#fb8c00"},
                       labels={"value": "μg/m³", "variable": "Pollutant"})
    fig_city.update_layout(height=300)
    st.plotly_chart(fig_city, use_container_width=True)

    st.markdown("---")
    st.subheader("🕐 Recent Predictions")
    st.dataframe(
        df[["timestamp", "city", "prediction", "confidence", "pm25", "pm10"]]
        .head(5)
        .rename(columns={"timestamp": "Time", "city": "City", "prediction": "Result",
                          "confidence": "Confidence %", "pm25": "PM2.5", "pm10": "PM10"}),
        use_container_width=True
    )