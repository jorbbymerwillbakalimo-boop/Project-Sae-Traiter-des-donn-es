#!/usr/bin/env python3
import asyncio
from bleak import BleakScanner
from datetime import datetime
import os

# Fichier de log
LOG_FILE = "capteurs.log"

# Seuils (change-les si besoin)
SEUIL_TEMP = 25.0  # °C
SEUIL_HUM = 70     # %

def parse_data(name):
    """Parse le nom de la balise : nom|temp|hum"""
    if not name or "|" not in name:
        return None
    parts = name.split("|")
    if len(parts) >= 3:
        try:
            nom = parts[0].strip()
            temp = float(parts[1].strip())
            hum = float(parts[2].strip())
            return {"nom": nom, "temp": temp, "hum": hum}
        except ValueError:
            return None
    return None

def save_to_file(data):
    """Enregistre avec timestamp dans capteurs.log"""
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp} | {data['nom']} | {data['temp']}°C | {data['hum']}%"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")
    print(f"Données enregistrées : {log_entry}")

def check_seuil(data):
    """Affiche un message si seuil dépassé"""
    if data['temp'] > SEUIL_TEMP:
        print(f"🚨 ALERTE : Température trop élevée sur {data['nom']} : {data['temp']}°C (> {SEUIL_TEMP}°C)")
    if data['hum'] > SEUIL_HUM:
        print(f"🚨 ALERTE : Humidité trop élevée sur {data['nom']} : {data['hum']}% (> {SEUIL_HUM}%)")

async def main():
    print("Scan BLE en cours... (Ctrl+C pour arrêter)")
    print(f"Seuils : Temp > {SEUIL_TEMP}°C ou Hum > {SEUIL_HUM}% → Alerte")
    print(f"Données sauvées dans {LOG_FILE}\n")

    while True:
        devices = await BleakScanner.discover(timeout=5.0)  # Scan 5 secondes
        trouve = False
        for device in devices:
            if device.name:  # Si nom présent
                data = parse_data(device.name)
                if data:
                    trouve = True
                    print(f"Balise trouvée : {device.address} → {data['nom']}")
                    save_to_file(data)
                    check_seuil(data)
                    print("-" * 50)

        if not trouve:
            print("Aucune balise trouvée ce tour...")

        await asyncio.sleep(3)  # Pause 3 secondes entre scans

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du scan.")
