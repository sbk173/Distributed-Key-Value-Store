import etcd3

class Client:
    """
    A class for interacting with an etcd server.
    
    Attributes:
        client (etcd3.Client): An instance of etcd3 client.
    """
    client = None

    def __init__(self, host='localhost', port=2379):
        """
        Initializes the Client object.
        
        Args:
            host (str): The host address of the etcd server. Default is 'localhost'.
            port (int): The port number of the etcd server. Default is 2379.
        """

        self.client = etcd3.client(host=host, port=port)

    def get_all_keys(self):
        """
        Retrieves all keys from the etcd server.
        
        Returns:
            list: A list of tuples containing key-value pairs.
        """

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
        """
        Retrieves the value corresponding to a given key from the etcd server.
        
        Args:
            key (str): The key whose value is to be retrieved.
            
        Returns:
            str: The value associated with the given key.
        """
        try:
            value, metadata = self.client.get(key)
            if value is None:
                raise etcd3.exceptions.Etcd3Exception
            return key + " : " + value.decode('utf-8')
        except etcd3.exceptions.Etcd3Exception:
            return "KeyError: Key '{}' not found.".format(key)
        except Exception as e:
            return "Error getting value for key '{}': {}".format(key, e)

    def put_key(self, key, value):
        """
        Stores a key-value pair in the etcd server.
        
        Args:
            key (str): The key to be stored.
            value (str): The value associated with the key.

        Returns:
            None
        """

        self.client.put(key, value)

    def delete_key(self, key):
        """
        Deletes a key-value pair from the etcd server.
        
        Args:
            key (str): The key to be deleted.
            
        Returns:
            str: Confirmation message indicating whether the deletion was successful.
        """
        
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