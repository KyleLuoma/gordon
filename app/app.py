from flask import Flask
from flask_cors import CORS
from flask import request, jsonify

from recipe_ingredient_getter.RecipeIngredientGetter import (
    Ingredient,
    Recipe,
    RecipeIngredientGetter
)

app = Flask(__name__)
app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['PUT'])
def hello_world():
    return '<p>Hello, World!</p>'


@app.route("/get_user_recipes", methods=["GET"])
def get_user_recipes():
    if "user_name" not in request.args:
        return jsonify({"error": "Missing 'user_name' parameter"}), 400
    user_name = request.args.get("user_name")
    ingredient_getter = RecipeIngredientGetter(user=user_name)
    return jsonify([
        ingredient.__dict__ for ingredient in 
        ingredient_getter.get_all_recipes_from_db()
        ])
