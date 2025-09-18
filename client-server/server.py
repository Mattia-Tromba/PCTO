import socket, threading, sqlite3, secrets, string

host = "localhost"
port = 5000
server_socket = socket.socket()
server_socket.bind((host, port))
print("Starting...")
server_socket.listen(6)

def server_program(conn, address):
    connessione = sqlite3.connect(r'C:\Users\NADIA\workspace\CPTO\database\database.db')
    c = connessione.cursor()
    c.execute("create table if not exists users (email varchar[50], token varchar[27])")
    carattere = ""

    while carattere != 'r' and carattere != 'a':
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Server received: ", data, "from port: ", address)
        conn.send("Vuoi registrarti o autenticarti? (r/a)".encode("utf-8"))
        carattere = conn.recv(1024).decode()

        if carattere != 'r' and carattere != 'a':
            conn.send("inserisci o la lettera a o la lettera r".encode("utf-8"))

    if carattere == "r":
        conn.send("invia la tua email per la registrazione: ".encode("utf-8"))
        email = conn.recv(1024).decode()
        caratteri = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(caratteri) for i in range(26))
        conn.send(("questo è il tuo token: %s" %token).encode("utf-8"))
        c.execute("insert into users (email, token) values (?, ?)", (email, token))
        connessione.commit()
    else:
        successo = True

        while successo:
                conn.send("invia la tua email per il controllo: ".encode("utf-8"))
                email = conn.recv(1024).decode()
                if c.execute("select email from users where email = ?", (email,)).fetchone():
                    conn.send("invia il token: ".encode("utf-8"))
                    token = conn.recv(1024).decode()
                    if c.execute("select token from users where token = ?", (token,)).fetchone():
                        conn.send("autenticazione effettuata".encode("utf-8"))
                        successo = False
                    else:
                        conn.send("il token è errato".encode("utf-8"))
                else:
                    conn.send("l'email che hai inserito è sbagliata \n".encode("utf-8"))
    conn.close()

while True:
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    thread = (threading.Thread(target=server_program, args=(conn, address,)))
    thread.start()