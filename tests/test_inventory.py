from app import create_app
from app.models import db, Inventory
from app.utils.util import encode_token
import unittest


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.item = Inventory(name="test_part", price=10.0)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.item)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_inventory_item(self):
        payload = {
            "name": "Brake Pad",
            "price": 25.0
        }
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Brake Pad')

    def test_create_inventory_item_missing_fields(self):
        payload = {
            "name": "Brake Pad"
        }
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    def test_get_all_inventory_empty(self):
        with self.app.app_context():
            Inventory.query.delete()
            db.session.commit()
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_inventory_item(self):
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_part')

    def test_get_inventory_item_not_found(self):
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_item(self):
        payload = {"price": 15.0}
        response = self.client.put('/inventory/1', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['price'], 15.0)

    def test_update_inventory_item_not_found(self):
        payload = {"price": 15.0}
        response = self.client.put('/inventory/999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory_item(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
