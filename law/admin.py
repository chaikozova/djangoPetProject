from django.contrib import admin

# Register your models here.
from law.models import Laws, FavoriteLaws

admin.site.register(Laws)
admin.site.register(FavoriteLaws)