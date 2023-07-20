import unittest

from src.dsl.commands.sln import *
from src.dsl.commands.db import *
from src.etc.db import get_db


schema = "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL);"


class TestsDbCommands(unittest.TestCase):
    def test_get_page(self):
        context = {
            "db_name": "test.db",
            "schema": schema,
        }

        # Call the function
        context = create_db(context=context)

        # Check if the database was created
        self.assertTrue(os.path.exists(context.get("db_name")))

        # delete the database
        delete_db(context=context)

        # Check if the database was created
        self.assertFalse(os.path.exists(context.get("db_name")))


class TestDBFunctions(unittest.TestCase):
    def setUp(self) -> None:
        context = {
            "db_name": "test.db",
            "schema": schema,
        }
        create_db(context=context)
        self.context = context
        self.db = get_db(context.get("db_name"))

    def tearDown(self) -> None:
        delete_db(context=self.context)
        self.db = None

    def test_execute_query(self):
        query1 = "INSERT INTO test (name, age) VALUES ('test_user', 20);"
        context = self.context
        context["query"] = query1
        context["db"] = self.db
        context = execute_query(context=context)

        query2 = "SELECT name, age FROM test;"
        context["query"] = query2
        context = execute_query_results(context=context, db=self.db, result_to="result")
        self.assertIsNotNone(context.get("result"))

    def test_execute_query_results(self):
        # Test execute_query_results function
        context = self.context
        context["query"] = "SELECT * FROM test"
        context["db"] = self.db

        context = execute_query_results(context=context, result_to="result")
        self.assertIsNotNone(context.get("result"))


if __name__ == '__main__':
    unittest.main()