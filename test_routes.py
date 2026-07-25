# tests for the flask routes in web.py
# uses flask's test client so we dont need to run the actual server
import os
import unittest
from web import finsight

TEST_DB = 'test_userprofile.db'

class TestRoutes(unittest.TestCase):
    def setUp(self):
        # runs before every test, points app at a fresh test db
        import init_db
        init_db.DB_NAME = TEST_DB
        init_db.create_db()
        finsight.config['TESTING'] = True
        self.client = finsight.test_client()

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
        response = self.client.post('/register', data={'username': 'routetestuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, 302)

    def test_login_correct_password(self):
        self.client.post('/register', data={'username': 'routetestuser', 'password': 'testpassword123'})
        response = self.client.post('/login', data={'username': 'routetestuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/watchlist', response.location)

    def test_login_wrong_password(self):
        self.client.post('/register', data={'username': 'routetestuser', 'password': 'testpassword123'})
        response = self.client.post('/login', data={'username': 'routetestuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_add_and_view_watchlist(self):
        self.client.post('/user/0/watchlist/add', data={'ticker': 'AAPL'})
        response = self.client.get('/user/0/watchlist')
        self.assertIn(b'AAPL', response.data)

    def test_add_duplicate_watchlist_entry(self):
        # this only works now because we added the unique constraint earlier
        self.client.post('/user/0/watchlist/add', data={'ticker': 'AAPL'})
        response = self.client.post('/user/0/watchlist/add', data={'ticker': 'AAPL'})
        self.assertEqual(response.status_code, 302)

    def test_remove_from_watchlist(self):
        # using MSFT here instead of AAPL, since AAPL appears in the placeholder text on this page
        self.client.post('/user/0/watchlist/add', data={'ticker': 'MSFT'})
        self.client.post('/user/0/watchlist/remove/MSFT')
        response = self.client.get('/user/0/watchlist')
        self.assertNotIn(b'MSFT', response.data)

    def test_logout_clears_session(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()

