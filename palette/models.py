from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Color(models.Model):
    hex_code = models.CharField(max_length=256)


class ColorPalette(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='palette')
    is_private = models.BooleanField(default=True)
    name = models.CharField(max_length=256)
    dominant_colors = models.ManyToManyField(Color, related_name='+')
    accent_colors = models.ManyToManyField(Color, related_name='+')

    class Meta:
        managed = True
        ordering = ['name']

    def __str__(self):
        return self.name


class FavoritePalette(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='favourite')
    palette = models.ForeignKey('ColorPalette', models.DO_NOTHING)

    class Meta:
        managed = True
