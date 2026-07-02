import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pickle
import pandas as pd

def show():
    st.title("📈 Model Analytics")

    try:
        with open("model/model.pkl", "rb") as f:
            package = pickle.load(f)
    except FileNotFoundError:
        st.error("Model not found. Please run model/train_model.py first.")
        return

    results      = package["results"]
    best_name    = package["best_model_name"]
    feature_cols = package["feature_cols"]
    model        = package["model"]

    st.success(f"✅ Best Model: **{best_name}**")

    st.subheader("📊 Model Comparison")
    rows = [{"Model": name, "Accuracy %": m["accuracy"], "Precision %": m["precision"],
             "Recall %": m["recall"], "F1 Score %": m["f1"]} for name, m in results.items()]
    metrics_df = pd.DataFrame(rows).set_index("Model")
    st.dataframe(metrics_df.style.highlight_max(axis=0, color="#c8e6c9"), use_container_width=True)

    st.subheader("📊 Accuracy Comparison")
    fig_acc = px.bar(pd.DataFrame(rows), x="Model", y="Accuracy %", color="Accuracy %",
                      color_continuous_scale="Blues", text="Accuracy %")
    fig_acc.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_acc.update_layout(height=350, coloraxis_showscale=False, yaxis_range=[0, 105])
    st.plotly_chart(fig_acc, use_container_width=True)

    st.subheader("📊 F1 Score Comparison")
    fig_f1 = px.bar(pd.DataFrame(rows), x="Model", y="F1 Score %", color="F1 Score %",
                     color_continuous_scale="Greens", text="F1 Score %")
    fig_f1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_f1.update_layout(height=350, coloraxis_showscale=False, yaxis_range=[0, 105])
    st.plotly_chart(fig_f1, use_container_width=True)

    if hasattr(model, "feature_importances_"):
        st.subheader("🔬 Feature Importance (Random Forest)")
        importance_df = pd.DataFrame({
            "Feature": feature_cols, "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=True)
        fig_imp = px.bar(importance_df, x="Importance", y="Feature", orientation="h",
                          color="Importance", color_continuous_scale="Reds")
        fig_imp.update_layout(height=350, coloraxis_showscale=False)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.subheader(f"🔢 Confusion Matrix — {best_name}")
    cm = results[best_name]["confusion_matrix"]
    labels = package["label_encoder"].classes_.tolist()
    fig_cm = ff.create_annotated_heatmap(z=cm, x=labels, y=labels, colorscale="Blues", showscale=True)
    fig_cm.update_layout(height=400, xaxis_title="Predicted", yaxis_title="Actual")
    st.plotly_chart(fig_cm, use_container_width=True)

    st.markdown("---")
    st.subheader("📁 Dataset Info")
    col1, col2, col3 = st.columns(3)
    col1.metric("Features Used", len(feature_cols))
    col2.metric("Train/Test Split", "80% / 20%")
    col3.metric("Cross Validation", "5-Fold")

    st.markdown("**Features:** " + ", ".join(feature_cols))
    st.markdown("**Target:** Air Quality (Good, Moderate, Poor, Hazardous)")
    st.markdown("**Dataset Source:** Kaggle — Air Quality and Pollution Assessment")