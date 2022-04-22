from xmlrpc.client import DateTime
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ingredient, IngredientUsed, Meal, Planification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {
            'password': { 'write_only': True }
        }

        

#######


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


#######

class IngredientUsedNameSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False)
    class Meta:
        model = IngredientUsed
        fields = '__all__'

class IngredientUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientUsed
        fields = '__all__'

#######


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id','title','process','duration','isBasic','owner']


class MealFullSerializer(serializers.ModelSerializer):
    ingredients = IngredientUsedNameSerializer(many=True)
    class Meta:
        model = Meal
        fields = '__all__'

class MealNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['title']

#######

class PlanificationSerializer(serializers.ModelSerializer):
    meal = MealNameSerializer(many=False)
    class Meta:
        model = Planification
        fields = '__all__'

###############

class UserFullSerializer(serializers.ModelSerializer):
    meals = MealFullSerializer(many=True)
    planifications = PlanificationSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    class Meta:
        model = User
        fields = ['id','username','email','meals','planifications','ingredients']