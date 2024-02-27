import socket
import pickle
import threading
import time

class TaskQueueClient:
    def __init__(self):
        self.server_host = 'localhost'
        self.server_port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_task(self, task_func, *args):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            task_id = str(time.time())  # Unique ID for each task
            task_data = {'id': task_id, 'func': task_func, 'args': args}
            self.client_socket.sendall(pickle.dumps(task_data))

            response = self.client_socket.recv(4096)
            if response:
                result = pickle.loads(response)
                print("Task ID:", result['id'])
                print("Result:", result['result'])
        except Exception as e:
            print("Error sending task:", e)
        finally:
            self.client_socket.close()

def main():
    client = TaskQueueClient()
    while True:
        task_func = input("Enter the task function name: ")
        args = input("Enter the arguments (comma-separated): ").split(',')
        client.send_task(task_func, *args)

if __name__ == "__main__":
    main()
