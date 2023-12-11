# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#        views.py         #
# = = = = = = = = = = = = #

# This is where data is primarily processed for each page. Depending on
# the URL path it will be matched with a view here. That view will utilize an
# html template, located in the templates folder, and send data back and forth
# to make our pages functional.

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import Recipe, Profile, Rating, Ingredient, RecipeIngredient
from .forms import SignupForm, RecipeForm, LoginForm, UpdateUserForm, UpdateProfileForm, IngredientFormSet, EditIngredientForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Value, Q, Case, When, BooleanField
from django.db.models.functions import Round
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

# Dummy Data
posts = [
    {
        "author": "John Smith",
        "title": "Recipe Post 1",
        "content": "This is a recipe post",
        "date": "1 November 2023",
    },
    {
        "author": "Jane Doe",
        "title": "Recipe Post 2",
        "content": "This is another recipe post",
        "date": "7 November 2023",
    },
]


# Home View
def home(request):
    # Recipe Ratings for each Recipe
    recipes = Recipe.objects.annotate(
        avg_rating=Round(Avg('rating__rating'), 1),
        has_ratings=Case(
            When(rating__isnull=True, then=Value(False)),
            default=Value(True),
            output_field=BooleanField(),
        ),
    ).order_by("-date")

    # Used for Displaying Rating as Stars
    for recipe in recipes:
        if recipe.avg_rating is not None:
            recipe.stars_filled = range(int(recipe.avg_rating))
            recipe.stars_empty = range(5 - int(recipe.avg_rating))
        else:
            recipe.stars_filled = []
            recipe.stars_empty = range(5)

    return render(request, "home.html", {"recipes": recipes, "title": "Home"})
    # return HttpResponse('<h1>Recipe Home</h1>')


# Register View
def register(request):
    message = ""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Hello {user.username}! Welcome to Recipe Builder!",
                extra_tags="alert alert-success",
            )
            return redirect("recipe-home")
        else:
            message = (
                "There was a problem creating your account. Check your information."
            )
    else:
        form = SignupForm()
    return render(
        request,
        "register.html",
        {"title": "Register", "form": form, "message": message},
    )

# Submit Recipe View
def submit_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST) # Set the base form to Recipe
        formset = IngredientFormSet(request.POST) # This sets our formset to Ingreidents. It is a set because there can be multiple.

        # Django automatically checks to see if data entered is valid against our Models and Forms
        if form.is_valid() and formset.is_valid():
        # Check if at least one ingredient has been provided
            if any(form.cleaned_data.get('ingredient') for form in formset):
                new_recipe = form.save(commit=False)
                new_recipe.author = request.user
                new_recipe.save()

                formset.instance = new_recipe
                formset.save()

                return redirect('recipe_detail', recipe_id=new_recipe.pk)
            else:
                # Adds an error message if no ingredients are provided
                messages.error(request, 'At least one ingredient is required.', extra_tags="alert alert-danger")
                return render(request, 'recipe_submission.html', {'form': form, 'formset': formset})

    else:
        form = RecipeForm()
        formset = IngredientFormSet()

    return render(request, 'recipe_submission.html', {'form': form, 'formset': formset})

# Login Page View
def login_page(request):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    f"Hello {user.username}! You have successfully logged in!",
                    extra_tags="alert alert-success",
                )
                return redirect("recipe-home")
            else:
                message = "Login failed!"
    return render(request, "login.html", context={"form": form, "message": message})


# Logs out the user
def logout_user(request):
    logout(request)
    messages.success(
        request, f"You have successfully logged out!", extra_tags="alert alert-primary"
    )
    return redirect("recipe-home")


# User Profile View
def user_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    user_recipes = Recipe.objects.filter(author=user_profile.user)
    return render(request, "profile.html", {"user_profile": user_profile, "user_recipes": user_recipes})


# Edit User Profile View, Requires user to be logged in
@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="edit-profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        "edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


# Change Password View, Accessible from Edit Profile
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "change_password.html"
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy("edit-profile")


# Search Bar, Handles Search Data and Displays a Results Page
def search_bar(request):
    query = request.GET.get("query")

    if query:
        # Normalize query to lower case for case-insensitive search
        query = query.lower().strip()
        
        # Use Q objects for searching across multiple fields
        results = Recipe.objects.filter(
            Q(title__icontains=query) |  # Match in recipe title
            Q(content__icontains=query) |  # Match in recipe content
            Q(ingredients__name__icontains=query)  # Match in ingredient names
        ).distinct()  # Ensure distinct results
    else:
        results = None

    return render(request, "search.html", {"results": results, "query": query})


# Recipe Detail View
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = recipe.recipeingredient_set.all()
    ratings = Rating.objects.filter(recipe=recipe)
    average_rating = ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"]
    total_nutrition = recipe.calculate_total_nutrition()

    # Calculate Stars for Recipe out of 5
    if average_rating:
        full_stars = range(int(average_rating))
        empty_stars = range(5 - int(average_rating))
    else:
        full_stars = 0
        empty_stars = 5

    return render(request, 'recipe_detail.html', {'recipe': recipe, 
                                                  'average_rating': average_rating, 
                                                  'ingredients': ingredients, 
                                                  'total_nutrition': total_nutrition,
                                                  'full_stars': full_stars,
                                                  'empty_stars': empty_stars})

# Edit Recipe View. Users must be logged in to access.
@login_required(login_url="/login/")
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)

    IngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=EditIngredientForm, extra=0)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)

    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)

    return render(request, 'edit_recipe.html', {'form': form, 'formset': formset, 'recipe': recipe})


# Allows users to Rate Recipes. They must be logged in to do so.
@login_required(login_url="/login/")
def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user_rating = int(request.POST.get('rating'))
        
        Rating.objects.create(user=request.user, recipe=recipe, rating=user_rating)

    return redirect("recipe_detail", recipe_id=recipe_id)
