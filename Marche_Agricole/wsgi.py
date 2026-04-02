import os
import sys

path = '/home/Khalil18/Marche_Agricole/Marche_Agricole'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Marche_Agricole.settings')
application=get_wsgi_application()
