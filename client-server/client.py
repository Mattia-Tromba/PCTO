import socket

def client_program():
    client = socket.socket()
    client.connect(('localhost', 8999))
    print(client)
    message = ""
    while message != "bye":
        entrata=(client.recv(1024).decode())
        print("il server dice: " + entrata)
        message = input(" -> ")
        while message =="":
            message = input(" -> ")
        client.send(message.encode("utf-8"))
    client.close()

client_program()