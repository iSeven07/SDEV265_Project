# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#         urls.py         #
# = = = = = = = = = = = = #

# URLs is where you identify your URL patterns. It is how Django
# knows where it should send the user based on the path. In some cases
# a variable is included such as a recipe_id or profile so that the relevant
# information can be pulled. Once matched, the URL will send data to the view.

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="recipe-home"),  # Home page
    path("register/", views.register, name="recipe-register"),  # User registration page
    path(
        "submit_recipe/", views.submit_recipe, name="recipe-submit"
    ),  # Recipe submission page
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
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
