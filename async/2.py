# echo_server(('', 25000))
# nc localhost 25000

from threading import Thread

def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        Thread(target=echo_handler, args=(client, addr)).start()

def echo_handler(client, addr):
    print('Connection from', addr)
    with client:
        while True:
            data = client.recv(100000)
            if not data:
                break
            client.sendall(data)
    print('Connection closed')
