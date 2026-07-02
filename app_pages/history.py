import streamlit as st
import plotly.express as px
from database.db import get_predictions

def show():
    st.title("📊 Prediction History")

    df = get_predictions()

    if df.empty:
        st.info("No prediction history yet. Make a prediction first.")
        return

    col1, col2 = st.columns(2)
    with col1:
        cities = ["All"] + list(df["city"].dropna().unique())
        city_filter = st.selectbox("Filter by City", cities)
    with col2:
        categories = ["All"] + list(df["prediction"].unique())
        cat_filter = st.selectbox("Filter by Category", categories)

    filtered = df.copy()
    if city_filter != "All":
        filtered = filtered[filtered["city"] == city_filter]
    if cat_filter != "All":
        filtered = filtered[filtered["prediction"] == cat_filter]

    st.markdown(f"Showing **{len(filtered)}** records")

    st.subheader("📈 AQI Trend Over Time")
    plot_df = filtered.head(30).copy().iloc[::-1]
    label_order = {"Good": 0, "Moderate": 1, "Poor": 2, "Hazardous": 3}
    plot_df["level"] = plot_df["prediction"].map(label_order)

    color_map = {"Good": "#00e400", "Moderate": "#ffff00", "Poor": "#ff7e00", "Hazardous": "#7e0023"}
    fig = px.scatter(plot_df, x="timestamp", y="level", color="prediction", color_discrete_map=color_map)
    fig.update_yaxes(tickvals=[0, 1, 2, 3], ticktext=["Good", "Moderate", "Poor", "Hazardous"])
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌫️ Pollutant Trends")
    poll_choice = st.selectbox("Select Pollutant", ["pm25", "pm10", "no2", "so2", "co"])
    fig2 = px.line(plot_df, x="timestamp", y=poll_choice, markers=True,
                    labels={"timestamp": "Date", poll_choice: poll_choice.upper()})
    fig2.update_layout(height=250)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 All Records")
    st.dataframe(
        filtered[["timestamp", "city", "prediction", "confidence",
                  "pm25", "pm10", "no2", "so2", "co",
                  "temperature", "humidity", "proximity", "population_density"]].rename(columns={
            "timestamp": "Time", "city": "City", "prediction": "Result", "confidence": "Conf %",
            "pm25": "PM2.5", "pm10": "PM10", "no2": "NO2", "so2": "SO2", "co": "CO",
            "temperature": "Temp", "humidity": "Humidity",
            "proximity": "Proximity", "population_density": "Pop. Density"
        }),
        use_container_width=True
    )

    csv = filtered.to_csv(index=False)
    st.download_button("⬇️ Download as CSV", data=csv, file_name="air_quality_history.csv", mime="text/csv")