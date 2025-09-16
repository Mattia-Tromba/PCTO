import socket

def client_program():
    client = socket.socket()
    client.connect(('localhost', 5000))
    print(client)
    message = ""
    while message != "bye":
        message = input(" -> ")
        client.send(message.encode())
    client.close()

client_program()