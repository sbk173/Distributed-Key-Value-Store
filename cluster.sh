SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

NODE1_CONFIG="$SCRIPT_DIR/config/etcd.conf.yml"
NODE2_CONFIG="$SCRIPT_DIR/config/etcd2.conf.yml"
NODE3_CONFIG="$SCRIPT_DIR/config/etcd3.conf.yml"

start_node() {
    osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR'; etcd --config-file=$1\""
}

start_node "$NODE1_CONFIG"
start_node "$NODE2_CONFIG"
start_node "$NODE3_CONFIG"
