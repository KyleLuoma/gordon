from recipe_ingredient_getter.RecipeIngredientGetter import (
    Ingredient,
    RecipeIngredientGetter
)

def main():
    recipes = [
        ("Corned Beef and Cabbage", "nyt_corned_beef.txt", "New York Times"),
        ("Shrimp Burgers", "nyt_shrimp_burgers.txt", "New York Times"),
        ("Gombaleves (Creamy Mushroom Soup)", "nyt_gombaleves.txt", "New York Times"),
        (
            "Roasted Spiced Squash With Whipped Feta and Pistachios",
            "nyt_roasted_squash_with_feta_and_pistachios.txt",
            "New York Times"
        )  
    ]

    recipe_folder = "./recipe_ingredient_getter/recipe_text"
    ingredient_getter = RecipeIngredientGetter()

    for recipe in recipes:
        with open(f"{recipe_folder}/{recipe[1]}") as f:
            recipe_text = f.read()
        ingredient_getter.add_recipe_to_database(
            recipe_name=recipe[0],
            recipe_text=recipe_text,
            source=recipe[2]
        )

if __name__ == "__main__":
    main()