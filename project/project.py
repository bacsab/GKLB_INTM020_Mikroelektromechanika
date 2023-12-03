import Adafruit_DHT #Szenzor felismeréséhez szükséges
import sqlite3 #Adatbázis létrehozásához szükséges
import csv #Adatbázis CSV-be exportálásához szükséges
import matplotlib.pyplot as plt #Grafikon megjelenítéséhez szükséges
from datetime import datetime #Dátum és idő kezeléséhez szükséges

import time #Időzítés használatához szükséges

# Szenzor típusa és csatlakozás
sensor = Adafruit_DHT.DHT22
pin = 4  # Példa: 4-es GPIO tüske


while True:
    # Adatbázis csatlakozás
    conn = sqlite3.connect('szenzor_adatok.db')
    cursor = conn.cursor()

    # Ellenőrizze, hogy a tábla már létezik-e, és csak akkor hozza létre, ha még nem létezik
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meresek'")
    if cursor.fetchone() is None:
        cursor.execute('''
            CREATE TABLE meresek (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datum TIMESTAMP,
                homerseklet REAL,
                paratartalom REAL
            )
        ''')
