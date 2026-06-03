from flask import Flask
from flask_cors import CORS
from flask import request, jsonify

from shopping_list.RecipeIngredientGetter import (
    Ingredient,
    Recipe,
    RecipeIngredientGetter
)

from shopping_list.ShoppingListManager import (
    AdditionalItem,
    ShoppingListEntryType,
    ShoppingListItem,
    ShoppingList,
    CombinedShoppingListItem,
    ShoppingListManager
)

from htmx_utils.form_builder import (
    FormBuilder,
    InputType,
    LabelElement,
    InputElement
)

from htmx_utils.table_builder import TableBuilder

app = Flask(__name__)
app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['PUT'])
def hello_world():
    return '<p>Hello, World!</p>'


@app.route("/submit_recipe_url", methods=["POST"])
def submit_recipe_url():
    if "recipe_url" not in request.form or "user_name" not in request.form:
        return jsonify({"error": "Missing 'recipe_url' or 'user_name' parameter"}), 400
    
    recipe_url = request.form.get("recipe_url")
    user_name = request.form.get("user_name")
    ingredient_getter = RecipeIngredientGetter(user=user_name)
    response = ingredient_getter.add_recipe_to_database_from_url(
        recipe_url=recipe_url
    )
    return jsonify({"message": response}), 200




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
    if len(recipes) == 0:
        return ""
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

@app.route("/get_user_recipes_as_form", methods=["GET"])
def get_user_recipes_as_form():
    if "user_name" not in request.args:
        return jsonify({"error": "Missing 'user_name' parameter"}), 400
    user_name = request.args.get("user_name")
    ingredient_getter = RecipeIngredientGetter(user=user_name) 
    recipes = ingredient_getter.get_all_recipes_from_db()
    form_builder = FormBuilder(include_form_tags=False)
    for recipe in recipes:
        form_builder.add_element(InputElement(
            type=InputType.CHECKBOX,
            id=f"recipe-checkbox-{recipe.id}",
            name=f"recipe_ids",
            value=recipe.id,
            css_class="recipe-checkbox"
        ))
        form_builder.add_element(LabelElement(
            for_attr=f"{recipe.name}-{recipe.id}",
            label_text=recipe.name,
            linebreaks=1
        ))
    return str(form_builder)
    

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

@app.route("/get_combined_shopping_list_items", methods=["POST"])
def get_combined_shopping_list_items():
    user_name = request.form.get("user_name").strip()
    list_id = request.form.get("list_id").strip()
    if not user_name or not list_id:
        return jsonify({"error": f"Missing required parameter."}), 400
    list_manager = ShoppingListManager(user=user_name)
    combined_ingredients = list_manager.get_combined_shopping_list_items(
        list_id=int(list_id)
    )
    ing_table = TableBuilder.row_wise_dict_list_to_html_table(
        dict_list=[{
            "Category": ing.category,
            "Ingredient": ing.item_name,
            "Unit": ing.unit_of_measurement,
            "Amount": ing.amount,
            "From": ", ".join(ing.ingredient_recipes)
        } for ing in combined_ingredients],
        table_id="shopping-list-table",
        thead_id="shopping-list-table-head",
        tbody_id="shopping-list-table-body"
    )
    return ing_table


@app.route("/add_additional_item_to_list", methods=["POST"])
def add_additional_item_to_list():
    user_name = (request.form.get("user_name") or "").strip()
    list_id_raw = (request.form.get("list_id") or "").strip()
    item_name = (request.form.get("item_name") or "").strip()
    item_category = (request.form.get("item_category") or "").strip()

    missing_params = []
    if not user_name:
        missing_params.append("user_name")
    if not item_name:
        missing_params.append("item_name")
    if missing_params:
        return jsonify({"error": f"missing attributes: {','.join(missing_params)}"}), 400

    slm = ShoppingListManager(user=user_name)

    if list_id_raw.isnumeric():
        list_id = int(list_id_raw)
    else:
        cur = slm.db_conn.cursor()
        cur.execute("SELECT id FROM shopping_list ORDER BY id DESC LIMIT 1")
        last_row = cur.fetchone()
        if last_row:
            list_id = int(last_row[0])
        else:
            list_id = slm.make_new_list(name="Default Shopping List").id

    category = item_category or "Additional Items"
    slm.add_additional_item_to_list(
        list_id=list_id,
        item=AdditionalItem(
            id=-1,
            name=item_name,
            category=category
        )
    )

    combined_ingredients = slm.get_combined_shopping_list_items(list_id=list_id)
    return TableBuilder.row_wise_dict_list_to_html_table(
        dict_list=[{
            "Category": ing.category,
            "Ingredient": ing.item_name,
            "Unit": ing.unit_of_measurement,
            "Amount": ing.amount,
            "From": ", ".join(ing.ingredient_recipes) if isinstance(ing.ingredient_recipes, list) else ing.ingredient_recipes
        } for ing in combined_ingredients],
        table_id="shopping-list-table",
        thead_id="shopping-list-table-head",
        tbody_id="shopping-list-table-body",
        include_headers=False
    )


@app.route("/add_recipe_to_list", methods=["POST"])
def add_recipe_to_list():
    user_name = request.form.get("user_name").strip()
    list_id = request.form.get("list_id").strip()


@app.route("/get_additional_item_selections", methods=["GET"])
def get_additional_item_selections():
    user_name = request.args.get("user_name", "test")
    ingredient_getter = RecipeIngredientGetter(user=user_name)
    categories = ingredient_getter.get_all_categories_from_db()
    if len(categories) == 0:
        categories = ["Additional Items"]

    options = "\n".join([
        f'<option value="{category}">{category}</option>' for category in categories
    ])
    return (
        '<label for="item-category">Category:</label>'
        '<select id="item-category" name="item_category">'
        f'{options}'
        '</select>'
    )


@app.route("/make_new_shopping_list", methods=["POST"])
def make_new_shopping_list():
    user_name = request.form.get("user_name")
    list_name = request.form.get("list_name")
    missing_attr = []
    if not user_name:
        missing_attr.append("user_name")
    if not list_name:
        missing_attr.append("list_name")
    if len(missing_attr) > 0:
        return jsonify({"error": f"missing attributes: {','.join(missing_attr)}"}), 400
    
    slm = ShoppingListManager(user=user_name)
    new_list = slm.make_new_list(name=list_name)
    return f'<div id="shopping-list-{new_list.id}"><h3>Shopping List {new_list.name}</h3></div>'


