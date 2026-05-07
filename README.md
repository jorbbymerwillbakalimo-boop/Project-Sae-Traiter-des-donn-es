# SAÉ – Traiter des données

> SAÉ de 1ère année – BUT Réseaux & Télécommunications  
> Université de Guyane – IUT de Kourou

---

## 📌 Description du projet

Ce projet consiste à développer un **système interactif sur Raspberry Pi** pilotable via une **télécommande infrarouge (IR)**, capable d'afficher des données en temps réel depuis un **capteur DHT11** (température et humidité).

Le projet articule trois grandes fonctionnalités :
- Détection et lecture des **signaux infrarouges** (télécommande IR + récepteur VS1838B)
- Affichage d'une **image** au pressage d'une touche IR (touche 1)
- Affichage de la **température et humidité** intérieures/extérieures en interface graphique (touches 2 et 3)

---

## 🎯 Compétences travaillées

- Câblage et branchement de **composants électroniques** sur les GPIO du Raspberry Pi
- Configuration du module noyau Linux **`gpio_ir_recv`** pour la réception IR
- Lecture de capteur physique (**DHT11**) via Python avec gestion des erreurs
- Développement d'une **interface graphique** avec `Tkinter`
- Transfert de fichiers et accès distant via **SSH**
- Débogage matériel/logiciel et résolution de problèmes en conditions réelles

---

## 🗂️ Contenu du répertoire

```
Project-Sae-Traiter-des-donnees/
├── scripts/
│   ├── ir_display.py        # Détection IR + affichage image
│   ├── dht11_display.py     # Lecture capteur DHT11 + interface Tkinter
│   └── ...
├── compte-rendu/            # Documentation du projet
└── README.md
```

---

## 🛠️ Stack technique

![Raspberry Pi]
![Python]
![Linux]

**Matériel utilisé :**

| Composant | Rôle |
|---|---|
| Raspberry Pi 4 | Unité centrale du système |
| Récepteur IR VS1838B | Réception des signaux de la télécommande |
| Télécommande IR | Contrôle du système |
| Capteur DHT11 (GPIO 12) | Mesure température & humidité |
| Écran HDMI | Affichage de l'interface graphique |

**Bibliothèques & outils Linux :**

| Outil | Usage |
|---|---|
| `gpio_ir_recv` | Module noyau pour réception IR |
| `ir-keytable` | Activation des protocoles IR |
| `evtest` | Débogage et lecture des événements IR |
| `Tkinter` | Interface graphique Python |
| `LXDE` + `startx` | Environnement graphique du Raspberry Pi |
| `SSH` | Transfert de fichiers et accès distant |

---

## 🎓 Contexte académique

- **Formation** : BUT Réseaux & Télécommunications – 1ère année
- **Module** : SAÉ – Traiter des données
- **Établissement** : Université de Guyane – IUT de Kourou

---

*Répertoire à visée pédagogique – projet réalisé en contexte de formation.*
