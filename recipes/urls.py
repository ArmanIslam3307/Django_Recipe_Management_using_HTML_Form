from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Recipe
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/update/', views.recipe_update, name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),

    # Ingredient
    path('recipe/<int:recipe_pk>/ingredient/add/', views.ingredient_add, name='ingredient_add'),
    path('ingredient/<int:pk>/update/', views.ingredient_update, name='ingredient_update'),
    path('ingredient/<int:pk>/delete/', views.ingredient_delete, name='ingredient_delete'),
]