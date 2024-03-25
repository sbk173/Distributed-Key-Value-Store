import unittest
from client import Client

class TestClient(unittest.TestCase):

    """
    This file contains unit tests for the core functionalities of:
        putting keys, getting values, deleting keys, and retrieving all keys.
    """

    def setUp(self):
        self.client = Client()

    def test_put_key(self):
        self.client.put_key('test_key', 'test_value')
        value = self.client.get_value('test_key')
        self.assertEqual(value, 'test_key : test_value')

    def test_get_value(self):
        self.client.put_key('test_key', 'test_value')
        value = self.client.get_value('test_key')
        self.assertEqual(value, 'test_key : test_value')

    def test_delete_key(self):
        self.client.put_key('test_key', 'test_value')
        self.client.delete_key('test_key')
        value = self.client.get_value('test_key')
        self.assertEqual(value, "Error getting value for key 'test_key': 'NoneType' object has no attribute 'decode'")

    def test_get_all_keys(self):
        self.client.put_key('key1', 'test_value1')
        self.client.put_key('key2', 'test_value2')
        self.client.put_key('key3', 'test_value3')
        keys = self.client.get_all_keys()

        expected_keys = [('key1', 'test_value1'), ('key2', 'test_value2'), ('key3', 'test_value3')]
        self.assertCountEqual(keys, expected_keys)
        self.client.delete_key('key1')
        self.client.delete_key('key2')
        self.client.delete_key('key3')


if __name__ == '__main__':
    unittest.main()
