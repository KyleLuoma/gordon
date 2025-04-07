from flask import Flask
from flask_cors import CORS
from flask import request, jsonify

from recipe_ingredient_getter.RecipeIngredientGetter import (
    Ingredient,
    Recipe,
    RecipeIngredientGetter
)

from htmx_utils.table_builder import TableBuilder

app = Flask(__name__)
app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['PUT'])
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/submit_recipe_text', methods=["POST"])
def submit_recipe_text():
    if "recipe_text" not in request.form or "user_name" not in request.form:
        return jsonify({"error": "Missing 'recipe_text' or 'user_name' parameter"}), 400

    recipe_text = request.form.get("recipe_text")
    user_name = request.form.get("user_name")
    recipe_name = request.form.get("recipe_name")
    recipe_source = request.form.get("recipe_source")

    ingredient_getter = RecipeIngredientGetter(user=user_name)
    ingredient_getter.add_recipe_to_database(
        recipe_name=recipe_name if recipe_name else "",
        recipe_text=recipe_text,
        source=recipe_source if recipe_source else ""
    )
    return jsonify({"message": "Recipe saved successfully"}), 200


@app.route("/get_user_recipes", methods=["GET"])
def get_user_recipes():
    if "user_name" not in request.args:
        return jsonify({"error": "Missing 'user_name' parameter"}), 400
    user_name = request.args.get("user_name")
    ingredient_getter = RecipeIngredientGetter(user=user_name) 
    recipes = ingredient_getter.get_all_recipes_from_db()
    return TableBuilder.row_wise_dict_list_to_html_table(
        dict_list=[
            {
                "Recipe": recipe.name,
                "Source": recipe.source
            } for recipe in recipes
        ],
        table_id="recipe-list-table",
        thead_id="recipe-list-table-head",
        tbody_id="recipe-list-table-body",
        row_ids=[
            f"recipe-{recipe.id}-row" for recipe in recipes
            ]
    )

@app.route("/get_recipe_ingredients", methods=["POST"])
def get_recipe_ingredients():

    user_name = request.form.get("user_name")
    recipe_ids = request.form.get("recipe_ids")

    missing_user_name = ""
    missing_recipe_ids = ""
    if not user_name:
        missing_user_name = "missing user name"
    if not recipe_ids:
        missing_recipe_ids = "missing recipe ids"
    if not user_name or not recipe_ids:
        return jsonify({"error": f"{missing_user_name}, {missing_recipe_ids}"}), 400

    ingredient_getter = RecipeIngredientGetter(user=user_name)
    if type(recipe_ids) == str and "[" in recipe_ids and "]" in recipe_ids:
        recipe_ids = recipe_ids.replace("[","").replace("]","").split(",")
        recipe_ids = [int(rid) for rid in recipe_ids if rid.strip().isnumeric()]
        ingredients = ingredient_getter.get_ingredients_for_recipes(recipe_ids)
    
    if len(recipe_ids) == 0 or type(recipe_ids) != list:
        ingredients = [
            Ingredient(
                category="",
                name="",
                unit_of_measurement="",
                amount="",
                recipe_id=None
            )
        ]

    return TableBuilder.row_wise_dict_list_to_html_table(
        dict_list=[
            {
                "Category": ingredient.category,
                "Ingredient": ingredient.name,
                "Unit": ingredient.unit_of_measurement,
                "Amount": ingredient.amount
            } for ingredient in ingredients
        ],
        table_id="ingredient-list-table",
        thead_id="ingredient-list-table-head",
        tbody_id="ingredient-list-table-body",
        row_ids=True
    )
