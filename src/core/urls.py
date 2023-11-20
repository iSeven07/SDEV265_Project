from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="recipe-home"),
    # path('search/', views.search, name="recipe-search"),
    path('register/', views.register, name="recipe-register"),
    path('submit_recipe/', views.submit_recipe, name='recipe-submit'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/rate/', views.rate_recipe, name='rate_recipe'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search_bar, name='search'),
    path("profile/<str:username>/", views.user_profile, name='user-profile'),
    path('update/profile/', views.edit_profile, name='edit-profile'),
    path('update/password/', views.ChangePasswordView.as_view(), name='edit-password')
] 