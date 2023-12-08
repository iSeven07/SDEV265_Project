from django.db import models
from PIL import Image
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

# Recipes Model for DB
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)  # Adjust the field type as needed
    
    class Meta:
        db_table = 'core_recipes_ingredients'

    def __str__(self):
        return self.title
    
# Rating system for recipe entries
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
# Extending User Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Avatars will require pillow, which has been added to requirements.txt
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField()

    # # resizing images
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.avatar.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)

    def __str__(self):
        return self.user.username