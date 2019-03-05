import os
import unittest
from Test import app, db

TEST_DB = 'site.db'

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()



    # executed after each test
    def tearDown(self):
        pass
###############
#### tests ####
###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def register(self, username, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(username = username,  email=email, password=password, confirmPassword=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_valid_user_registration(self):
        response = self.register('Mitali', 'mitali@gmail.com', '123', '123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created. You can now login', response.data)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsNotAwesome')
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_duplicate_email(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.register('Mitali Singh', 'mitali@gmail.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'Email already exists', response.data)

    def test_invalid_user_registration_duplicate_username(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.register('Mitali', 'mitali123@gmail.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'Username already exists', response.data)



if __name__ == "__main__":
    unittest.main()
