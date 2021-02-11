from django.contrib import admin
from .models import Cloth, Opinion

class ClothesAdmin(admin.ModelAdmin):
    pass

class OpinionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cloth, ClothesAdmin)
admin.site.register(Opinion, OpinionsAdmin)
