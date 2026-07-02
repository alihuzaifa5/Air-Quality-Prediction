import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import CITY_BASELINES

def show():
    st.title("🏙️ Pakistani City Baselines")
    st.caption("Average pollution levels across major Pakistani cities.")

    col1, col2 = st.columns(2)
    with col1:
        city1 = st.selectbox("City 1", list(CITY_BASELINES.keys()), index=0)
    with col2:
        city2 = st.selectbox("City 2", list(CITY_BASELINES.keys()), index=1)

    d1 = CITY_BASELINES[city1]
    d2 = CITY_BASELINES[city2]

    st.markdown("---")
    st.subheader(f"📊 {city1} vs {city2} Comparison")

    pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO"]
    vals1 = [d1[p] for p in pollutants]
    vals2 = [d2[p] for p in pollutants]

    fig = go.Figure(data=[
        go.Bar(name=city1, x=pollutants, y=vals1, marker_color="#e53935"),
        go.Bar(name=city2, x=pollutants, y=vals2, marker_color="#1e88e5")
    ])
    fig.update_layout(barmode="group", height=350, yaxis_title="μg/m³",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Side by Side")
    cols = st.columns(len(pollutants))
    for i, p in enumerate(pollutants):
        with cols[i]:
            diff = d1[p] - d2[p]
            st.metric(label=p, value=d1[p], delta=f"{diff:+.0f} vs {city2}", delta_color="inverse")

    st.markdown("---")
    st.subheader("🗺️ All Cities Overview")
    rows = [{"City": c, **v} for c, v in CITY_BASELINES.items()]
    overview_df = pd.DataFrame(rows)

    fig2 = px.bar(overview_df, x="City", y="PM2.5", color="PM2.5", color_continuous_scale="Reds",
                  title="PM2.5 Levels Across Pakistani Cities", labels={"PM2.5": "PM2.5 (μg/m³)"})
    fig2.update_layout(height=300, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.info("🌍 WHO safe limit for PM2.5: **15 μg/m³ annual average**. All major Pakistani cities exceed this limit significantly.")

    st.markdown("---")
    st.subheader("📊 Full Data Table")
    st.dataframe(overview_df, use_container_width=True)