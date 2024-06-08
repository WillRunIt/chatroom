import socket
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 65432)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
message = input(">>>")
binary_msg= pickle.dumps(message)
try:
    print('sending {!r}'.format(*server_address))
    sock.sendall(binary_msg)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(pickle.loads(data)))

finally:
    print('closing socket')
    sock.close()