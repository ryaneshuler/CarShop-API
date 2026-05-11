from app import create_app
from app.models import db, Mechanic
from app.utils.util import encode_token
import unittest


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="test_mechanic", email="mech@email.com", phone="555-1234", salary=50000.0)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        payload = {
            "name": "John Doe",
            "email": "jdoe@email.com",
            "phone": "555-5678",
            "salary": 60000.0
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_create_mechanic_missing_fields(self):
        payload = {
            "name": "John Doe"
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    def test_get_all_mechanics_empty(self):
        with self.app.app_context():
            Mechanic.query.delete()
            db.session.commit()
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_most_worked_mechanics(self):
        response = self.client.get('/mechanics/most-worked')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_mechanic(self):
        payload = {"name": "Updated Name"}
        response = self.client.put('/mechanics/1', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Name')

    def test_update_mechanic_not_found(self):
        payload = {"name": "Updated Name"}
        response = self.client.put('/mechanics/999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
