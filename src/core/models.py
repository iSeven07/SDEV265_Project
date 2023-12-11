# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#        models.py        #
# = = = = = = = = = = = = #

# Here is where we declare our Models. Models is what
# Django uses to create objects and store them in our database.
# You can also set requirements for fields here. Django will create
# a fresh database based off of these models as well.

from django.db import models
from PIL import Image
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Returns the name of the ingredient if referenced
    def __str__(self):
        return self.name

# Recipes Model 
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False, default='')
    instructions = models.TextField(blank=False, default='')
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    # Calculate nutrition function allows us to call it from our Recipe Detail page.
    # This allows us to display total calories, total protein, etc for each recipe.
    def calculate_total_nutrition(self):
        total_calories = 0
        total_protein = 0
        total_fat = 0
        total_carbohydrates = 0

        # Loop through each recipe ingredient
        for recipe_ingredient in self.recipeingredient_set.all():
            ingredient = recipe_ingredient.ingredient
            quantity = Decimal(recipe_ingredient.quantity)

            # Update totals based on the nutritional content of the ingredient and quantity
            total_calories += ingredient.calories * quantity
            total_protein += ingredient.protein * quantity
            total_fat += ingredient.fat * quantity
            total_carbohydrates += ingredient.carbohydrates * quantity

        # Return the results
        return {
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_fat': total_fat,
            'total_carbohydrates': total_carbohydrates,
        }

# Since we have a ManytoMany relationship between Recipe and Ingredient, this model
# helps us make that association. 
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)  # Adjust the field type as needed
    
    # The db_table needed to be declared here because we originally messed up on the naming convention.
    class Meta:
        db_table = 'core_recipes_ingredients'

    def __str__(self):
        return self.ingredient.name


# Rating system for recipe entries
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
# Extending User Model. Allows us to have additional profile properties, like a photo and bio.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Avatars will require pillow, which has been added to requirements.txt
    avatar = models.ImageField(default="default.png", upload_to="profile_images")
    bio = models.TextField()

    """
    # This code helps if we need to keep file size down for photos. We found that we did not
    # need to utilize it, but have kept it in case it would be useful in the future.
    def save(self, *args, **kwargs):
         super().save()

         img = Image.open(self.avatar.path)

         if img.height > 100 or img.width > 100:
             new_img = (100, 100)
             img.thumbnail(new_img)
             img.save(self.avatar.path)
    """

    def __str__(self):
        return self.user.username
