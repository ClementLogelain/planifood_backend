from django.urls import path, include
from . import views

urlpatterns = [

    path('auth/login', views.LoginView.as_view()),
    path('user/register', views.RegisterView.as_view()),
    path('user/delete/<str:pk>', views.DeleteUserView.as_view()),
    path('users',views.getAllUsers.as_view()),

    path('ingredients', views.IngredientView.as_view()),
    path('appIngredients', views.AppIngredientView.as_view()),
    path('ingredients/<str:pk>', views.IngredientUpdateDelete.as_view()),

    path('meals', views.MealView.as_view()),
    path('appMeals', views.AppMealView.as_view()),
    path('meals/<str:pk>', views.MealUpdateDelete.as_view()),

    path('planifications', views.PlanificationView.as_view()),
    path('planifications/<str:pk>', views.PlanificationUpdateDelete.as_view()),

    path('ingredientsUsed', views.IngredientUsedView.as_view()),
    path('ingredientsUsed/<str:pk>', views.IngredientUsedDelete.as_view())
]
