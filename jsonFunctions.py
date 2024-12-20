import json

#function for receiving json data
def receive_json(conn):
    raw_size = conn.recv(4)
    if not raw_size:
        return None
    size = int.from_bytes(raw_size, 'big')

    data_buffer = b""
    while len(data_buffer) < size:
        chunk = conn.recv(size - len(data_buffer))
        if not chunk:
            break
        data_buffer += chunk

    return json.loads(data_buffer.decode())

#function for sending json data
def send_json(client, data):
    json_data = json.dumps(data).encode()
    size = len(json_data)
    client.sendall(size.to_bytes(4, 'big'))
    client.sendall(json_data)