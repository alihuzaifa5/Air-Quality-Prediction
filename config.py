APP_NAME = "AirSense Pakistan"
DB_PATH = "database/air_quality.db"

FEATURES = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Temperature", "Humidity",
            "Proximity_to_Industrial_Areas", "Population_Density"]

AQI_LABELS = {
    0: ("Good", "🟢", "#00e400"),
    1: ("Moderate", "🟡", "#ffff00"),
    2: ("Poor", "🟠", "#ff7e00"),
    3: ("Hazardous", "🔴", "#7e0023")
}

HEALTH_ADVICE = {
    "Good": [
        "Air quality is satisfactory.",
        "Outdoor activities are safe.",
        "No precautions needed."
    ],
    "Moderate": [
        "Sensitive groups should limit prolonged outdoor exertion.",
        "Keep windows open for ventilation.",
        "Monitor air quality updates."
    ],
    "Poor": [
        "Reduce prolonged outdoor activities.",
        "Wear a mask if going outside.",
        "Keep windows closed."
    ],
    "Hazardous": [
        "Stay indoors as much as possible.",
        "Wear N95 mask if you must go outside.",
        "Children and elderly must stay indoors.",
        "Avoid all outdoor exercise."
    ]
}

CITY_BASELINES = {
    "Lahore":     {"PM2.5": 98,  "PM10": 180, "NO2": 45, "SO2": 30, "CO": 8,  "Temperature": 28, "Humidity": 55, "Proximity_to_Industrial_Areas": 2.0, "Population_Density": 850},
    "Karachi":    {"PM2.5": 65,  "PM10": 120, "NO2": 38, "SO2": 22, "CO": 6,  "Temperature": 31, "Humidity": 70, "Proximity_to_Industrial_Areas": 3.5, "Population_Density": 900},
    "Peshawar":   {"PM2.5": 72,  "PM10": 140, "NO2": 35, "SO2": 25, "CO": 5,  "Temperature": 25, "Humidity": 45, "Proximity_to_Industrial_Areas": 4.0, "Population_Density": 600},
    "Islamabad":  {"PM2.5": 42,  "PM10": 85,  "NO2": 28, "SO2": 15, "CO": 3,  "Temperature": 24, "Humidity": 50, "Proximity_to_Industrial_Areas": 6.0, "Population_Density": 300},
    "Quetta":     {"PM2.5": 55,  "PM10": 105, "NO2": 30, "SO2": 18, "CO": 4,  "Temperature": 22, "Humidity": 35, "Proximity_to_Industrial_Areas": 5.5, "Population_Density": 250},
    "Multan":     {"PM2.5": 88,  "PM10": 160, "NO2": 42, "SO2": 28, "CO": 7,  "Temperature": 30, "Humidity": 50, "Proximity_to_Industrial_Areas": 2.5, "Population_Density": 700},
}