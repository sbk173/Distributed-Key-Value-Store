import etcd3
import random

class Client:
    def __init__(self, available_endpoints):
        """
        Initializes the Client object.

        Args:
            available_endpoints (list): A list of endpoint strings in the format "host:port" or "protocol://host:port".
        """
        
        self.available_endpoints = available_endpoints
        self.check_available_endpoints()
        if not self.available_endpoints:
            raise Exception("No available endpoints found")
        random_endpoint = random.choice(self.available_endpoints)
        self.host, self.port = random_endpoint.split("//")[-1].split(":")
        self.client = etcd3.client(host=self.host, port=int(self.port))
        print(f"Connected to host: {self.host}, port: {self.port}")

    def check_available_endpoints(self):
        """
        Checks and updates the list of available endpoints by performing a read operation.
        """
        available_endpoints = []
        for endpoint in self.available_endpoints:
            host_port = endpoint.split("//")[-1]
            host, port = host_port.split(":")
            try:
                client = etcd3.client(host=host, port=int(port))
                client.get('/')
                available_endpoints.append(endpoint)
            except etcd3.exceptions.ConnectionFailedError:
                print(f"Failed to connect to {endpoint}")
            except Exception as e:
                print(f"Error checking endpoint {endpoint}: {e}")

        self.available_endpoints = available_endpoints
        print(f"Available endpoints: {self.available_endpoints}")

    def is_connection_active(self):
        """
        Checks if the current connection to the etcd server is active.

        Returns:
            bool: True if the connection is active, False otherwise.
        """
        try:
            self.client.get('/')
            return True
        except etcd3.exceptions.ConnectionFailedError:
            return False
        except Exception as e:
            print(f"Error checking connection: {e}")
            return False
        
    def reconnect(self):
        """
        Connects to an available endpoint if the current endpoint is down.
        """
        self.check_available_endpoints()
        if not self.available_endpoints:
            raise Exception("No available endpoints found")
        random_endpoint = random.choice(self.available_endpoints)
        self.host, self.port = random_endpoint.split("//")[-1].split(":")
        self.client = etcd3.client(host=self.host, port=int(self.port))
        print(f"Connected to host: {self.host}, port: {self.port}")

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
