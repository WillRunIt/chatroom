import time
import socket
import pickle
import os
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 65432)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

data_directory = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(data_directory, 'userinfo.json')
# if not os.path.exists(data_path):
#     with open(data_path, 'w') as data_file:
#         username = input('Please enter your username: ')
#         json.dump({'username': username}, data_file)
# else:
#     with open(data_path, 'r') as data_file:
#         username = json.load(data_file)['username']
username = input("Please provide your username: ")


def sender():
    while True:
        message = input()
        binary_data = pickle.dumps({"message": message, "username": username})
        sock.sendall(binary_data)


def receiver():
    while True:
        binary_data = sock.recv(1024)
        if not binary_data:
            continue
        data = pickle.loads(binary_data)
        if username == data["username"]:
            continue
        print(f"{data['username']}: {data['message']}")


receiver_thread = threading.Thread(target=receiver)
receiver_thread.start()
sender_thread = threading.Thread(target=sender)
sender_thread.start()
