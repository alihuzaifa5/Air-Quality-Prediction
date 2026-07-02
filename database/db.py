import sqlite3
import pandas as pd
from datetime import datetime
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        city TEXT,
        pm25 REAL, pm10 REAL, no2 REAL, so2 REAL, co REAL,
        temperature REAL, humidity REAL,
        proximity REAL, population_density REAL,
        prediction TEXT,
        confidence REAL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        role TEXT,
        message TEXT
    )''')

    conn.commit()
    conn.close()

def save_prediction(city, inputs, prediction, confidence):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO predictions
        (timestamp, city, pm25, pm10, no2, so2, co, temperature, humidity,
         proximity, population_density, prediction, confidence)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (datetime.now().strftime("%Y-%m-%d %H:%M"),
         city,
         inputs["PM2.5"], inputs["PM10"], inputs["NO2"], inputs["SO2"], inputs["CO"],
         inputs["Temperature"], inputs["Humidity"],
         inputs["Proximity_to_Industrial_Areas"], inputs["Population_Density"],
         prediction, confidence))
    conn.commit()
    conn.close()

def get_predictions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM predictions ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def save_chat(role, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (timestamp, role, message) VALUES (?,?,?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M"), role, message))
    conn.commit()
    conn.close()

def get_chat_history():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM chat_history ORDER BY timestamp ASC", conn)
    conn.close()
    return df