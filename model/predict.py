import pickle
import numpy as np
from config import AQI_LABELS, HEALTH_ADVICE

with open("model/model.pkl", "rb") as f:
    package = pickle.load(f)

model        = package["model"]
scaler       = package["scaler"]
le           = package["label_encoder"]
feature_cols = package["feature_cols"]

def predict_air_quality(inputs: dict):
    values = np.array([[inputs[f] for f in feature_cols]])
    scaled = scaler.transform(values)

    pred_encoded = model.predict(scaled)[0]
    proba        = model.predict_proba(scaled)[0]
    confidence   = round(max(proba) * 100, 1)

    label_name = le.inverse_transform([pred_encoded])[0]

    for k, (name, emoji, color) in AQI_LABELS.items():
        if name.lower() == label_name.lower():
            return {
                "label": name,
                "emoji": emoji,
                "color": color,
                "confidence": confidence,
                "advice": HEALTH_ADVICE[name]
            }

    return {
        "label": label_name,
        "emoji": "🔵",
        "color": "#0000ff",
        "confidence": confidence,
        "advice": []
    }

def get_feature_importance():
    if hasattr(model, "feature_importances_"):
        return dict(zip(feature_cols, model.feature_importances_))
    return {}