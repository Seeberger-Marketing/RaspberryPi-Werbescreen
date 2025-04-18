import os
import random
import subprocess
import time
import logging
import signal
from config import DISPLAY_TIME_IMAGES, DISPLAY_TIME_VIDEOS

class DisplayManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_process = None
        
    def kill_current_process(self):
        """Beendet den aktuellen Medienprozess, falls einer läuft"""
        if self.current_process and self.current_process.poll() is None:
            try:
                # Sende SIGTERM
                self.current_process.terminate()
                time.sleep(0.5)
                # Falls der Prozess immer noch läuft, sende SIGKILL
                if self.current_process.poll() is None:
                    self.current_process.kill()
            except Exception as e:
                self.logger.error(f"Fehler beim Beenden des Prozesses: {e}")
    
    def display_image(self, image_path):
        """Zeigt ein Bild mit FBI an"""
        self.logger.info(f"Zeige Bild an: {image_path}")
        self.kill_current_process()
        
        # FBI zum Anzeigen des Bildes verwenden
        try:
            # "-noverbose": keine Ausgabe, "-a": automatisches Skalieren
            # "-t": Anzeigedauer in Sekunden, "-1": kein Hintergrundbild
            self.current_process = subprocess.Popen(
                ["fbi", "-noverbose", "-a", "-t", str(DISPLAY_TIME_IMAGES), "-1", image_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Warten bis die Anzeigedauer abgelaufen ist
            time.sleep(DISPLAY_TIME_IMAGES)
            self.kill_current_process()
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Anzeigen des Bildes {image_path}: {e}")
            return False
    
    def display_video(self, video_path):
        """Spielt ein Video mit OMXPlayer ab"""
        self.logger.info(f"Spiele Video ab: {video_path}")
        self.kill_current_process()
        
        try:
            # omxplayer zum Abspielen des Videos verwenden
            # "--no-osd": keine Bildschirmanzeige, "-b": schwarzer Hintergrund
            self.current_process = subprocess.Popen(
                ["omxplayer", "--no-osd", "-b", video_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wenn eine feste Videodauer angegeben ist, verwenden wir diese
            if DISPLAY_TIME_VIDEOS > 0:
                time.sleep(DISPLAY_TIME_VIDEOS)
                self.kill_current_process()
            else:
                # Sonst warten wir, bis das Video fertig ist
                self.current_process.wait()
            
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Abspielen des Videos {video_path}: {e}")
            return False
            
    def play_media_list(self, media_items):
        """Spielt eine Liste von Medien in zufälliger Reihenfolge ab"""
        if not media_items:
            self.logger.warning("Keine Medien zum Anzeigen vorhanden!")
            return
            
        # Zufällige Reihenfolge
        random.shuffle(media_items)
        
        for item in media_items:
            if item['type'] == 'image':
                self.display_image(item['path'])
            elif item['type'] == 'video':
                self.display_video(item['path'])
            else:
                self.logger.warning(f"Unbekannter Medientyp: {item['type']}")
