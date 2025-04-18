#!/bin/bash

# Benötigte Pakete installieren
echo "Installiere benötigte Pakete..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip omxplayer fbi git

# Projektverzeichnis erstellen
INSTALL_DIR="/home/pi/werbescreen"
echo "Erstelle Projektverzeichnis $INSTALL_DIR..."
mkdir -p $INSTALL_DIR
mkdir -p $INSTALL_DIR/media

# Dateien kopieren oder erstellen
echo "Kopiere Projektdateien..."
cp -r ./* $INSTALL_DIR/

# Berechtigungen setzen
echo "Setze Berechtigungen..."
chmod +x $INSTALL_DIR/install.sh

# Python-Abhängigkeiten installieren
echo "Installiere Python-Abhängigkeiten..."
pip3 install -r $INSTALL_DIR/requirements.txt

# Systemd-Service einrichten
echo "Richte Systemd-Service ein..."
sudo cp $INSTALL_DIR/werbescreen.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable werbescreen.service

echo "Installation abgeschlossen!"
echo "Bearbeiten Sie die Datei $INSTALL_DIR/.env mit Ihren Contentful-Zugangsdaten."
echo "Starten Sie den Service mit: sudo systemctl start werbescreen.service"
