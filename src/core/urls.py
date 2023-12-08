from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="recipe-home"),  # Home page
    path("register/", views.register, name="recipe-register"),  # User registration page
    path(
        "submit_recipe/", views.submit_recipe, name="recipe-submit"
    ),  # Recipe submission page
    path(
        "recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"
    ),  # Recipe detail page
    path(
        "recipe/<int:recipe_id>/rate/", views.rate_recipe, name="rate_recipe"
    ),  # Recipe rating system
    path("login/", views.login_page, name="login"),  # User login page
    path("logout/", views.logout_user, name="logout"),  # User logout
    path("search/", views.search_bar, name="search"),  # Search results page
    path("profile/<str:username>/", views.user_profile, name="user-profile"),
    path(
        "update/profile/", views.edit_profile, name="edit-profile"
    ),  # Update user profile page
    path(
        "update/password/", views.ChangePasswordView.as_view(), name="edit-password"
    ),  # Password change page
]
