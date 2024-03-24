import etcd3

class Client:
    client = None
    def __init__(self,host='localhost',port=2379):
        self.client = etcd3.client(host=host,port=port)

    def get_all_keys(self):
        keys = self.client.get_all()
        keys = list(keys)
        for key in keys:
            value,metadata = key
            print(metadata.key.decode('utf-8'),":",value.decode('utf-8'))

    def get_value(self,key):
        try:
            value,metadata = self.client.get(key)
        except:
            print("KeyError: Key not found")
        else:
            print(key,":",value.decode('utf-8'))

    def put_key(self,key,value):
        self.client.put(key,value)


if __name__ == "__main__":
    client = Client()
    client.get_all_keys()
    client.get_value('a')

