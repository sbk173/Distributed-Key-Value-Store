export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
python -m unittest discover -s tests -p 'test_client.py'
python -m unittest discover -s tests -p 'test_app.py'
