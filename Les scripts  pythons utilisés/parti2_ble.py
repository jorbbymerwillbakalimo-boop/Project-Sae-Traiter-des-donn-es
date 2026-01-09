from bluepy.btle import Scanner
import time

scanner = Scanner()

SEUIL_TEMP = 30  # température max
SEUIL_HUM = 60   # humidité max

print("Démarrage du scan BLE...\n")

while True:
    devices = scanner.scan(5.0)

    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            
            if "Nounouch1" in value:
                print("Balise trouvée :", value)
                
                try:
                    nom, temp, hum = value.split("|")

                    temp = float(temp)
                    hum = float(hum)

                    print("Température :", temp, "°C")
                    print("Humidité :", hum, "%")

                    # ✅ TEST DES SEUILS
                    if temp > SEUIL_TEMP:
                        print("⚠️ ALERTE : TEMPÉRATURE TROP ÉLEVÉE")
                    else:
                        print("✅ Température normale")

                    if hum > SEUIL_HUM:
                        print("⚠️ ALERTE : HUMIDITÉ TROP ÉLEVÉE")
                    else:
                        print("✅ Humidité normale")

                    print("----------------------------")

                except Exception as e:
                    print("Erreur de décodage des données:", e)

    time.sleep(5)

