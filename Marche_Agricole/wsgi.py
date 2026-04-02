import os
from django.core.wsgi import get_wsgi_application

# Assure-toi que le nom correspond bien au dossier de ton projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Marche_Agricole.settings')

application = get_wsgi_application()
