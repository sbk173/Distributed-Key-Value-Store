import etcd3

class Client:
    client = None
    def __init__(self, host='localhost', port=2379):
        self.client = etcd3.client(host=host, port=port)

    def get_all_keys(self):
        keys = self.client.get_all()
        keys = list(keys)
        key_set = []
        for key in keys:
            value, metadata = key
            alpha = (metadata.key.decode('utf-8'), value.decode('utf-8'))
            key_set.append(alpha)
            print(alpha[0], ':', alpha[1])
        return key_set
        

    def get_value(self, key):
        try:
            value, metadata = self.client.get(key)
            return key + " : " + value.decode('utf-8')
        except etcd3.exceptions.Etcd3Exception:
            return "KeyError: Key '{}' not found.".format(key)
        except Exception as e:
            return "Error getting value for key '{}': {}".format(key, e)

    def put_key(self, key, value):
        self.client.put(key, value)

    def delete_key(self, key):
        key_set = self.get_all_keys()
        keys = []
        for i in key_set:
            keys.append(i[0])
        if key not in keys:
            return "KeyError: Key not found in store. Cannot Delete non-existent pairs"
        try:
            self.client.delete(key)
            return "Key '{}' deleted successfully.".format(key)
        except etcd3.exceptions.Etcd3Exception:
            return "KeyError: Key '{}' not found.".format(key)
        except Exception as e:
            return "Error deleting key '{}': {}".format(key, e)


if __name__ == "__main__":
    client = Client()
    client.put_key('a','200')
    client.get_all_keys()
    client.get_value('a')
    client.put_key('beta', '100')
    client.get_all_keys()
    client.delete_key('beta')
    client.get_all_keys()