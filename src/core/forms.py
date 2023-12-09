from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Profile, RecipeIngredient, Ingredient

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

# class IngredientForm(forms.ModelForm):
#     ingredient = forms.CharField(max_length=63)
#     quantity = forms.DecimalField(required=True)

#     class Meta:
#         model = RecipeIngredient
#         fields = ['ingredient', 'quantity']
#         widgets = {
#             'ingredient': forms.TextInput(attrs={'placeholder': 'Enter ingredient name'}),
#         }

# IngredientFormSet = inlineformset_factory(Recipes, RecipeIngredient, form=IngredientForm, extra=1)

class IngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']
        widgets = {
            'ingredient': forms.TextInput(attrs={'placeholder': 'Enter ingredient name'}),
        }

    ingredient = forms.CharField(max_length=100, required=False)

    def clean_ingredient(self):
        ingredient_name = self.cleaned_data['ingredient']
        if not ingredient_name:
            return None  # Handle the case when the field is empty
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name, defaults={'calories': 0})
        return ingredient

IngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=IngredientForm, extra=1)

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'content']  # These are the fields you want to include in the form


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
