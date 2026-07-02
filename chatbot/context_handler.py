from database.db import get_predictions

def get_history_summary():
    df = get_predictions()
    if df.empty or len(df) < 2:
        return "You have not made enough predictions yet to analyze a trend."

    recent = df.head(7)
    labels = recent["prediction"].tolist()
    count = len(labels)
    last = labels[0]
    first = labels[-1]

    order = {"Good": 0, "Moderate": 1, "Poor": 2, "Hazardous": 3}
    trend = "stable"
    if order.get(last, 0) > order.get(first, 0):
        trend = "worsening"
    elif order.get(last, 0) < order.get(first, 0):
        trend = "improving"

    summary = (
        f"Based on your last {count} predictions, "
        f"air quality has been {trend}. "
        f"Most recent prediction: {last}. "
        f"Predictions: {', '.join(reversed(labels))}."
    )
    return summary

def build_prediction_context(last_prediction: dict):
    if not last_prediction:
        return ""
    return (
        f"The user's most recent prediction was: {last_prediction.get('label', 'Unknown')} "
        f"with {last_prediction.get('confidence', 0)}% confidence. "
        f"Feature importances: {last_prediction.get('importances', {})}."
    )