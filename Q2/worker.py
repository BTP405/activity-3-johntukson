import socket
import pickle
import threading

class WorkerNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tasks = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Worker node started on", self.host, "port", self.port)

        while True:
            client_socket, addr = self.server_socket.accept()
            print("Connection established from", addr)

            task_data = client_socket.recv(4096)
            if task_data:
                task = pickle.loads(task_data)
                task_id = task['id']
                task_func = task['func']
                task_args = task['args']

                # Execute task in a separate thread
                task_thread = threading.Thread(target=self.execute_task, args=(client_socket, task_id, task_func, task_args))
                task_thread.start()
            else:
                client_socket.close()

    def execute_task(self, client_socket, task_id, task_func, task_args):
        try:
            result = task_func(*task_args)
            response = {'id': task_id, 'result': result}
            client_socket.sendall(pickle.dumps(response))
        except Exception as e:
            print("Error executing task:", e)
        finally:
            client_socket.close()

def main():
    worker = WorkerNode('localhost', 12345)
    worker.start()

if __name__ == "__main__":
    main()
