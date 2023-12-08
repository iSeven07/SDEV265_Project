from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import Recipe, Profile, Rating, Ingredient
from .forms import SignupForm, RecipeForm, LoginForm, UpdateUserForm, UpdateProfileForm, IngredientFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Value, F, Case, When, BooleanField
from django.db.models.functions import Round

# Dummy Data
posts = [
    {
        'author': 'John Smith',
        'title': 'Recipe Post 1',
        'content': 'This is a recipe post',
        'date': '1 November 2023'
    },
    {
        'author': 'Jane Doe',
        'title': 'Recipe Post 2',
        'content': 'This is another recipe post',
        'date': '7 November 2023'
    }
]

# Home View
def home(request):
    # Recipe Ratings for each Recipe
    recipes = Recipe.objects.annotate(
        avg_rating=Round(Avg('rating__rating'), 1),
        has_ratings=Case(
            When(rating__isnull=True, then=Value(False)),
            default=Value(True),
            output_field=BooleanField()
        ) 
    ).order_by('-date')

    # Used for Displaying Rating as Stars
    for recipe in recipes:
        if recipe.avg_rating is not None:
            recipe.stars_filled = range(int(recipe.avg_rating))
            recipe.stars_empty = range(5 - int(recipe.avg_rating))
        else:
            recipe.stars_filled = []
            recipe.stars_empty = range(5)
        
    return render(request, "home.html", {'recipes': recipes, 'title': 'Home'})
    # return HttpResponse('<h1>Recipe Home</h1>')

# Search View
"""
def search(request):

    return render(request, "search.html", {'title': 'Search'})
    # return HttpResponse('<h1>Recipe Search</h1>')
"""

# Register View
def register(request):
    message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Hello {user.username}! Welcome to Recipe Builder!', extra_tags='alert alert-success')
            return redirect('recipe-home')
        else:
            message = 'There was a problem creating your account. Check your information.'
    else:
        form = SignupForm()
    return render(request, 'register.html', {'title': 'Register', 'form': form, 'message': message})
    
"""
 def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            form.save()
            return redirect('recipe-submit')  # Adjust the redirect as needed
    else:
        form = RecipeForm()
    return render(request, 'recipe_submission.html', {'form': form})
"""

# Submit Recipe View
# def submit_recipe(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         formset = IngredientFormSet(request.POST, instace=Recipes())

#         if form.is_valid() and formset.is_valid:
#             # Save the form data to the database
#             new_recipe = form.save(commit=False)
#             new_recipe.author = request.user  # Assuming you have user authentication
#             new_recipe.save()

#             for form in formset:
#                 ingredient = form.cleaned_data.get('ingredient')
#                 quantity = form.cleaned_data.get('quantity')
#                 if ingredient and quantity:
#                     new_recipe.ingredients.add(ingredient, through_defaults={'quantity': quantity})

#             messages.success(request, 'Recipe submitted successfully!')
#             return redirect('recipe-submit')   # Redirect to recipe detail page
#             # removed , pk=new_recipe.pk from ('recipe-submit )
#     else:
#         form = RecipeForm()
#         formset = IngredientFormSet(instance=Recipes())

#     return render(request, 'recipe_submission.html', {'form': form, 'formset': formset})

# def submit_recipe(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         formset = IngredientFormSet(request.POST, instance=Recipes())

#         if form.is_valid() and formset.is_valid():
#             # Save the form data to the database
#             new_recipe = form.save(commit=False)
#             new_recipe.author = request.user  # Assuming you have user authentication
#             new_recipe.save()

#             for form in formset:
#                 ingredient = form.cleaned_data.get('ingredient')
#                 quantity = form.cleaned_data.get('quantity')
#                 if ingredient and quantity:
#                     recipe_ingredient = form.save(commit=False)
#                     recipe_ingredient.recipe = new_recipe
#                     recipe_ingredient.save()

#             messages.success(request, 'Recipe submitted successfully!')
#             # return redirect('recipe-detail', pk=new_recipe.pk)  # Redirect to recipe detail page
#             return redirect(f'/recipe/{new_recipe.pk}/')

#     else:
#         form = RecipeForm()
#         formset = IngredientFormSet(instance=Recipes())

#     return render(request, 'recipe_submission.html', {'form': form, 'formset': formset})

# def submit_recipe(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         formset = IngredientFormSet(request.POST, instance=new_recipe)
#         print("Made it to right before checking if form is valid...")
#         if form.is_valid() and formset.is_valid():
#             new_recipe = form.save(commit=False)
#             new_recipe.author = request.user
#             new_recipe.save()

#             print("Made it before the for form in formset")
#             for form in formset:
#                 ingredient_name = form.cleaned_data.get('ingredient')
#                 quantity = form.cleaned_data.get('quantity')

#                 print(f'Type of ingredient: {type(ingredient)}')
#                 # Create or get the Ingredient instance
#                 ingredient = Ingredient.objects.get_or_create(name=ingredient_name)

#                 # Create the RecipeIngredient instance and set the ingredient field
#                 recipe_ingredient = RecipeIngredient(recipe=new_recipe, ingredient=ingredient, quantity=quantity)
#                 recipe_ingredient.save()

#             messages.success(request, 'Recipe submitted successfully!')
#             return redirect('recipe_detail', recipe_id=new_recipe.pk)

#     else:
#         form = RecipeForm()
#         formset = IngredientFormSet(instance=Recipes())

#     return render(request, 'recipe_submission.html', {'form': form, 'formset': formset})

def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = IngredientFormSet(request.POST)

        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()

            if formset.is_valid():
                formset.instance = new_recipe  
                formset.save()  

                return redirect('recipe_detail', recipe_id=new_recipe.pk)

    else:
        form = RecipeForm()
        formset = IngredientFormSet()

    return render(request, 'recipe_submission.html', {'form': form, 'formset': formset})

# Login Page View
def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello {user.username}! You have successfully logged in!', extra_tags='alert alert-success')
                return redirect('recipe-home')
            else:
                message = 'Login failed!'
    return render(request, 'login.html', context={'form': form, 'message': message})

# Logout
def logout_user(request):
    logout(request)
    messages.success(request, f'You have successfully logged out!', extra_tags='alert alert-primary')
    return redirect('recipe-home')

# User Profile View
def user_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'profile.html', {'user_profile': user_profile})

# Edit User Profile View, Requires user to be logged in
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='edit-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

# Change Password View
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('edit-profile')

# Search Bar
def search_bar(request):
    query = request.GET.get('query')

    if query:
        # Normalize query and content to lower case for case-insensitive search
        query = query.strip()
        results = Recipe.objects.filter(content__icontains=query)
    else:
        results = None

    return render(request, 'search.html', {'results': results, 'query': query})

# Recipe Detail View
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = recipe.recipeingredient_set.all()
    ratings = Rating.objects.filter(recipe=recipe)
    average_rating = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']

    return render(request, 'recipe_detail.html', {'recipe': recipe, 'average_rating': average_rating, 'ingredients': ingredients})

# Rating Submission requires login
@login_required(login_url='/login/')
def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user_rating = int(request.POST.get('rating'))
        
        Rating.objects.create(user=request.user, recipe=recipe, rating=user_rating)
        
    return redirect('recipe_detail', recipe_id=recipe_id)