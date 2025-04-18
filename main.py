import os
import sys
import time
import random
import logging
import signal
from contentful_client import ContentfulClient
from display_manager import DisplayManager
from config import MEDIA_DIRECTORY

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/werbescreen.log')
    ]
)

logger = logging.getLogger("WerbeScreen")

def handle_exit(signum, frame):
    """Behandelt Beenden-Signale sauber"""
    logger.info("Programm wird beendet...")
    # Stelle sicher, dass alle Prozesse beendet werden
    sys.exit(0)
    
# Signal-Handler registrieren
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

def main():
    """Hauptfunktion"""
    logger.info("Starte Werbescreen...")
    
    # Stelle sicher, dass Medienverzeichnis existiert
    os.makedirs(MEDIA_DIRECTORY, exist_ok=True)
    
    contentful = ContentfulClient()
    display = DisplayManager()
    
    refresh_interval = 600  # Aktualisierung alle 10 Minuten
    media_items = []
    
    try:
        while True:
            # Neue Medien von Contentful abrufen und herunterladen
            logger.info("Aktualisiere Medien von Contentful...")
            fetched_items = contentful.fetch_all_media()
            media_items = contentful.download_media(fetched_items)
            
            if not media_items:
                logger.warning("Keine Medien gefunden. Warte auf nächste Aktualisierung...")
                time.sleep(60)  # Warte 1 Minute
                continue
            
            # Medien in zufälliger Reihenfolge abspielen
            rotation_count = 0
            start_time = time.time()
            
            while (time.time() - start_time) < refresh_interval and rotation_count < 10:
                # Medien neu mischen bei jedem Durchgang
                random.shuffle(media_items)
                display.play_media_list(media_items)
                rotation_count += 1
                
    except KeyboardInterrupt:
        logger.info("Programm durch Benutzer beendet.")
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}")
        return 1
    finally:
        # Stelle sicher, dass alle Prozesse beendet werden
        display.kill_current_process()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
