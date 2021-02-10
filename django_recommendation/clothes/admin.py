from django.contrib import admin
from .models import Cloth

class ClothesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cloth, ClothesAdmin)
