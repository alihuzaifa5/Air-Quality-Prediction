import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv("data/air_quality.csv")

feature_cols = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Temperature", "Humidity",
                 "Proximity_to_Industrial_Areas", "Population_Density"]
target_col = "Air Quality"

df = df[feature_cols + [target_col]].dropna()

le = LabelEncoder()
df[target_col] = le.fit_transform(df[target_col])

X = df[feature_cols]
y = df[target_col]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

models = {
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree":       DecisionTreeClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "KNN":                 KNeighborsClassifier(n_neighbors=5)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        "model": model,
        "accuracy":  round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred, average="weighted") * 100, 2),
        "recall":    round(recall_score(y_test, y_pred, average="weighted") * 100, 2),
        "f1":        round(f1_score(y_test, y_pred, average="weighted") * 100, 2),
        "confusion_matrix": confusion_matrix(y_test, y_pred)
    }
    print(f"{name}: Accuracy={results[name]['accuracy']}%")

best_model_name = max(results, key=lambda x: results[x]["accuracy"])
best_model = results[best_model_name]["model"]

package = {
    "model": best_model,
    "scaler": scaler,
    "label_encoder": le,
    "feature_cols": feature_cols,
    "results": {k: {m: v for m, v in r.items() if m != "model"} for k, r in results.items()},
    "best_model_name": best_model_name
}

with open("model/model.pkl", "wb") as f:
    pickle.dump(package, f)

print(f"\nBest Model: {best_model_name}")
print("Model saved to model/model.pkl")