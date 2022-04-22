from django.contrib import admin
from .models import Meal, Planification, Ingredient, IngredientUsed

# Register your models here.

admin.site.register(Meal)
admin.site.register(Planification)
admin.site.register(Ingredient)
admin.site.register(IngredientUsed)