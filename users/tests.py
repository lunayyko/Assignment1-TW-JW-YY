import json, jwt

from django.test import TestCase, Client

from .models import User
from django.conf  import settings

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="bbb@wecode.com",
            name="파이썬",
            password="abcde12345@",
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        client = Client()
        user = {
            "email": "aaa@wecode.com",
            "name": "깔끔한",
            "password": "abcde12345@",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_duplication_user(self):
        client = Client()
        user = {
            "email": "bbb@wecode.com",
            "name": "탄탄한",
            "password": "abcde12345@@",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "ALREADY_EXISTED_EMAIL"})

    def test_email_format_error(self):
        client = Client()
        user = {
            "email": "cccwecode.com",
            "name": "파이썬",
            "password": "abcde12345@",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "EMAIL_ERROR"})
    
    def test_password_format_error(self):
        client = Client()
        user = {
            "email": "ddd@wecode.com",
            "name": "파이썬",
            "password": "abcde12345",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "PASSWORD_ERROR"})
    
    def test_key_error(self):
        client = Client()
        user = {
            "email": "eee@wecode.com",
            "name": "파이썬",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})

class LoginTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            email="yesjiwon5304@gmail.com",
            name="박지원구글",
            password="$2b$12$qC9kIeB0FiNPpo7f2SVzcuKDNznmKPbiUnAiCwc.UhQU5PmWDRP0S",
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_email_error(self):
        client = Client()
        user = {
            "email": "yesjiwon534@gmail.com",
            "password": "abcde12345@",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_USER"})

    def test_password_error(self):
        client = Client()
        user = {
            "email": "yesjiwon5304@gmail.com",
            "password": "aaaaaaaaa",
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_USER"})

    def test_login_success(self):
        client = Client()
        user = {
            "email": "yesjiwon5304@gmail.com",
            "password": "abcde12345@",
        }
        access_token = jwt.encode({"id": self.test_user.id}, settings.SECRET_KEY , settings.ALGORITHM)

        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "MESSAGE": "SUCCESS",
            "token": access_token,
            })
    
    def test_key_error(self):
        client = Client()
        user = {
            "email": "yesjiwon5304@gmail.com",
            
        }
        response = client.post(
            "/users/login", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})
