import requests
from decouple import config

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
