# import relevant packages
# unit tests for the database helper functions in init_db.py
# this will test the functions for creating the database, saving and loading users, and managing the watchlist
# to ensure that this is a seperate test database, we will create a new database file for testing so that the real userprofile.db will not be affected

import sqlite3 
import os
import unittest
from init_db import create_db, save_user, load_user, add_to_watchlist, get_watchlist, remove_from_watchlist

TEST_DB = 'test_userprofile.db'

class TestInitDB(unittest.TestCase):
    def setUp(self):
        # Create a test database, and import the relveant pacakges
        # runs before every test, creating a test db
        import init_db
        init_db.DB_NAME = TEST_DB
        create_db()

    def tearDown(self):
        # Remove the test database after each test
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_load_user(self):
        # saves a new user and loades them back from the database, checking that the username is correct
        save_user("johntest", "orbitalteam7666")
        result = load_user(1)
        self.assertEqual(result, "johntest")

    def test_duplicate_username(self):
        # saves a new user and attempts to save another user with the same username
        save_user("johntest", "orbitalteam7666")
        save_user("johntest", "anotherpassword")
        result = load_user(1)
        self.assertEqual(result, "johntest")

    def test_add_and_get_watchlist(self):
        save_user("johntest", "orbitalteam7666")
        add_to_watchlist(1, "AAPL")
        watchlist = get_watchlist(1)
        self.assertIn("AAPL", watchlist)

    def test_remove_from_watchlist(self):
        save_user("johntest", "orbitalteam7666")
        add_to_watchlist(1, "AAPL")
        remove_from_watchlist(1, "AAPL")
        watchlist = get_watchlist(1)
        self.assertNotIn("AAPL", watchlist)

    def test_remove_nonexistent_user(self):
        result = load_user(999)  # Assuming user ID 999 does not exist
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()