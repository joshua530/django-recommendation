from django.db import models
from django.conf import settings

class Cloth(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cloth = models.ForeignKey('Cloth', on_delete=models.CASCADE)

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    cloth = models.ForeignKey('Cloth', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
