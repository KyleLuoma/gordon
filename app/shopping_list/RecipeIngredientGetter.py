import sqlite3
from llm_service.GoogleLLMService import GoogleLLMService
from dataclasses import dataclass
import json
import os

@dataclass
class Ingredient:
    name: str
    recipe_id: int
    unit_of_measurement: str
    amount: float
    category: str

@dataclass
class Recipe:
    id: str
    name: str
    full_text: str
    source: str

class RecipeIngredientGetter:

    def __init__(
            self, 
            llm: GoogleLLMService = None,
            user: str = "test",
            build_db_on_init: bool = False
            ):
        db_path = f"./recipe_ingredient_getter/db/{user}.sqlite"
        db_exists = os.path.exists(db_path)
        self.db_conn = sqlite3.connect(db_path)
        if llm == None:
            self.llm = GoogleLLMService()
        else:
            self.llm = llm
        if build_db_on_init or not db_exists:
            with open("./recipe_ingredient_getter/ingredient_db_builder.sql") as f:
                build_query = f.read()
                statements = build_query.split(";")
            cursor = self.db_conn.cursor()
            for statement in statements:
                cursor.execute(statement)
            self.db_conn.commit()


    def get_all_ingredients_from_db(self) -> list[str]:
        get_query = "select distinct name from ingredients"
        cursor = self.db_conn.cursor()
        result = cursor.execute(get_query)
        return [row[0] for row in result.fetchall()]
    

    def get_all_recipes_from_db(self) -> list[Recipe]:
        get_query = "select id, name, full_text, recipe_source from recipes"
        cursor = self.db_conn.cursor()
        result = cursor.execute(get_query)
        recipes = [Recipe(
            id=row[0],
            name=row[1],
            full_text=row[2],
            source=row[3]
        ) for row in result.fetchall()]
        return recipes

    

    def get_all_measurement_units_from_db(self) -> list[str]:
        get_query = "select distinct unit_of_measurement from ingredients"
        cursor = self.db_conn.cursor()
        result = cursor.execute(get_query)
        return [row[0] for row in result.fetchall()]
    

    def get_all_categories_from_db(self) -> list[str]:
        get_query = "select distinct category from ingredients"
        cursor = self.db_conn.cursor()
        result = cursor.execute(get_query)
        return [row[0] for row in result.fetchall()]
    

    def parse_ingredient_list_from_llm_response(
            self, 
            llm_response: str,
            recipe_id: int,
            start_delimiter: str = "```json",
            end_delimiter: str = "```"
            ) -> list[Ingredient]:
        start_index = llm_response.find(start_delimiter) + len(start_delimiter)
        end_index = llm_response.find(end_delimiter, start_index)
        json_data = llm_response[start_index:end_index].strip()

        try:
            ingredients_list = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from LLM response: {e}")
        
        ingredients = []
        failed_to_add = []
        for item in ingredients_list:
            try:
                new_ingr = Ingredient(
                    name=item["name"],
                    recipe_id=recipe_id,
                    unit_of_measurement=item["unit"],
                    amount=item["amount"],
                    category=item["category"]
                )
                ingredients.append(new_ingr)
            except KeyError as e:
                failed_to_add.append(item)
        return ingredients

    
    def extract_ingredients_from_text_recipe(
            self, 
            recipe_text: str,
            recipe_id: int
            ) -> list[Ingredient]:
        
        with open("./recipe_ingredient_getter/prompts/make_recipe_json.prompt", "rt") as f:
            prompt = f.read()
        prompt = prompt.replace("__RECIPE_TEXT__", recipe_text)

        db_ingredients = self.get_all_ingredients_from_db()
        ingredient_prompt = ""
        for ingr in db_ingredients:
            ingredient_prompt += f"- {ingr}\n"
        prompt = prompt.replace("__INGREDIENT_LIST__", ingredient_prompt)

        db_units = self.get_all_measurement_units_from_db()
        unit_prompt = ""
        for unit in db_units:
            unit_prompt += f"- {unit}\n"
        prompt = prompt.replace("__UNIT_LIST__", unit_prompt)

        db_categories = self.get_all_categories_from_db()
        categ_prompt = ""
        for categ in db_categories:
            categ_prompt += f"- {categ}\n"
        prompt = prompt.replace("__CATEGORY_LIST__", categ_prompt)

        llm_response = self.llm.send_prompt(prompt)

        try:
            ingredients = self.parse_ingredient_list_from_llm_response(
                llm_response=llm_response,
                recipe_id=recipe_id
                )
        except ValueError as e:
            return []
        return ingredients
    

    def recover_failed_items(self, failed_items: list) -> list[Ingredient]:
        with open("./recipe_ingredient_getter/prompts/recover_failed_adds.prompt", "rt") as f:
            prompt = f.read()
        item_prompt = "[\n"
        for item in failed_items:
            item_prompt += str(item)
            item_prompt += "\n"
        item_prompt += "]"
        prompt = prompt.replace("__FAILED_ITEMS__", item_prompt)


    def add_recipe_to_database(self, recipe_name: str, recipe_text: str, source: str):
        query = "insert into recipes (name, full_text, recipe_source) values (?, ?, ?)"
        cursor = self.db_conn.cursor()
        cursor.execute(query, [recipe_name, recipe_text, source])
        self.db_conn.commit()
        query = f"select max(id) from recipes where name = '{recipe_name}'"
        cursor.execute(query)
        recipe_id = int(cursor.fetchall()[0][0])
        ingredients = self.extract_ingredients_from_text_recipe(
            recipe_text=recipe_text,
            recipe_id=recipe_id
        )
        query = f"insert into ingredients (name, recipe_id, unit_of_measurement, amount, category) values (?, ?, ?, ?, ?)"
        for ingredient in ingredients:
            if ingredient.unit_of_measurement == None:
                ingredient.unit_of_measurement = "None"
            if ingredient.amount == None:
                ingredient.amount = -1
            cursor.execute(
                query, 
                [
                    ingredient.name, 
                    ingredient.recipe_id, 
                    ingredient.unit_of_measurement,
                    ingredient.amount,
                    ingredient.category
                ]
                )
        self.db_conn.commit()

    def get_ingredients_for_recipes(self, recipe_ids: list[int]) -> list[Ingredient]:
        print("DEBUG", recipe_ids, type(recipe_ids))
        query = """
        select category, name, unit_of_measurement, sum(amount) as amount
        from ingredients
        where amount > 0 and recipe_id in ({})
        group by category, name, unit_of_measurement

        union

        select category, name, unit_of_measurement, count(amount) as amount
        from ingredients
        where amount = -1 and recipe_id in ({})
        group by category, name, unit_of_measurement
        """.format(",".join("?" for _ in recipe_ids), ",".join("?" for _ in recipe_ids))
        
        cursor = self.db_conn.cursor()
        result = cursor.execute(query, recipe_ids + recipe_ids)
        rows = result.fetchall()

        ingredients = []
        for row in rows:
            ingredients.append(Ingredient(
                category=row[0],
                name=row[1],
                unit_of_measurement=row[2],
                amount=row[3],
                recipe_id=None
            ))
        return ingredients
