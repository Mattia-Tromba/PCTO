import socket

def client_program():
    client = socket.socket()
    client.connect(('localhost', 8888))
    print(client)
    message = ""
    while message != "bye":
        print(client.recv(1024).decode())
        message = input(" -> ")
        client.send(message.encode())
        """if client.recv(1024).decode() == "utente trovato":
            client.close()
        if client.recv(1024).decode() == "utente non trovato, ricontrolla il token o la email oppure registrati ":
            client.close()"""
        #zMJY918XTCrgAPp4ckYnZwivhO
    client.close()

client_program()