from app import create_app
from app.models import db, User
from app.utils.util import encode_token
import unittest


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = User(username="test_user", email="test@email.com", password="test")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_customer(self):
        payload = {
            "username": "new_user",
            "email": "new@email.com",
            "password": "password123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], 'new@email.com')

    def test_create_customer_missing_fields(self):
        payload = {
            "username": "no_email_user"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('auth_token', response.json)

    def test_invalid_login(self):
        credentials = {
            "email": "bad@email.com",
            "password": "wrong"
        }
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)

    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    def test_get_my_tickets(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_my_tickets_no_token(self):
        response = self.client.get('/customers/my-tickets')
        self.assertEqual(response.status_code, 401)

    def test_update_customer(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        payload = {"username": "updated_user"}
        response = self.client.put('/customers/1', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'updated_user')

    def test_update_customer_not_found(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        payload = {"username": "updated_user"}
        response = self.client.put('/customers/999', json=payload, headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_customer(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
