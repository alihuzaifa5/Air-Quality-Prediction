import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from model.predict import predict_air_quality, get_feature_importance
from database.db import save_prediction
from config import CITY_BASELINES

def show():
    st.title("🔍 Air Quality Prediction")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Enter Sensor Values")

        city = st.selectbox("Select City (optional)",
                           ["Manual Input"] + list(CITY_BASELINES.keys()))

        defaults = CITY_BASELINES.get(city, {}) if city != "Manual Input" else {}

        pm25  = st.slider("PM2.5 (μg/m³)",  0.0, 300.0, float(defaults.get("PM2.5", 50.0)))
        pm10  = st.slider("PM10 (μg/m³)",   0.0, 400.0, float(defaults.get("PM10", 80.0)))
        no2   = st.slider("NO2 (μg/m³)",    0.0, 100.0, float(defaults.get("NO2", 30.0)))
        so2   = st.slider("SO2 (μg/m³)",    0.0, 100.0, float(defaults.get("SO2", 20.0)))
        co    = st.slider("CO (ppm)",       0.0, 20.0,  float(defaults.get("CO", 4.0)))
        temp  = st.slider("Temperature (°C)", -10.0, 60.0, float(defaults.get("Temperature", 25.0)))
        humid = st.slider("Humidity (%)",   0.0, 100.0, float(defaults.get("Humidity", 50.0)))
        prox  = st.slider("Proximity to Industrial Areas (km)", 0.0, 20.0, float(defaults.get("Proximity_to_Industrial_Areas", 5.0)))
        pop   = st.slider("Population Density (per km²)", 0, 1500, int(defaults.get("Population_Density", 500)))

    inputs = {
        "PM2.5": pm25, "PM10": pm10, "NO2": no2, "SO2": so2, "CO": co,
        "Temperature": temp, "Humidity": humid,
        "Proximity_to_Industrial_Areas": prox, "Population_Density": pop
    }

    with col2:
        st.subheader("Prediction Result")

        if st.button("🔍 Predict Air Quality", use_container_width=True):
            result = predict_air_quality(inputs)
            importances = get_feature_importance()

            st.session_state["last_prediction"] = {
                "label": result["label"],
                "confidence": result["confidence"],
                "importances": importances,
                "inputs": inputs
            }

            save_prediction(city, inputs, result["label"], result["confidence"])

            st.markdown(f"""
            <div style="background-color:{result['color']}22; border-left: 5px solid {result['color']};
                        padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h2 style="color:{result['color']}; margin:0;">
                    {result['emoji']} {result['label']}
                </h2>
                <p style="font-size:18px; margin:5px 0;">
                    Confidence: <b>{result['confidence']}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result["confidence"],
                title={"text": "Confidence %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": result["color"]},
                    "steps": [
                        {"range": [0, 50],  "color": "#ffcccc"},
                        {"range": [50, 75], "color": "#ffe0b2"},
                        {"range": [75, 100],"color": "#c8e6c9"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=30, b=0))
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.subheader("💊 Health Recommendations")
            for tip in result["advice"]:
                st.success(f"✓ {tip}")

            st.subheader("🔬 Why This Prediction? (XAI)")
            if importances:
                fig_imp = px.bar(
                    x=list(importances.values()),
                    y=list(importances.keys()),
                    orientation="h",
                    color=list(importances.values()),
                    color_continuous_scale="Reds",
                    labels={"x": "Importance", "y": "Feature"}
                )
                fig_imp.update_layout(
                    height=320,
                    margin=dict(t=10, b=10),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_imp, use_container_width=True)

            st.markdown("---")
            st.info("💬 Go to the **AI Assistant** page and ask: \"Why was my prediction hazardous?\" for a detailed explanation.")