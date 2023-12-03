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

    # Mérési adatok kiolvasása
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    now = datetime.now() #Dátum alapértelmezett módon
    formatted_date= now.strftime("%Y-%m-%d %H:%M:%S") #Dátum formázása é-h-n ó:p:mp módon
    now=formatted_date

    # Adatok adatbázisba helyezése
    if humidity is not None and temperature is not None:
        cursor.execute("INSERT INTO meresek (datum, homerseklet, paratartalom) VALUES (?, ?, ?)", (now, temperature, humidity))
        conn.commit()
    else:
        print('Szenzorolvasási hiba')

    # Adatok kiírása a képernyőre
    cursor.execute("SELECT * FROM meresek")
    records = cursor.fetchall()
    for record in records:
        id, datum, homerseklet, paratartalom = record
        print(f"ID: {id}, Dátum: {datum}, Hőmérséklet: {homerseklet:.1f} °C, Páratartalom: {paratartalom:.1f} %")

    # Adatbázis kapcsolat lezárása
    conn.close()
    # Adatok exportálása CSV fájlba
    with open('exported_data.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Fejléc hozzáadása
        csv_writer.writerow(["ID", "Dátum", "Hőmérséklet (°C)", "Páratartalom (%)"])

        # Adatok CSV-be írása
        csv_writer.writerows(records)

    # CSV fájl bezárása
    csv_file.close()

    # Adatok beolvasása a CSV fájlból és automatikusan be is záródik a kapcsolat
    with open('exported_data.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Ugrás a fejléc fölé
        data = list(csv_reader)

    # Adatok kinyerése az oszlopokból
    dates = [row[1] for row in data]
    temperatures = [float(row[2]) for row in data]
    humidities = [float(row[3]) for row in data]
    # Vonaldiagramm létrehozása
    plt.figure(figsize=(12, 6))
    plt.plot(dates, temperatures, label='Hőmérséklet (°C)', marker='o', linestyle='-', color='b')
    plt.plot(dates, humidities, label='Páratartalom (%)', marker='o', linestyle='-', color='g')

    # Grafikon beállítások, X tengely forgatása
    plt.title('Hőmérséklet és Páratartalom')
    plt.xlabel('Dátum')
    plt.xticks(rotation=45)
    plt.ylabel('Érték')
    plt.legend()

    # Grafikon megjelenítése
    plt.tight_layout()
    plt.show(block=False)  # Itt a block=False lehetővé teszi a folyamatos futást
    plt.pause(30)  # 30 másodperc szünet

    plt.close()  # Bezárja a grafikont
