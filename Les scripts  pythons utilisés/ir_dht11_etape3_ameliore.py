#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IR + GUI Temp/Hum (version simple et fiable)

- Touche 1 (code 22) : IMAGE (infraimage.png via feh)
- Touche 2 (code 25) : lance gui_temp_hum.py en mode 'temp'
- Touche 3 (code 13) : lance gui_temp_hum.py en mode 'hum'

On utilise os.system() comme dans ton programme initial,
pour être sûr que feh et python affichent bien les fenêtres.
"""

import evdev
import os
import sys
import time

CODE_IMG  = 22   # touche 1
CODE_TEMP = 25   # touche 2
CODE_HUM  = 13   # touche 3

IMAGE_FILE = "infraimage.png"
GUI_FILE   = "gui_temp_hum.py"

last_code = None
last_time = 0
ANTI_SPAM = 0.5  # secondes


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


def show_image():
    """Affiche l'image avec feh (comme ton code qui marchait)."""
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ Image file '{IMAGE_FILE}' not found !")
        return
    print("📷 Affichage de l'image (feh)...")
    # comme ton ancien code, bloquant, mais au moins tu VOIS ce qui se passe
    os.system(f"feh -F --auto-zoom -Y '{IMAGE_FILE}'")


def launch_gui(mode):
    """
    Lance gui_temp_hum.py en lui passant 'temp' ou 'hum'.
    On utilise aussi os.system pour voir les erreurs si ça plante.
    """
    if not os.path.exists(GUI_FILE):
        print(f"❌ Script GUI '{GUI_FILE}' introuvable !")
        return
    print(f"🖼 Lancement de {GUI_FILE} en mode '{mode}'...")
    os.system(f"python3 {GUI_FILE} {mode}")


def main():
    global last_code, last_time

    device = get_ir_device()

    print("Télécommande IR prête :")
    print(f"- Touche 1 (code {CODE_IMG})  : IMAGE (feh)")
    print(f"- Touche 2 (code {CODE_TEMP}) : GUI TEMP (mode 'temp')")
    print(f"- Touche 3 (code {CODE_HUM})  : GUI HUM  (mode 'hum')")
    print("Ctrl + C pour quitter.\n")

    try:
        for event in device.read_loop():
            code = event.value
            now = time.time()

            # Anti-spam simple
            if code == last_code and (now - last_time) < ANTI_SPAM:
                continue

            last_code = code
            last_time = now

            if code == CODE_IMG:
                print(f"\n➡ Touche 1 (code {CODE_IMG}) détectée : IMAGE")
                show_image()

            elif code == CODE_TEMP:
                print(f"\n➡ Touche 2 (code {CODE_TEMP}) détectée : GUI TEMP")
                launch_gui("temp")

            elif code == CODE_HUM:
                print(f"\n➡ Touche 3 (code {CODE_HUM}) détectée : GUI HUM")
                launch_gui("hum")

    except KeyboardInterrupt:
        print("\n🛑 Arrêt du programme par l'utilisateur.")
        sys.exit(0)


if __name__ == "__main__":
    main()

