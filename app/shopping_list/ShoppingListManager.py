import sqlite3
from dataclasses import dataclass
import json
import time
from enum import Enum
from shopping_list import RecipeIngredientGetter
from typing import Union
import os

@dataclass
class AdditionalItem:
    id: str
    name: str
    category: str

class ShoppingListEntryType(Enum):
    ADDITIONAL_ITEM = "additional_item"
    RECIPE = "recipe"

@dataclass
class ShoppingListItem:
    entry_type: ShoppingListEntryType
    entry_id: str
    entry_object: Union[AdditionalItem | RecipeIngredientGetter.Ingredient]

@dataclass
class ShoppingList:
    id: str
    name: str
    created_at: str
    items: list[ShoppingListItem]

@dataclass
class CombinedShoppingListItem:
    shopping_list_id: str
    shopping_list_item_id: str
    category: str
    item_name: str
    ingredient_recipes: list
    unit_of_measurement: str
    amount: float


class ShoppingListManager:

    def __init__(
            self, 
            user: str = "test",
            build_db_on_init: bool = False
            ):
        self.user = user
        db_path = f"./recipe_ingredient_getter/db/{user}.sqlite"
        db_exists = os.path.exists(db_path)
        self.db_conn = sqlite3.connect(db_path)
        if not db_exists or build_db_on_init:
            with open("./recipe_ingredient_getter/ingredient_db_builder.sql") as f:
                build_query = f.read()
                statements = build_query.split(";")
            cursor = self.db_conn.cursor()
            for statement in statements:
                cursor.execute(statement)
            self.db_conn.commit()
        self.recipe_ingredient_getter = RecipeIngredientGetter.RecipeIngredientGetter(
            build_db_on_init=False,
            user = self.user
        )

    def make_new_list(
            self,
            name: str,
            items: list[Union[AdditionalItem | RecipeIngredientGetter.Ingredient]] = None
            ) -> ShoppingList:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        new_list_query = f"""
INSERT INTO shopping_list (
    name, created_at
) VALUES (
    ?, ?
)
"""
        cur = self.db_conn.cursor()
        cur.execute(new_list_query, [name, timestamp])
        self.db_conn.commit()
        get_list_id_query = f"""
SELECT MAX(id) FROM shopping_list WHERE name = '{name}' and created_at = '{timestamp}'
"""
        cur.execute(get_list_id_query)
        list_id = int(cur.fetchall()[0][0])
        shopping_list = ShoppingList(
            id=list_id,
            name=name,
            created_at=timestamp,
            items=items or []
        )
        if not items:
            return shopping_list
        for item in items:
            shopping_list.items.append(item)
            if type(item) == AdditionalItem:
                self.add_additional_item_to_list(shopping_list.id, item)
            elif type(item) == RecipeIngredientGetter.Recipe:
                self.add_recipe_to_list(shopping_list.id, item)
        return shopping_list


    def add_additional_item_to_list(self, list_id: int, item: AdditionalItem):
        add_item_query = """
INSERT INTO shopping_list_items (shopping_list_id, entry_type, entry_id) VALUES (?, ?, ?)
"""
        cur = self.db_conn.cursor()
        cur.execute(add_item_query, [list_id, ShoppingListEntryType.ADDITIONAL_ITEM, item.id])
        self.db_conn.commit()


    def add_recipe_to_list(self, list_id: int, recipe: RecipeIngredientGetter.Recipe):
        add_recipe_query = """
INSERT INTO shopping_list_items (shopping_list_id, entry_type, entry_id) VALUES (?, ?, ?)
"""
        cur = self.db_conn.cursor()
        cur.execute(add_recipe_query, [list_id, ShoppingListEntryType.RECIPE, recipe.id])
        self.db_conn.commit()


    def remove_entry_from_list(self, shopping_list_item_id: int):
        remove_entry_query = """
        UPDATE shopping_list_items
        SET removed = 1
        WHERE id = ?
"""
        cur = self.db_conn.cursor()
        cur.execute(remove_entry_query, [shopping_list_item_id])
        self.db_conn.commit()


    def get_combined_shopping_list_items(self, list_id: int) -> list[CombinedShoppingListItem]:
        get_list_query = f"""
SELECT 
    shopping_list_id,
    shopping_list_item_id,
    category,
    item_name,
    ingredient_recipes,
    unit_of_measurement,
    amount
FROM combined_shopping_list_view
WHERE shopping_list_id = {list_id}
"""
        cur = self.db_conn.cursor()
        cur.execute(get_list_query)
        clist = []
        for row in cur.fetchall():
            clist.append(CombinedShoppingListItem(
                shopping_list_id=list_id,
                shopping_list_item_id=row[1],
                category=row[2],
                item_name=row[3],
                ingredient_recipes=[entry.strip() for entry in row[4].split(",")] if "," in row[3] else row[3],
                unit_of_measurement=row[5],
                amount=row[6]
            ))
        return clist