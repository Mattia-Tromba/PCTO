import socket, re

def client_program():
    client = socket.socket()
    client.connect(('localhost', 5000))
    print(client)
    message = ""
    while message != "r" and message != "a":
        print(client.recv(1024).decode())
        message = input(" -> ")
        while message == "":
            message = input(" -> ")
        client.send(message.encode())
        if message != "r" and message != "a":
            print(client.recv(1024).decode())
    if message == "r":
        print(client.recv(1024).decode())
        messaggio = input(" -> ")
        print(messaggio)
        while message == "" or not re.match(r"^\w+@\w+\.\w+$", message):
            print("email errata")
            message = input(" -> ")
        client.send(messaggio.encode("utf-8"))
        print(client.recv(1024).decode())
    else:
        successo = False
        print(client.recv(1024).decode())
        while not successo:
            message = input(" -> ")
            while message == "":
                message = input(" -> ")
            client.send(message.encode())
            print(client.recv(1024).decode())
            messaggio = input(" -> ")
            while message == "":
                message = input(" -> ")
            client.send(messaggio.encode())
            message = client.recv(1024).decode()
            print(message)
            if message == "autenticazione effettuata":
                successo = True

    client.close()

client_program()