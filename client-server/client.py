import socket

def client_program():
    client = socket.socket()
    client.connect(('localhost', 5000))
    print(client)
    message = ""
    while message != "r" or message != "a":
        message = input(" -> ")
        client.send(message.encode())
        print(client.recv(1024).decode())
    if message == "r":
        print(client.recv(1024).decode())
        client.send(input(" -> ").encode())
        print(client.recv(1024).decode())
    else:
        while True:
            print(client.recv(1024).decode())
            client.send(input(" -> ").encode())
            if client.recv(1024).decode() == "invia il token: ":
                client.send(input(" -> ").encode())
                print(client.recv(1024).decode())
                break
    client.close()

client_program()