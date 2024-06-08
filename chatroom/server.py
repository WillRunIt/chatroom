import pickle
import threading
import socketserver

HOST = "localhost"
PORT = 65432

messages_queue = []
message_queue_lock = threading.Lock()
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global messages_queue
        try:
            data = self.request.recv(1024)
            data = pickle.loads(data)
            self.request.sendall(pickle.dumps(data))
        except pickle.UnpicklingError:
            print("Keepalive received")


if __name__ == "__main__":
    print("Server started")
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
