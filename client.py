import etcd3

class Client:
    client = None
    def __init__(self, host='localhost', port=2379):
        self.client = etcd3.client(host=host, port=port)

    def get_all_keys(self):
        keys = self.client.get_all()
        keys = list(keys)
        for key in keys:
            value, metadata = key
            print(metadata.key.decode('utf-8'), ":", value.decode('utf-8'))

    def get_value(self, key):
        try:
            value, metadata = self.client.get(key)
            print(key, ":", value.decode('utf-8'))
        except etcd3.exceptions.Etcd3Exception:
            print("KeyError: Key '{}' not found.".format(key))
        except Exception as e:
            print("Error getting value for key '{}': {}".format(key, e))

    def put_key(self, key, value):
        self.client.put(key, value)

    def delete_key(self, key):
        try:
            self.client.delete(key)
            print("Key '{}' deleted successfully.".format(key))
        except etcd3.exceptions.Etcd3Exception:
            print("KeyError: Key '{}' not found.".format(key))
        except Exception as e:
            print("Error deleting key '{}': {}".format(key, e))


if __name__ == "__main__":
    client = Client()
    client.get_all_keys()
    client.get_value('a')
    client.put_key('beta', '100')
    client.get_all_keys()
    client.delete_key('beta')
    client.get_all_keys()