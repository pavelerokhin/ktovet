import sqlite3
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
    def setUp(self):
        context = {
            "db_name": "test.db",
            "schema": schema,
        }
        create_db(context=context)
        self.db = get_db(context.get("db_name"))

    def test_execute_query(self):
        query1 = "INSERT INTO test_table (name, age) VALUES ('test_user', 20);"
        execute_query(self.db, query1)
        query2 = "SELECT name, age FROM test_table;"

        execute_query_results(self.db, query2)

    def test_execute_query_results(self, mock_execute_get_results):
        # Test execute_query_results function
        db_mock = "test_db"
        query_mock = "SELECT * FROM test_table"
        context = {
            "db": db_mock,
            "query": query_mock,
        }
        context = execute_query_results(context=context, result_to="result")
        self.assertEqual(context.get("result"), mock_execute_get_results.return_value)

        mock_execute_get_results.assert_called_with(db=db_mock, query=query_mock)


if __name__ == '__main__':
    unittest.main()