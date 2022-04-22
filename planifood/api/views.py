from urllib.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password

from django.http import Http404

from .models import Ingredient, IngredientUsed, Meal, Planification
from .serializers import UserFullSerializer, UserSerializer, IngredientSerializer, IngredientUsedSerializer, MealSerializer, MealFullSerializer, PlanificationSerializer


# Create your views here.

class LoginView(ObtainAuthToken):
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {'id':user.pk,
                     'email': user.email,
                     'username': user.username}
        })

class RegisterView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        initialpassword = request.data['password']
        request.data['password'] = make_password(request.data['password'])
        userSerializer  = UserSerializer(data=request.data)
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()
        return Response(data=userSerializer.data)

class DeleteUserView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response('Deleted succussfully !', 202)

class getAllUsers(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserFullSerializer(users, many=True)
        return Response(serializer.data)



# -------------------- INGREDIENTS ---------------------

class IngredientView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ingredients = Ingredient.objects.filter(owner=request.user)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AppIngredientView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ingredients = Ingredient.objects.filter(owner=None)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

class IngredientUpdateDelete(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 403)

    def delete(self, request, pk):
        ingredient = self.get_object(pk)
        ingredient.delete()
        return Response("Meal successfully deleted", 202)

# -------------------- MEALS ----------------------------

class MealView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        meals = Meal.objects.filter(owner=request.user)
        serializer = MealFullSerializer(meals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MealSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AppMealView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        meals = Meal.objects.filter(isBasic=True)
        serializer = MealFullSerializer(meals, many=True)
        return Response(serializer.data)


class MealUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        meal = Meal.objects.get(id=pk)
        serializer = MealFullSerializer(meal, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        meal = self.get_object(pk)
        serializer = MealSerializer(meal, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 403)

    def delete(self, request, pk):
        meal = self.get_object(pk)
        meal.delete()
        return Response(["Meal successfully deleted"], 202)


# --------------------- INGREDIENTS USED IN MEAL ------------------------


class IngredientUsedView(APIView):
    def post(self, request):
        serializer = IngredientUsedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class IngredientUsedDelete(APIView):
    def get_object(self, pk):
        try:
            return IngredientUsed.objects.get(pk=pk)
        except IngredientUsed.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        using = self.get_object(pk)
        serializer = IngredientUsedSerializer(using, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 403)

    def delete(self, request, pk):
        using = self.get_object(pk)
        using.delete()
        return Response("Meal successfully deleted", 202)


# --------------------- Planifications ------------------------


class PlanificationView(APIView):
    def get(self, request):
        plani = Planification.objects.filter(owner=request.user)
        serializer = PlanificationSerializer(plani, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PlanificationUpdateDelete(APIView):
    def get_object(self, pk):
        try:
            return Planification.objects.get(pk=pk)
        except Planification.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        planification = self.get_object(pk)
        serializer = PlanificationSerializer(planification, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, 403)

    def delete(self, request, pk):
        planification = self.get_object(pk)
        planification.delete()
        return Response("Meal successfully deleted", 202)


