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

    def account(self, username, email, picture):
        return self.app.post(
            '/account',
            data=dict(username = username, email=email, picture = picture),
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

    def test_invalid_user_registration_empty_username(self):
     response = self.register('', 'mitali123@gmail.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'This field is required', response.data)

    def test_invalid_user_registration_empty_email(self):
     response = self.register('Mitali', '', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'This field is required', response.data)

    def test_invalid_user_registration_empty_password(self):
     response = self.register('Mitali', 'm@gmail.com', '', 'FlaskIsReallyAwesome')
     self.assertIn(b'This field is required', response.data)

    def test_invalid_user_registration_empty_Cpassword(self):
     response = self.register('Mitali', 'm@gmail.com', 'hey', '')
     self.assertIn(b'This field is required', response.data)

    def test_invalid_user_registration_small_username(self):
     response = self.register('M', 'mitali123@gmail.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'Field must be between 2 and 20 characters long', response.data)

    def test_invalid_user_registration_long_username(self):
     response = self.register('abcdefghijklmnopqrstuvwxyz', 'mitali123@gmail.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'Field must be between 2 and 20 characters long', response.data)

    def test_invalid_user_registration_invalid_email(self):
     response = self.register('Mitali', 'mitali123gmail.com', 'FlaskIsReallyAwesome', 'FlaskIsReallyAwesome')
     self.assertIn(b'Invalid email address.', response.data)

    def test_valid_login(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.login('mitali@gmail.com', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)

    def test_invalid_login_invalidEmail(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.login('m', 'FlaskIsAwesome')
     self.assertIn(b'Invalid email address.', response.data)

    def test_invalid_login_invalidPassword(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.login('mitali@gmail.com', '1FlaskIsAwesome')
     self.assertIn(b'Login unsuccessful. Please check username and password', response.data)

    def test_invalid_login_emptyPassword(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.login('mitali@gmail.com', '')
     self.assertIn(b'This field is required', response.data)

    def test_invalid_login_emptyEmail(self):
     response = self.register('Mitali', 'mitali@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
     self.assertEqual(response.status_code, 200)
     response = self.login('', 'FlaskIsAwesome')
     self.assertIn(b'This field is required', response.data)

    def test_valid_account_registration(self):
        response = self.account('Mitali', 'mitali@gmail.com', 'default.jpeg')
        self.assertEqual(response.status_code, 200)

    def test_invalid_account_registration(self) :
        response = self.account('Mitali', 'mitali@gmail.com', 'Assignment.docx')
        self.assertIn(b'File does not have an approved extension: jpg, png', response.data)

if __name__ == "__main__":
    unittest.main()
