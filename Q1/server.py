import socket
import pickle

def receive_file(save_directory, server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('127.0.0.1', server_port))
            server_socket.listen(1)
            print("Server is listening for incoming connections...")

            conn, addr = server_socket.accept()
            print(f"Connection established with {addr}")

            file_pickle = conn.recv(4096)
            file_data = pickle.loads(file_pickle)

            with open(save_directory, 'wb') as file:
                file.write(file_data)

            print("File received and saved successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    save_directory = input("Enter the directory to save the received file: ")
    server_port = int(input("Enter the server port: "))
    receive_file(save_directory, server_port)
