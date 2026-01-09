#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Interface graphique Tkinter pour afficher en temps réel
UNIQUEMENT la température mesurée par un capteur DHT11
connecté sur le GPIO 12 (BCM) du Raspberry Pi.

- Le capteur est lu toutes les 2 secondes.
- En cas de petite erreur de lecture, l'ancienne valeur est conservée
  et un message "Erreur temporaire" s'affiche en bas.
"""

import tkinter as tk
import board
import adafruit_dht

# ---------------------------------------------------------------------------
# 1) Configuration du capteur DHT11 (sur GPIO12)
# ---------------------------------------------------------------------------

# ⚠️ IMPORTANT : DATA du DHT11 connecté sur la broche physique 32 (GPIO12)
dht_device = adafruit_dht.DHT11(board.D12)

# Variable globale pour garder la dernière température valide
dernier_temp = None


# ---------------------------------------------------------------------------
# 2) Fonction de lecture du capteur
# ---------------------------------------------------------------------------

def lire_capteur():
    """
    Lit la température sur le DHT11 toutes les 2 secondes
    et met à jour l'affichage dans la fenêtre.
    - Si la lecture réussit : on affiche la nouvelle température.
    - Si la lecture échoue : on garde l'ancienne température
      et on indique une erreur temporaire.
    """
    global dernier_temp

    try:
        temperature = dht_device.temperature  # en °C

        if temperature is not None:
            # Mise à jour de la dernière valeur valide
            dernier_temp = temperature
            label_temp.config(text=f"Température : {temperature:.1f} °C")
            label_status.config(text="Lecture OK", fg="green")
        else:
            # Le capteur n'a rien renvoyé (cas rare)
            label_status.config(text="Lecture invalide (None)", fg="red")

    except Exception:
        # Le DHT11 est connu pour renvoyer fréquemment des erreurs,
        # on ne panique pas : on garde la dernière température valide.
        if dernier_temp is not None:
            label_temp.config(text=f"Température : {dernier_temp:.1f} °C")
        label_status.config(text="Erreur temporaire de lecture", fg="orange")

    # Relance la fonction après 2 secondes
    window.after(2000, lire_capteur)


# ---------------------------------------------------------------------------
# 3) Interface graphique (Tkinter)
# ---------------------------------------------------------------------------

window = tk.Tk()
window.title("DHT11 - GPIO12 (Température)")
window.minsize(400, 150)

font_title = ("Helvetica", 16, "bold")
font_value = ("Helvetica", 18)
font_status = ("Helvetica", 12, "italic")

# Titre
label_titre = tk.Label(window, text="Capteur DHT11 - GPIO 12", font=font_title)
label_titre.pack(pady=10)

# Affichage de la température uniquement
label_temp = tk.Label(window, text="Température : -- °C", font=font_value)
label_temp.pack(pady=5)

# Zone de statut (OK / erreur)
label_status = tk.Label(window, text="En attente de la première lecture...", font=font_status)
label_status.pack(pady=10)


# ---------------------------------------------------------------------------
# 4) Bouton de fermeture propre
# ---------------------------------------------------------------------------

def quitter():
    """
    Ferme proprement la fenêtre.
    Selon la version de la librairie, dht_device.exit() peut exister ou pas,
    donc on le met dans un try/except pour éviter une erreur.
    """
    try:
        dht_device.exit()
    except Exception:
        pass
    window.destroy()


btn_quit = tk.Button(window, text="Quitter", command=quitter)
btn_quit.pack(pady=5)


# ---------------------------------------------------------------------------
# 5) Lancement de l'application
# ---------------------------------------------------------------------------

# On lance la première lecture après 1 seconde
window.after(1000, lire_capteur)

# Boucle principale Tkinter
window.mainloop()

