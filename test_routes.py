import unittest
import requests
from flask_app import app
from flask import render_template,redirect,request,session,flash,Flask,url_for
from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)  

class TestRoutes(unittest.TestCase):
    URL = "http://127.0.0.1:5000"

    def test_index(self):
        res = requests.get(f"{self.URL}/")
        self.assertEqual(res.status_code, 200)

    def test_register(self):
        pw_hash = bcrypt.generate_password_hash('Password123')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": 'Password123',
            "cpassword": 'Password123'
        }
        res = requests.post(f"{self.URL}/register", data=data)
        self.assertEqual(res.status_code, 200)

    # Google mail server has disabled less secure app accessing it, does this feature will be disabled
    # def test_confirm_email(self):
    #     token = "valid_token_here"  # Replace with a valid token
    #     res = requests.get(f"{self.URL}/confirm_email/{token}")
    #     self.assertEqual(res.status_code, 200)

    # def test_resend(self):
    #     data = {
    #         "re_email": "johndoe@example.com"
    #     }
    #     res = requests.post(f"{self.URL}/resend", data=data)
    #     self.assertEqual(res.status_code, 200)

    def test_login(self):
        data = {
            "lemail": "johndoe@example.com",
            "lpassword": "Password123"
        }
        res = requests.post(f"{self.URL}/login", data=data)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        res = requests.get(f"{self.URL}/logout")
        self.assertEqual(res.status_code, 200)

    def test_dashboard(self):
        res = requests.get(f"{self.URL}/dashboard")
        self.assertEqual(res.status_code, 200)

    def test_account(self):
        res = requests.get(f"{self.URL}/account")
        self.assertEqual(res.status_code, 200)

    def test_create_application(self):
        res = requests.get(f"{self.URL}/new/application")
        self.assertEqual(res.status_code, 200)

    def test_watchlist(self):
        data = {
            "pet_name": "Buddy",
            "pet_url": "https://www.example.com/pet/buddy"
        }
        res = requests.post(f"{self.URL}/watch", data=data)
        self.assertEqual(res.status_code, 200)

    def test_view_pet(self):
        pet_id = 1  # Replace with a valid pet ID
        res = requests.get(f"{self.URL}/pet/{pet_id}")
        self.assertEqual(res.status_code, 200)

    def test_edit_pet(self):
        pet_id = 1  # Replace with a valid pet ID
        res = requests.get(f"{self.URL}/pet/{pet_id}/edit")
        self.assertEqual(res.status_code, 200)

    def test_update_pet(self):
        pet_id = 1  # Replace with a valid pet ID
        data = {
            "name": "Updated Buddy",
            "breed": "Labrador",
            "age": "5",
            "gender": "Male",
            "weight": "50 lbs",
            "description": "Friendly and active",
            "adopter_old_enough": "Yes",
            "adopter_stable_income": "Yes"
        }
        res = requests.post(f"{self.URL}/edit/{pet_id}", data=data)
        self.assertEqual(res.status_code, 200)

    def test_delete_pet(self):
        pet_id = 1  # Replace with a valid pet ID
        res = requests.get(f"{self.URL}/pet/{pet_id}/delete")
        self.assertEqual(res.status_code, 200)

    def test_about(self):
        res = requests.get(f"{self.URL}/about")
        self.assertEqual(res.status_code, 200)

    def test_search(self):
        res = requests.get(f"{self.URL}/input_search")
        self.assertEqual(res.status_code, 200)

    def test_input(self):
        data = {
            "location": "New York, NY",
            "animal": "Dog"
        }
        res = requests.post(f"{self.URL}/search", data=data)
        self.assertEqual(res.status_code, 200)

#  These two tests request an active HTTP request, might need to push a context. Consult the documentation on testing 
    # def test_api(self):
    #     with app.test_request_context():
    #     # Assuming session variables are set from /input_search
    #     session["animal"] = "Dog"
    #     session["location"] = "New York, NY"
    #     res = requests.get(f"{self.URL}/api", cookies=session)
    #     self.assertEqual(res.status_code, 200)

    # def test_delete_watch(self):
    #     session["watch_name"] = ['zoe', 'wendy', 'lucy']
    #     del_index = 0  # Replace with the appropriate index for deletion
    #     res = requests.get(f"{self.URL}/delete_watch/{del_index}", session=session)
    #     self.assertEqual(res.status_code, 200)
        
    def test_static_pages(self):
        pages = ["william", "gilbert", "beatrice", "shadow", "zoey", "azalea", "fry", "gucci"]
        for page in pages:
            res = requests.get(f"{self.URL}/{page}")
            self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    tester = TestRoutes()

    tester.test_index()
    tester.test_register()
    tester.test_confirm_email()
    tester.test_resend()
    tester.test_login()
    tester.test_logout()
    tester.test_dashboard()
    tester.test_account()
    tester.test_create_application()
    tester.test_watchlist()
    tester.test_delete_watch()
    tester.test_view_pet()
    tester.test_edit_pet()
    tester.test_update_pet()
    tester.test_delete_pet()
    tester.test_about()
    tester.test_search()
    tester.test_input()
    tester.test_api()
    tester.test_static_pages()

