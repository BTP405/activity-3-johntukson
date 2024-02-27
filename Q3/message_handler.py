import pickle

# Function to serialize message
def serialize_message(message):
    return pickle.dumps(message)

# Function to deserialize message
def deserialize_message(data):
    return pickle.loads(data)

# Function to receive message
def receive_message(socket):
    try:
        data = socket.recv(1024)
        if not data:
            return None
        return deserialize_message(data)
    except Exception as e:
        print(f"[ERROR] Error receiving message: {e}")
        return None

# Function to broadcast message
def broadcast_message(clients, message):
    for client_socket in clients:
        try:
            client_socket.send(serialize_message(message))
        except:
            clients.remove(client_socket)
