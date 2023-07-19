import unittest
import sqlite3
import os

from db import create, delete, execute, execute_get_results


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
            delete(self.db_name)

    def test_create_db(self):
        # Test the create_db function
        create(self.db_name, self.schema)
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
        create(self.db_name, self.schema)
        self.assertTrue(os.path.exists(self.db_name))
        # Now, call the delete_db function
        delete(self.db_name)
        self.assertFalse(os.path.exists(self.db_name))

    def test_execute_query(self):
        # Test the execute_query function
        create(self.db_name, self.schema)
        query = "INSERT INTO users (username, email) VALUES ('test_user', 'test@example.com');"
        execute(self.db_name, query)
        # Optionally, you can check if the data was inserted correctly
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username='test_user';")
        user_data = cursor.fetchone()
        db.close()
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data[1], 'test_user')
        self.assertEqual(user_data[2], 'test@example.com')

    def test_execute_get_results(self):
        # Test the execute_get_results function

        # Step 1: Create a temporary database and insert test data
        create_db(self.db_name, self.schema)
        query = "INSERT INTO users (username, email) VALUES ('test_user1', 'test1@example.com'), ('test_user2', 'test2@example.com');"
        execute_query(self.db_name, query)

        # Step 2: Execute the query and get the results
        select_query = "SELECT * FROM users WHERE email LIKE '%@example.com';"
        results = execute_get_results(self.db_name, select_query)

        # Step 3: Check if the results are as expected
        expected_results = [('test_user1', 'test1@example.com'), ('test_user2', 'test2@example.com')]
        self.assertEqual(results, expected_results)

        # Alternatively, you can also check for specific values in the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], 'test_user1')
        self.assertEqual(results[0][1], 'test1@example.com')
        self.assertEqual(results[1][0], 'test_user2')
        self.assertEqual(results[1][1], 'test2@example.com')

if __name__ == '__main__':
    unittest.main()
