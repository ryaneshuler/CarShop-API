from app import create_app
from app.models import db, ServiceTicket, Mechanic, Inventory, User
from app.utils.util import encode_token
import unittest


class TestServiceTicket(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            customer = User(username="test_user", email="test@email.com", password="test")
            mechanic = Mechanic(name="test_mechanic", email="mech@email.com", phone="555-1234", salary=50000.0)
            part = Inventory(name="test_part", price=10.0)
            ticket = ServiceTicket(
                vin="1HGCM82633A123456",
                service_date="2024-01-01",
                service_desc="Oil change",
                customer_name="Test Customer"
            )
            db.session.add_all([customer, mechanic, part, ticket])
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_service_ticket(self):
        payload = {
            "vin": "2HGCM82633A654321",
            "service_date": "2024-02-01",
            "service_desc": "Tire rotation",
            "customer_name": "Jane Doe"
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_desc'], 'Tire rotation')

    def test_create_service_ticket_missing_fields(self):
        payload = {
            "service_desc": "Oil change"
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_all_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    def test_get_all_service_tickets_empty(self):
        with self.app.app_context():
            ServiceTicket.query.delete()
            db.session.commit()
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_update_service_ticket(self):
        payload = {"service_desc": "Updated description"}
        response = self.client.put('/service-tickets/1', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['service_desc'], 'Updated description')

    def test_update_service_ticket_not_found(self):
        payload = {"service_desc": "Updated description"}
        response = self.client.put('/service-tickets/999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_assign_mechanic(self):
        response = self.client.put('/service-tickets/1/assign-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_assign_mechanic_not_found(self):
        response = self.client.put('/service-tickets/1/assign-mechanic/999')
        self.assertEqual(response.status_code, 404)

    def test_remove_mechanic(self):
        self.client.put('/service-tickets/1/assign-mechanic/1')
        response = self.client.put('/service-tickets/1/remove-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_edit_mechanics(self):
        payload = {"add_ids": [1], "remove_ids": []}
        response = self.client.put('/service-tickets/1/edit', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_assign_customer(self):
        response = self.client.put('/service-tickets/1/assign-customer/1')
        self.assertEqual(response.status_code, 200)

    def test_assign_customer_not_found(self):
        response = self.client.put('/service-tickets/1/assign-customer/999')
        self.assertEqual(response.status_code, 404)

    def test_remove_customer(self):
        response = self.client.put('/service-tickets/1/remove-customer')
        self.assertEqual(response.status_code, 200)

    def test_add_part(self):
        response = self.client.put('/service-tickets/1/add-part/1')
        self.assertEqual(response.status_code, 200)

    def test_add_part_not_found(self):
        response = self.client.put('/service-tickets/1/add-part/999')
        self.assertEqual(response.status_code, 404)

    def test_remove_part(self):
        self.client.put('/service-tickets/1/add-part/1')
        response = self.client.put('/service-tickets/1/remove-part/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
