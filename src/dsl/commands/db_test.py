import sqlite3
import unittest

from src.dsl.commands.sln import *
from src.dsl.commands.db import create_db, delete_db, execute_query


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

