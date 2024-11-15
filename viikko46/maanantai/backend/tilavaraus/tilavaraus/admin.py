# app_name/admin.py
from django.contrib import admin
from .models import Kayttaja, Tilat, Varaajat, Varaukset

# Register models with the admin site
admin.site.register(Kayttaja)
admin.site.register(Tilat)
admin.site.register(Varaajat)
admin.site.register(Varaukset)
