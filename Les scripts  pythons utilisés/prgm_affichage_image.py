#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
TP infrarouge – Étape 2
Détection de la touche "1" (code 22) et affichage de l'image infraimage.png
via la visionneuse d'images 'feh'.
"""

import evdev           # Pour lire les événements du récepteur IR
from time import sleep
import os              # Pour lancer la commande feh
import sys

# Code renvoyé par la touche "5" (trouvé à l'étape 1)
TOUCHE_1_CODE = 22

# Nom du fichier image à afficher (doit être dans le même dossier que ce script)
IMAGE_FILE = "infraimage.png"


def get_ir_device():
    """
    Recherche le périphérique d'entrée 'gpio_ir_recv'.
    Renvoie l'objet device correspondant.
    Si aucun périphérique n'est trouvé, on quitte le programme.
    """
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:
        print(f"Trouvé : {device.path} - {device.name}")
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
    print("📷 Affichage de l'image avec feh...")
    # -F : plein écran, --auto-zoom : adapte l'image à l'écran, -Y : cache la barre
    os.system(f"feh -F --auto-zoom -Y '{IMAGE_FILE}'")
    print("✅ Retour au programme.\n")


def main():
    device = get_ir_device()

    print(f"Appuie sur la touche '1' (code {TOUCHE_1_CODE}) pour afficher l'image.")
    print("Ctrl + C pour quitter.\n")

    try:
        # Boucle infinie qui lit les événements du récepteur IR
        for event in device.read_loop():
            # On teste simplement la valeur de l'événement
            if event.value == TOUCHE_1_CODE:
                print(f"Code {TOUCHE_1_CODE} détecté : touche 1 !")
                afficher_image()

    except KeyboardInterrupt:
        print("\n🛑 Arrêt du programme par l'utilisateur.")
        sys.exit(0)


if __name__ == "__main__":
    main()
