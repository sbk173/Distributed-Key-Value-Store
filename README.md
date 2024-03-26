## Pre-Requirements
- OS: Linux/MacOS
- etcd (version: 3.5.12)
- Python 3.11+
- etcd3 module (pip install etcd3)

## Execution
- Make appropriate changes to etcd.conf.yml
- Launch etcd in one terminal (etcd --config-file <"path to etcd.conf.yml">)
- Open another terminal window (./run.sh)
- Open a browser window and use the application on <http://127.0.0.1:5000>
- App is currently in debugging mode (to be changed later)
- To run the tests execute (./test.sh) in a terminal window
