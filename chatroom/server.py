import socket
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 65432)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)

while True:
    print('waiting for connection')
    connection, client_address = sock.accept()
    try:
        print('connection from ', client_address)
        while True:
            data = connection.recv(1024)
            data = pickle.loads(data)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(pickle.dumps(data))
            else:
                print('no data from', client_address)
                break
    finally:
        connection.close()
