import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Contentful-Konfiguration
CONTENTFUL_SPACE_ID = os.getenv('CONTENTFUL_SPACE_ID')
CONTENTFUL_ACCESS_TOKEN = os.getenv('CONTENTFUL_ACCESS_TOKEN')
CONTENTFUL_PREVIEW_ACCESS_TOKEN = os.getenv('CONTENTFUL_PREVIEW_ACCESS_TOKEN')
CONTENTFUL_ENVIRONMENT = os.getenv('CONTENTFUL_ENVIRONMENT', 'master')

# Anzeigeeinstellungen
DISPLAY_TIME_IMAGES = int(os.getenv('DISPLAY_TIME_IMAGES', 10))  # Sekunden
DISPLAY_TIME_VIDEOS = int(os.getenv('DISPLAY_TIME_VIDEOS', 0))   # 0 = Videolänge verwenden

# Medienspeicher
MEDIA_DIRECTORY = os.getenv('MEDIA_DIRECTORY', '/home/pi/werbescreen/media')

# Contentful Inhaltstyp
CONTENT_TYPE = 'werbung'
