from shopping_list.ShoppingListManager import (
    AdditionalItem,
    ShoppingListEntryType,
    ShoppingListItem,
    ShoppingList,
    CombinedShoppingListItem,
    ShoppingListManager
)
import os

class TestShoppingListManager:

    def test_make_new_list(self):
        slm = ShoppingListManager(
            user = "pytest_make_new_list",
            build_db_on_init=True
        )
        new_list = slm.make_new_list(
            name="test-list"
        )
        slm.db_conn.close()
        
        assert type(new_list) == ShoppingList

    def test_add_additional_item_to_list(self):
        slm = ShoppingListManager(
            user = "pytest_add_additional_item_to_list",
            build_db_on_init=True
        )
        new_list = slm.make_new_list(
            name="test-list"
        )
        slm.add_additional_item_to_list(
            list_id=new_list.id,
            item = AdditionalItem(
                id=1,
                name="test-item",
                category="test-category"
            )
        )
        slist = slm.get_combined_shopping_list_items(new_list.id)
        slm.db_conn.close()
        assert slist[0].item_name == "test-item"

    def test_db_cleanup(self):
        db_path = "./shopping_list/db/" 
        dbs = [
            "pytest_make_new_list.sqlite",
            "pytest_add_additional_item_to_list.sqlite"
            ]
        for db in dbs:
            if os.path.exists(f"{db_path}/{db}"):
                os.remove(f"{db_path}/{db}")
        assert True


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_class = TestShoppingListManager()
    test_class.test_make_new_list()
    test_class.test_add_additional_item_to_list()
    test_class.test_db_cleanup()