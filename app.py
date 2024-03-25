from flask import Flask, render_template, request
from client import Client

app = Flask(__name__)
client = Client()  # Instantiate the client

# Route to display available options
@app.route('/')
def index():
    return render_template('index.html')

# Route for put operation
@app.route('/put', methods=['POST'])
def put():
    key = request.form['key']
    value = request.form['value']
    client.put_key(key, value)
    return "Key '{}' with value '{}' added successfully.".format(key, value)

# Route for get operation
@app.route('/get', methods=['POST'])
def get():
    key = request.form['key']
    try:
        value = client.get_value(key)
        return value
    except Exception as e:
        return e

# Route for delete operation
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    try:
        message = client.delete_key(key)
        return message
    except Exception as e:
        return e

# Route for list operation
@app.route('/list')
def list_keys():
    keys = client.get_all_keys()
    return render_template('list.html', keys=keys)

if __name__ == '__main__':
    app.run(debug=True)