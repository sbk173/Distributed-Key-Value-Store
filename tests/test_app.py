import unittest
from flask_testing import TestCase
from app import app


class TestFlaskApp(TestCase):
    """
    This file tests the routes for the index, put, get, delete, and list functionalities.
    """
    
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_put_route(self):
        response = self.client.post('/put', data={'key': 'test_key', 'value': 'test_value'})
        self.assertEqual(response.data.decode('utf-8'), "Key 'test_key' with value 'test_value' added successfully.")

        response = self.client.post('/delete', data={'key': 'test_key'})
        self.assertIn("Key 'test_key' deleted successfully.", response.data.decode('utf-8'))

    def test_get_route(self):
        self.client.post('/put', data={'key': 'test_key', 'value': 'test_value'})

        response = self.client.post('/get', data={'key': 'test_key'})
        self.assertIn('test_key : test_value', response.data.decode('utf-8'))

        response = self.client.post('/get', data={'key': 'nonexistent_key'})
        self.assertIn("KeyError: Key 'nonexistent_key' not found.", response.data.decode('utf-8'))

    def test_delete_route(self):
        self.client.post('/put', data={'key': 'test_key', 'value': 'test_value'})

        response = self.client.post('/delete', data={'key': 'test_key'})
        self.assertIn("Key 'test_key' deleted successfully.", response.data.decode('utf-8'))

        response = self.client.post('/delete', data={'key': 'nonexistent_key'})
        self.assertIn("KeyError: Key not found in store. Cannot Delete non-existent pairs", response.data.decode('utf-8'))

        
    def test_list_route(self):
        response = self.client.get('/list')
        self.assert_template_used('list.html')


if __name__ == '__main__':
    unittest.main(exit=False)
