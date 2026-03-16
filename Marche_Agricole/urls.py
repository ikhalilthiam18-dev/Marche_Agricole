from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import accueil   # <-- AJOUT IMPORTANT

urlpatterns = [
    path('admin/', admin.site.urls),

    # Page d'accueil
    path('', accueil, name='accueil'),   # <-- AJOUT IMPORTANT

    # Applications
    path('', include('utilisateurs.urls')),
    path('produits/', include('produits.urls')),
    path('commandes/', include('commandes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)