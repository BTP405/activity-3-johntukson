import socket
import threading
import message_handler

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        message = message_handler.receive_message(client_socket)
        if not message:
            break
        print(message)

# Main function to run the client
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Enter message ('quit' to exit): ")
        if message.lower() == 'quit':
            client_socket.send(message_handler.serialize_message(message))
            break
        client_socket.send(message_handler.serialize_message(message))

    client_socket.close()

if __name__ == "__main__":
    main()
