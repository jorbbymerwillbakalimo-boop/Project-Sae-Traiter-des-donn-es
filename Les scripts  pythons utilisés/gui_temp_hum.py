#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Interface graphique Tkinter pour afficher les mesures du DHT11 (GPIO12)
et préparer l'affichage futur d'un capteur BLE.

Usage :
    python3 gui_temp_hum.py          -> mode normal
    python3 gui_temp_hum.py temp     -> mise en avant de la température
    python3 gui_temp_hum.py hum      -> mise en avant de l'humidité
"""

import sys
import tkinter as tk
import board
import adafruit_dht

# ---------------------------------------------------------------------------
# 1) Configuration du capteur DHT11
# ---------------------------------------------------------------------------

dht_device = adafruit_dht.DHT11(board.D12)
dernier_temp = None
dernier_hum = None

MODE = "normal"
if len(sys.argv) >= 2 and sys.argv[1].lower() in ("temp", "hum"):
    MODE = sys.argv[1].lower()


# ---------------------------------------------------------------------------
# 2) Lecture des capteurs
# ---------------------------------------------------------------------------

def lire_dht():
    global dernier_temp, dernier_hum
    try:
        t = dht_device.temperature
        h = dht_device.humidity
        if t is not None and h is not None:
            dernier_temp, dernier_hum = t, h
            return t, h
    except Exception:
        pass
    return None, None


def lire_ble():
    """Préparation pour BLE, retour vide pour l'instant."""
    return None, None


# ---------------------------------------------------------------------------
# 3) Mise à jour GUI
# ---------------------------------------------------------------------------

def mettre_a_jour():
    temp, hum = lire_dht()

    if temp is not None:
        label_temp_val.config(text=f"{temp:.1f} °C")
        label_hum_val.config(text=f"{hum:.1f} %")
        label_status.config(text="Lecture DHT11 OK", fg="green")
    else:
        if dernier_temp is not None:
            label_temp_val.config(text=f"{dernier_temp:.1f} °C")
            label_hum_val.config(text=f"{dernier_hum:.1f} %")
            label_status.config(text="Erreur DHT11 (valeurs précédentes)", fg="orange")
        else:
            label_status.config(text="Aucune mesure disponible", fg="red")

    # BLE (désactivé pour le moment)
    label_temp_ble.config(text="-- °C")
    label_hum_ble.config(text="-- %")

    fenetre.after(2000, mettre_a_jour)


# ---------------------------------------------------------------------------
# 4) Interface Tkinter
# ---------------------------------------------------------------------------

fenetre = tk.Tk()
fenetre.title("Station de mesure - Température & Humidité")
fenetre.minsize(460, 250)

font_title = ("Helvetica", 16, "bold")
font_label = ("Helvetica", 12)
font_value = ("Helvetica", 20, "bold")
font_status = ("Helvetica", 11, "italic")

# Titre
tk.Label(fenetre, text="Station météo intérieure / extérieure", font=font_title).pack(pady=8)

# Bloc intérieur
frame_int = tk.LabelFrame(fenetre, text=" Intérieur (DHT11 - GPIO12) ", font=font_label)
frame_int.pack(fill="x", padx=10, pady=5)

tk.Label(frame_int, text="Température :", font=font_label).grid(row=0, column=0, sticky="w")
label_temp_val = tk.Label(frame_int, text="-- °C", font=font_value)
label_temp_val.grid(row=0, column=1, sticky="e", padx=10)

tk.Label(frame_int, text="Humidité :", font=font_label).grid(row=1, column=0, sticky="w")
label_hum_val = tk.Label(frame_int, text="-- %", font=font_value)
label_hum_val.grid(row=1, column=1, sticky="e", padx=10)

if MODE == "temp":
    label_temp_val.config(fg="blue")
elif MODE == "hum":
    label_hum_val.config(fg="blue")

# Bloc extérieur (BLE futur)
frame_ext = tk.LabelFrame(fenetre, text=" Extérieur (BLE - à venir) ", font=font_label)
frame_ext.pack(fill="x", padx=10, pady=5)

tk.Label(frame_ext, text="Température :", font=font_label).grid(row=0, column=0)
label_temp_ble = tk.Label(frame_ext, text="-- °C", font=font_value)
label_temp_ble.grid(row=0, column=1, padx=10)

tk.Label(frame_ext, text="Humidité :", font=font_label).grid(row=1, column=0)
label_hum_ble = tk.Label(frame_ext, text="-- %", font=font_value)
label_hum_ble.grid(row=1, column=1, padx=10)

# Status + Quitter
label_status = tk.Label(fenetre, text="En attente de lecture...", font=font_status)
label_status.pack(pady=8)

def quitter():
    try:
        dht_device.exit()
    except:
        pass
    fenetre.destroy()

tk.Button(fenetre, text="Fermer", command=quitter).pack(pady=5)

fenetre.after(1000, mettre_a_jour)
fenetre.mainloop()
