from django.db import models
from django.conf import settings

class Cloth(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='clothes/%Y/%m/%d/', default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Clothes'

class Opinion(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    choices = (
        (LIKE, LIKE),
        (DISLIKE, DISLIKE)
    )

    name = models.CharField(choices=choices, default=None, null=True, max_length=7)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Cloth', on_delete=models.CASCADE)

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Cloth', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
