import unittest
import Webapps
import logging
logging.basicConfig(level=logging.ERROR)

class TestWebapps(unittest.TestCase):

    def test_index(self):
        rv = self.app.get('/index/')
        #print(rv)
        assert rv._status_code == 200
        assert b'Hello world' in rv.data
        logging.info('response code : %d',rv._status_code)

    def test_index_username(self):
        rv = self.app.get('/user/testuser1/')
        assert rv._status_code == 200
        assert b'Hello,testuser1' in rv.data

    def test_index_id(self):
        rv = self.app.get('/user/123/')
        assert rv._status_code == 200
        assert b'NO.123' in rv.data

    def test_index_path(self):
        rv = self.app.get('/user/123/aaa/')
        assert rv._status_code == 200
        assert b'your path:123/aaa' in rv.data

    def login(self,username,password):
        return self.app.post('/login',data=dict(
            username=username,
            password=password
        ),follow_redirects=True)

    def test_login(self):
        rv = self.login(username='admin',password='password')
        assert rv._status_code == 200
        assert b'Success' in rv.data
        logging.info('response code : %d', rv._status_code)

    def setUp(self):
        print("Start Server.......")
        self.app = Webapps.app.test_client()

if __name__ == "__main__":
    unittest.main()
