import os
import logging
import requests
import contentful
import time
from config import (CONTENTFUL_SPACE_ID, CONTENTFUL_ACCESS_TOKEN, 
                   CONTENTFUL_ENVIRONMENT, MEDIA_DIRECTORY,
                   CONTENT_TYPE)

class ContentfulClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = contentful.Client(
            CONTENTFUL_SPACE_ID,
            CONTENTFUL_ACCESS_TOKEN,
            environment=CONTENTFUL_ENVIRONMENT
        )
        
        # Stelle sicher, dass das Medienverzeichnis existiert
        os.makedirs(MEDIA_DIRECTORY, exist_ok=True)
        
    def fetch_all_media(self):
        """Ruft alle Werbeinhalte von Contentful ab"""
        media_items = []
        
        try:
            entries = self.client.entries({
                'content_type': CONTENT_TYPE,
                'include': 10
            })
            
            self.logger.info(f"Abgerufene Einträge: {len(entries)}")
            
            for entry in entries:
                try:
                    # Prüfen, ob das Feld "werbegrafik" vorhanden und nicht leer ist
                    if hasattr(entry, 'werbegrafik') and entry.werbegrafik:
                        # Bestimme Medientyp (Bild oder Video)
                        file_url = entry.werbegrafik.url()
                        file_extension = os.path.splitext(file_url.split('?')[0])[1].lower()
                        
                        media_type = 'video' if file_extension in ['.mp4', '.mov', '.avi', '.mkv'] else 'image'
                        
                        media_items.append({
                            'id': entry.sys['id'],
                            'title': entry.name if hasattr(entry, 'name') else f"Werbung {entry.sys['id']}",
                            'url': file_url,
                            'type': media_type,
                            'updated_at': entry.sys.get('updatedAt')
                        })
                except Exception as item_error:
                    self.logger.error(f"Fehler bei Eintrag {getattr(entry, 'name', 'Unbekannt')}: {item_error}")
                    
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Werbemedien: {e}")
            
        self.logger.info(f"Insgesamt {len(media_items)} Medienelemente von Contentful abgerufen")
        return media_items
    
    def download_media(self, media_items):
        """Lädt Medien herunter und speichert sie lokal"""
        downloaded_files = []
        
        for item in media_items:
            file_extension = os.path.splitext(item['url'].split('?')[0])[1]
            local_filename = f"{item['id']}{file_extension}"
            local_path = os.path.join(MEDIA_DIRECTORY, local_filename)
            
            # Prüfen ob Datei bereits existiert und aktuell ist
            if os.path.exists(local_path):
                self.logger.debug(f"Datei {local_filename} existiert bereits.")
                downloaded_files.append({
                    'id': item['id'],
                    'title': item['title'],
                    'path': local_path,
                    'type': item['type']
                })
                continue
                
            # Datei herunterladen
            try:
                self.logger.info(f"Lade {item['title']} herunter...")
                response = requests.get(item['url'], stream=True)
                response.raise_for_status()
                
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                self.logger.info(f"Download von {item['title']} abgeschlossen.")
                downloaded_files.append({
                    'id': item['id'],
                    'title': item['title'],
                    'path': local_path,
                    'type': item['type']
                })
            except Exception as e:
                self.logger.error(f"Fehler beim Herunterladen von {item['url']}: {e}")
        
        return downloaded_files
