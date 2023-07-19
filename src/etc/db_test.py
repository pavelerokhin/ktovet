import unittest
import sqlite3
import os

from db import create_db, delete_db, execute_query


class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # This method is called before each test case runs.
        # You can use it to set up any necessary resources.
        # For example, we'll create a temporary database for testing.
        self.db_name = 'test_database.db'
        self.schema = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        '''

    def tearDown(self):
        # This method is called after each test case runs.
        # You can use it to clean up any resources created during testing.
        if os.path.exists(self.db_name):
            delete_db(self.db_name)

    def test_create_db(self):
        # Test the create_db function
        create_db(self.db_name, self.schema)
        self.assertTrue(os.path.exists(self.db_name))
        # Optionally, you can check if the table exists in the database
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = cursor.fetchone()
        db.close()
        self.assertIsNotNone(table_exists)

    def test_delete_db(self):
        # Test the delete_db function
        # First, create a temporary database to delete
        create_db(self.db_name, self.schema)
        self.assertTrue(os.path.exists(self.db_name))
        # Now, call the delete_db function
        delete_db(self.db_name)
        self.assertFalse(os.path.exists(self.db_name))

    def test_execute_query(self):
        # Test the execute_query function
        create_db(self.db_name, self.schema)
        query = "INSERT INTO users (username, email) VALUES ('test_user', 'test@example.com');"
        execute_query(self.db_name, query)
        # Optionally, you can check if the data was inserted correctly
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username='test_user';")
        user_data = cursor.fetchone()
        db.close()
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data[1], 'test_user')
        self.assertEqual(user_data[2], 'test@example.com')


if __name__ == '__main__':
    unittest.main()
