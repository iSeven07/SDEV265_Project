# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#          utils.py       #
# = = = = = = = = = = = = #

# This file was created to handle our API calls to Edamam for
# nutritional information. We can import utils into other areas
# of oura pplication so that we can call fetch_nutrition_data or
# other functions not page specific. 

import requests
from decouple import config

# Queries Edamam API for nutritional data
def fetch_nutrition_data(ingredient_name, quantity=None):
    app_id = config('EDAMAM_APP_ID', default='') # YOU MUST HAVE A .ENV WITH YOUR OWN APP ID
    app_key = config('EDAMAM_APP_KEY', default='') # YOU MUST HAVE A .ENV WITH YOUR OWN APP KEY

    base_url = "https://api.edamam.com/api/nutrition-data"
    query_params = {
        "app_id": app_id,
        "app_key": app_key,
        "ingr": f"{quantity or 1} {ingredient_name}",
    }

    response = requests.get(base_url, params=query_params)

    # Make sure the request is valid
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
