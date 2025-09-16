import socket, threading
from concurrent.futures import thread

host = "localhost"
port = 5000
server_socket = socket.socket()
server_socket.bind((host, port))
print("Starting...")
server_socket.listen(6)

def server_program(conn, address):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Server received: ", data, "from port: ", address)
    conn.close()

while True:
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    thread = (threading.Thread(target=server_program, args=(conn, address,)))
    thread.start()