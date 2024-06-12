import pickle
import threading
import socketserver


HOST = "0.0.0.0"
PORT = 443

messages_queue = []
clients = []
message_queue_lock = threading.Lock()


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global messages_queue, clients
        with message_queue_lock:
            clients.append(self.request)
        try:
            while True:
                data = self.request.recv(1024)
                if not data:
                    break
                data = pickle.loads(data)
                with message_queue_lock:
                    messages_queue.append(data)
                with message_queue_lock:
                    for client in clients:
                        try:
                            client.sendall(pickle.dumps(data))
                        except Exception as e:
                            print(f"Error sending message to client: {e}")

        except pickle.UnpicklingError:
            print("Keepalive received")
        finally:
            with message_queue_lock:
                clients.remove(self.request)


if __name__ == "__main__":
    print("Server started")
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
