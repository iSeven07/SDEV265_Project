from django.core.management.base import BaseCommand
from core.models import Ingredient
from core.utils import fetch_nutrition_data
import time

class Command(BaseCommand):
    help = 'Update nutrition data for all ingredients'

    def handle(self, *args, **options):
        # Get all ingredients from the database
        ingredients = Ingredient.objects.all()

        for ingredient in ingredients:
            # Fetch nutrition data for each ingredient
            nutrition_data = fetch_nutrition_data(ingredient.name)

            if nutrition_data and "calories" in nutrition_data:
                # Update the ingredient with nutrition data
                ingredient.calories = nutrition_data.get("calories", 0)
                ingredient.protein = nutrition_data.get("protein", 0)
                ingredient.fat = nutrition_data.get("fat", 0)
                ingredient.carbohydrates = nutrition_data.get("carbs", 0)
                ingredient.save()
                print(ingredient.name + " updated.")

                time.sleep(6)

        self.stdout.write(self.style.SUCCESS('Successfully updated nutrition data for all ingredients.'))