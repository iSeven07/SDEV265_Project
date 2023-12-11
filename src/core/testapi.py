# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#        testapi.py       #
# = = = = = = = = = = = = #

# When having issues with API calls within Recipe Builder
# This file helps in detecting if we are properly receiving
# data back.

import requests
from decouple import config

# This function uses the app_id and app_key to query a food item that it receives. 
def fetch_nutrition_data(ingredient_name, quantity=None):
    app_id = config('EDAMAM_APP_ID', default='')
    app_key = config('EDAMAM_APP_KEY', default='')

    base_url = "https://api.edamam.com/api/nutrition-data"
    query_params = {
        "app_id": app_id,
        "app_key": app_key,
        "ingr": f"{quantity or 1} {ingredient_name}",
    }

    response = requests.get(base_url, params=query_params)

    if response.status_code == 200:
        data = response.json()
        calories = data.get("calories", 0)
        nutrients = data.get("totalNutrients", {})

        return {
            "calories": calories,
            "protein": nutrients.get("PROCNT", {}).get("quantity", 0),
            "fat": nutrients.get("FAT", {}).get("quantity", 0),
            "carbs": nutrients.get("CHOCDF", {}).get("quantity", 0),
        }
    else:
        print(f"Could not retrieve nutrition data for {ingredient_name}.")
        return None

# This is a test case using "orange".
ingredient_name = "orange"
nutrition_data = fetch_nutrition_data(ingredient_name)

if nutrition_data:
    print(f"Nutrition Information for {ingredient_name}:")
    print(f"Calories: {nutrition_data['calories']} kcal")
    print(f"Protein: {nutrition_data['protein']} g")
    print(f"Fat: {nutrition_data['fat']} g")
    print(f"Carbohydrates: {nutrition_data['carbs']} g")
else:
    print(f"Could not retrieve nutrition data for {ingredient_name}.")
