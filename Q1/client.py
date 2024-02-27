import socket
import pickle

def send_file(file_path, server_address, server_port):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_pickle = pickle.dumps(file_data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, server_port))
            client_socket.sendall(file_pickle)
            print("File sent successfully!")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    server_address = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port: "))
    send_file(file_path, server_address, server_port)
