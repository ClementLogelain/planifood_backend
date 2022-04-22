from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Meal(models.Model):
    title = models.CharField(max_length=45, unique=True)
    process = models.TextField(max_length=1000)
    duration = models.IntegerField(default=0)
    isBasic = models.BooleanField(default=True)
    owner = models.ForeignKey(User, related_name='meals', on_delete=models.CASCADE, blank=True, null=True,default=None)

    def __str__(self):
        return self.title


class Planification(models.Model):
    panified_at = models.DateTimeField(default=now)
    owner = models.ForeignKey(User, related_name='planifications', on_delete=models.CASCADE, default=None)
    meal = models.ForeignKey(Meal, related_name='planned', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.panified_at)


class Ingredient(models.Model):
    name = models.CharField(max_length=60, unique=True)
    owner = models.ForeignKey(User, related_name='ingredients', on_delete=models.CASCADE,blank=True, null=True,default=None)

    def __str__(self):
        return self.name

class IngredientUsed(models.Model):
    using = models.TextField(max_length=100)
    meal = models.ForeignKey(Meal, related_name='ingredients', on_delete=models.CASCADE, default=None)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.using
