import socket, re

def client_program():
    client = socket.socket()
    client.connect(('localhost', 5001))
    print(client)
    while True:
        message = client.recv(1024).decode("utf-8")
        print(message)
        message = input("-> ")
        while message == "":
            message = input("-> ")
        client.send(message.encode("utf-8"))
        if message == "quit":
            break
    client.close()

client_program()