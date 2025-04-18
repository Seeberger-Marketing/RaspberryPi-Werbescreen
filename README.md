# Raspberry Pi Werbescreen

Ein automatisiertes System zur Anzeige von Werbeinhalten (Bilder und Videos) auf einem Fernseher mithilfe eines Raspberry Pi Zero 2W ohne GUI. Die Inhalte werden von Contentful abgerufen und in zufälliger Reihenfolge angezeigt.

## Features

- Automatisches Abrufen und Anzeigen von Werbebildern und -videos aus Contentful
- Zufällige Rotation der Medien
- Automatische Aktualisierung der Inhalte (alle 10 Minuten)
- Automatischer Start nach Neustart des Raspberry Pi
- Unterstützung für Bilder und Videos
- Funktioniert auf einem Raspberry Pi Zero 2W ohne grafische Benutzeroberfläche

## Voraussetzungen

- Raspberry Pi Zero 2W (oder anderes Raspberry Pi Modell)
- SD-Karte mit Raspberry Pi OS Lite (ohne GUI)
- HDMI-Verbindung zu einem Fernseher/Display
- Internetverbindung für den Abruf von Contentful-Inhalten
- Contentful-Konto mit entsprechend eingerichtetem Content-Modell

## Installation

1. Kopieren Sie alle Projektdateien auf Ihren Raspberry Pi.
2. Stellen Sie sicher, dass die Dateien `.env` Ihre korrekten Contentful-Zugangsdaten enthält.
3. Führen Sie das Installationsskript aus:

```bash
chmod +x install.sh
./install.sh
```

4. Starten Sie den Service:

```bash
sudo systemctl start werbescreen.service
```

## Contentful-Konfiguration

In Ihrem Contentful-Konto muss ein Content-Type namens "werbung" mit folgenden Feldern eingerichtet sein:
- `name`: Name/Titel der Werbung (Textfeld)
- `werbegrafik`: Das Werbebild oder -video (Asset-Link)

## Systemkonfiguration

Die Anzeigedauer für Bilder und Videos kann in der `.env`-Datei angepasst werden:
- `DISPLAY_TIME_IMAGES`: Anzeigedauer für Bilder in Sekunden (Standard: 10 Sekunden)
- `DISPLAY_TIME_VIDEOS`: Spezifische Anzeigedauer für Videos in Sekunden (0 = Vollständige Wiedergabe)

## Fehlersuche

Logs des Werbescreens können wie folgt eingesehen werden:

```bash
sudo journalctl -u werbescreen.service
```

oder

```bash
cat /var/log/werbescreen.log
```

## Hinweise zur Nutzung mit dem Raspberry Pi Zero 2W

- Für optimale Leistung bei Videowiedergabe sollten Videos in geeigneter Auflösung und mit einem für den Raspberry Pi optimierten Codec (z.B. H.264) vorliegen.
- Der Raspberry Pi Zero 2W hat begrenzte Rechenleistung. Sehr hochauflösende Videos könnten Leistungsprobleme verursachen.
