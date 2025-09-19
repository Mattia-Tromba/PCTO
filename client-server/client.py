import socket

def client_program():
    client = socket.socket()
    client.connect(('localhost', 5000))
    print(client)
    message = ""
    while message != "r" and message != "a":
        print(client.recv(1024).decode())
        message = input(" -> ")
        client.send(message.encode())
    if message == "r":
        print(client.recv(1024).decode())
        messaggio = input(" -> ")
        client.send(messaggio.encode())
        print(client.recv(1024).decode())
    else:
        successo = False
        print(client.recv(1024).decode())
        while not successo:
            messaggio = input(" -> ")
            client.send(messaggio.encode())
            print(client.recv(1024).decode())
            messaggio = input(" -> ")
            client.send(messaggio.encode())
            messric = client.recv(1024).decode()
            print(messric)
            if messric == "autenticazione effettuata":
                successo = True

    client.close()

client_program()