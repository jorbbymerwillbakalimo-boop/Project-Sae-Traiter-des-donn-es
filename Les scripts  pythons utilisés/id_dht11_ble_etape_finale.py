#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Projet final IR + DHT11 + BLE + Historique

Touches :
- Touche 1 (code 22) : Image
- Touche 2 (code 25) : GUI intérieure (temp/hum)
- Touche 3 (code 13) : Scan BLE (temp/hum ext)
- Touche 4 (code 12) : Historique des mesures (capteurs.log)
"""

import evdev
import os
import sys
import time
import asyncio
from datetime import datetime
import tkinter as tk

try:
    from bleak import BleakScanner
    HAVE_BLEAK = True
except ImportError:
    HAVE_BLEAK = False

# ---------------------------------------------------------------------------
# Codes des touches
# ---------------------------------------------------------------------------

CODE_IMG  = 22   # touche 1
CODE_TEMP = 25   # touche 2
CODE_BLE  = 13   # touche 3
CODE_HIST = 12   # touche 4

IMAGE_FILE = "infraimage.png"
GUI_FILE   = "gui_temp_hum.py"
LOG_FILE   = "capteurs.log"

last_code = None
last_time = 0
ANTI_SPAM = 0.5  # secondes

SEUIL_TEMP = 25.0
SEUIL_HUM  = 70


# ---------------------------------------------------------------------------
# IR SETUP
# ---------------------------------------------------------------------------

def get_ir_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    print("Périphériques détectés :")
    for d in devices:
        print(f" - {d.path} - {d.name}")
        if d.name == "gpio_ir_recv":
            print("\n✅ Using device", d.path, "\n")
            return d
    print("❌ No device 'gpio_ir_recv' found !")
    sys.exit(1)


# ---------------------------------------------------------------------------
# IMAGE
# ---------------------------------------------------------------------------

def show_image():
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ Image '{IMAGE_FILE}' introuvable.")
        return
    print("📷 Affichage image...")
    os.system(f"feh -F --auto-zoom -Y '{IMAGE_FILE}'")
    print("Retour au programme.\n")


# ---------------------------------------------------------------------------
# GUI INTERIEURE
# ---------------------------------------------------------------------------

def launch_gui(mode):
    if not os.path.exists(GUI_FILE):
        print(f"❌ GUI '{GUI_FILE}' introuvable.")
        return
    print(f"🖼 Lancement GUI '{mode}'...")
    os.system(f"python3 {GUI_FILE} {mode}")
    print("Retour au programme.\n")


# ---------------------------------------------------------------------------
# BLE PARSING + LOGGING
# ---------------------------------------------------------------------------

def parse_data(name):
    if not name or "|" not in name:
        return None
    parts = name.split("|")
    if len(parts) >= 3:
        try:
            nom = parts[0].strip()
            temp = float(parts[1].strip())
            hum  = float(parts[2].strip())
            return {"nom": nom, "temp": temp, "hum": hum}
        except:
            return None
    return None


def save_to_file(data):
    timestamp = datetime.now().isoformat()
    entry = f"{timestamp} | {data['nom']} | {data['temp']}°C | {data['hum']}%"
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
    print(f"✓ Enregistré : {entry}")


def check_seuil(data):
    if data['temp'] > SEUIL_TEMP:
        print(f"🚨 Temp trop élevée : {data['temp']}°C (> {SEUIL_TEMP}°C)")
    if data['hum'] > SEUIL_HUM:
        print(f"🚨 Humidité trop élevée : {data['hum']}% (> {SEUIL_HUM}%)")


async def scan_ble_once():
    if not HAVE_BLEAK:
        print("❌ bleak non installé : sudo pip3 install bleak")
        return

    print("\n🔵 Scan BLE (5s)...")
    devices = await BleakScanner.discover(timeout=5.0)
    found = False

    for dev in devices:
        if dev.name:
            data = parse_data(dev.name)
            if data:
                found = True
                print(f"Balise trouvée : {dev.address} → {data}")
                save_to_file(data)
                check_seuil(data)
                print("-" * 40)

    if not found:
        print("Aucune balise BLE trouvée.\n")


def lancer_ble_scan():
    try:
        asyncio.run(scan_ble_once())
    except Exception as e:
        print("Erreur BLE :", e)


# ---------------------------------------------------------------------------
# HISTORIQUE (TOUCHE 4)
# ---------------------------------------------------------------------------

def show_history():
    """Affiche capteurs.log dans une fenêtre Tkinter."""
    print("\n📚 Affichage de l'historique...\n")

    # fenêtre Tkinter simple
    win = tk.Tk()
    win.title("Historique des mesures")
    win.minsize(600, 400)

    text = tk.Text(win, font=("Courier", 12))
    text.pack(expand=True, fill="both")

    if not os.path.exists(LOG_FILE):
        text.insert("end", "Aucun historique trouvé (capteurs.log manquant).")
    else:
        with open(LOG_FILE, "r") as f:
            contenu = f.read()
            if contenu.strip() == "":
                text.insert("end", "Historique vide.")
            else:
                text.insert("end", contenu)

    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=10)

    win.mainloop()


# ---------------------------------------------------------------------------
# MAIN LOOP (TELECOMMANDE)
# ---------------------------------------------------------------------------

def main():
    global last_code, last_time

    device = get_ir_device()

    print("\nTélécommande prête :")
    print("- Touche 1 → Image")
    print("- Touche 2 → GUI Temp./Hum int.")
    print("- Touche 3 → Scan BLE ext.")
    print("- Touche 4 → Historique (capteurs.log)\n")

    try:
        for event in device.read_loop():
            code = event.value
            now = time.time()

            # Anti-spam
            if code == last_code and (now - last_time) < ANTI_SPAM:
                continue

            last_code = code
            last_time = now

            if code == CODE_IMG:
                print("\n➡ Touche 1 : Image")
                show_image()

            elif code == CODE_TEMP:
                print("\n➡ Touche 2 : GUI Temp/Hum intérieur")
                launch_gui("temp")

            elif code == CODE_BLE:
                print("\n➡ Touche 3 : Scan BLE extérieur")
                lancer_ble_scan()

            elif code == CODE_HIST:
                print("\n➡ Touche 4 : Historique")
                show_history()

    except KeyboardInterrupt:
        print("\n🛑 Arrêt du programme.")
        sys.exit(0)


if __name__ == "__main__":
    main()

