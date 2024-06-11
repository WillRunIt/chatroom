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
username = input("Please provide your username")

def sender():
    while True:
        message = input(">>>")
        binary_msg = pickle.dumps(message)
        sock.sendall(binary_msg)

def receiver():
    while True:
        data = sock.recv(1024)
        if not data:
            continue
        else:
            print(pickle.loads(data))

receiver_thread = threading.Thread(target=receiver)
receiver_thread.start()
sender_thread = threading.Thread(target=sender)
sender_thread.start()
