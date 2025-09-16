import socket

def client_program():
    client = socket.socket()
    client.connect(('localhost', 5000))
    print(client)
    message = ""
    while message != "bye":
        message = input(" -> ")
        client.send(message.encode())
        print(client.recv(1024).decode())
    client.close()

client_program()