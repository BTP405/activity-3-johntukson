import socket
import threading
import message_handler

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

# List to keep track of connected clients
clients = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    while True:
        message = message_handler.receive_message(client_socket)
        if not message:
            break

        if message.lower() == 'quit':
            break

        message_handler.broadcast_message(clients, message)

    print(f"[DISCONNECTED] {client_address} disconnected.")
    client_socket.close()
    clients.remove(client_socket)
    message_handler.broadcast_message(clients, f"[DISCONNECTED] Client {client_address} has left the chat.")

# Function to accept incoming connections and spawn client handling threads
def accept_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Main function to start the server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print(f"[LISTENING] Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    accept_thread.start()

    accept_thread.join()
    server_socket.close()

if __name__ == "__main__":
    main()
