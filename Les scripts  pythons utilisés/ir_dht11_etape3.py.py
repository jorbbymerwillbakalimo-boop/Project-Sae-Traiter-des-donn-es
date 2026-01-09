#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
TP infrarouge – Étape 3
Télécommande IR + Capteur DHT11

- Touche 1 (code 22) : affiche l'image infraimage.png avec 'feh'
- Touche 2 (code 25) : affiche la TEMPERATURE et l'HUMIDITE
  mesurées par le DHT11 connecté sur le GPIO 12 (BCM)
"""

import evdev           # Pour lire les événements du récepteur IR
import os              # Pour lancer la commande feh
import sys
import time

import board           # Pour accéder au GPIO12
import adafruit_dht    # Pour le capteur DHT11


# ---------------------------------------------------------------------------
# 1) Constantes de configuration
# ---------------------------------------------------------------------------

# Codes renvoyés par la télécommande (valeurs de event.value dans ton cas)
TOUCHE_IMAGE_CODE = 22   # touche "1"
TOUCHE_DHT_CODE   = 25   # touche "2"

# Nom du fichier image à afficher (doit être dans le même dossier que ce script)
IMAGE_FILE = "infraimage.png"

# Capteur DHT11 sur GPIO12 (broche physique 32)
dht_device = adafruit_dht.DHT11(board.D12)


# ---------------------------------------------------------------------------
# 2) Fonctions utilitaires
# ---------------------------------------------------------------------------

def get_ir_device():
    """
    Recherche le périphérique d'entrée 'gpio_ir_recv'.
    Renvoie l'objet device correspondant.
    Si aucun périphérique n'est trouvé, on quitte le programme.
    """
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    print("Périphériques détectés :")
    for device in devices:
        print(f" - {device.path} - {device.name}")
        if device.name == "gpio_ir_recv":
            print("\n✅ Using device", device.path, "\n")
            return device

    print("❌ No device 'gpio_ir_recv' found !")
    sys.exit(1)


def afficher_image():
    """
    Affiche l'image avec la commande 'feh' en plein écran.
    La fenêtre se ferme quand tu appuies sur une touche ou Échap.
    """
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ Image file '{IMAGE_FILE}' not found !")
        return

    print("📷 Affichage de l'image avec feh...")
    os.system(f"feh -F --auto-zoom -Y '{IMAGE_FILE}'")
    print("✅ Retour au programme.\n")


def lire_dht():
    """
    Lit une fois le capteur DHT11 et renvoie (température, humidité).
    En cas d'erreur, renvoie (None, None).
    """
    try:
        temperature = dht_device.temperature   # en °C
        humidity = dht_device.humidity         # en %

        if temperature is not None and humidity is not None:
            return temperature, humidity
        else:
            return None, None

    except Exception as e:
        print("❌ Erreur de lecture DHT11 :", e)
        return None, None


def afficher_mesures_dht():
    """
    Affiche la température et l'humidité lues sur le DHT11.
    """
    temp, hum = lire_dht()

    if temp is not None and hum is not None:
        print(f"🌡 Température intérieure : {temp:.1f} °C")
        print(f"💧 Humidité intérieure   : {hum:.1f} %\n")
    else:
        print("❌ Impossible de lire les mesures (DHT11).\n")


# ---------------------------------------------------------------------------
# 3) Programme principal : lecture des touches IR
# ---------------------------------------------------------------------------

def main():
    device = get_ir_device()

    print(f"Télécommande IR prête.")
    print(f"- Touche 1 (code {TOUCHE_IMAGE_CODE}) : afficher l'image")
    print(f"- Touche 2 (code {TOUCHE_DHT_CODE})   : afficher température + humidité")
    print("Ctrl + C pour quitter.\n")

    try:
        # Boucle infinie qui lit les événements du récepteur IR
        for event in device.read_loop():
            # ⚠️ On reste fidèle à TON programme qui regarde event.value
            if event.value == TOUCHE_IMAGE_CODE:
                print(f"Code {TOUCHE_IMAGE_CODE} détecté : touche 1 -> IMAGE")
                afficher_image()

            elif event.value == TOUCHE_DHT_CODE:
                print(f"Code {TOUCHE_DHT_CODE} détecté : touche 2 -> DHT11")
                afficher_mesures_dht()

            # Si tu veux déboguer d'autres touches, tu peux décommenter :
            # else:
            #     if event.type == evdev.ecodes.EV_KEY:
            #         print("Event brut :", event)

    except KeyboardInterrupt:
        print("\n🛑 Arrêt du programme par l'utilisateur.")
        sys.exit(0)


if __name__ == "__main__":
    main()

