import json
import socket
import pickle
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 65432)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

data_directory = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(data_directory, 'userinfo.json')
if not os.path.exists(data_path):
    with open(data_path, 'w') as data_file:
        username = input('Please enter your username: ')
        json.dump({'username': username}, data_file)
else:
    with open(data_path, 'r') as data_file:
        username = json.load(data_file)['username']

message = input(">>>")
binary_msg = pickle.dumps(message)

try:
    print('sending {!r}'.format(*server_address))
    sock.sendall(binary_msg)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print('received {!r}'.format(pickle.loads(data)))

finally:
    print('closing socket')
    sock.close()
