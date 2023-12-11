from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Profile, RecipeIngredient, Ingredient
from .utils import fetch_nutrition_data

# User registration form
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# Recipe submission form
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'content', 'ingredients']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']
        widgets = {
            'ingredient': forms.TextInput(attrs={'placeholder': 'Enter ingredient name', 'readonly': 'readonly'}),
        }

    ingredient = forms.CharField(max_length=100, required=False)
    quantity = forms.DecimalField(max_digits=5, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the display of ingredient names
        if self.instance and self.instance.ingredient:
            self.initial['ingredient'] = str(self.instance.ingredient.name)

    def clean_ingredient(self):
        ingredient_name = self.cleaned_data['ingredient']
        print(f'Cleaned Ingredient Name: {ingredient_name}')
        if not ingredient_name:
            return None  # Handle the case when the field is empty

        nutrition_data = fetch_nutrition_data(ingredient_name)
        if nutrition_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name,
                defaults={
                    'calories': nutrition_data['calories'],
                    'protein': nutrition_data['protein'],
                    'fat': nutrition_data['fat'],
                    'carbohydrates': nutrition_data['carbs'],
                }
            )
            return ingredient
        else:
            # If nutrition data is not available, create the Ingredient object with default values
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name,
                defaults={'calories': 0, 'protein': 0, 'fat': 0, 'carbohydrates': 0}
            )
            return ingredient

IngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=IngredientForm, extra=1)

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'content', 'instructions']  # These are the fields you want to include in the form


# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


# Profile update form
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]


# Update avatar/picture
class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control-file"})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5})
    )

    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
