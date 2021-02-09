from django.contrib import admin

# Register your models here.
from publications.models import Publications, FavoritePublications

admin.site.register(Publications)
admin.site.register(FavoritePublications)