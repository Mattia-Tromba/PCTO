import socket, threading, sqlite3, secrets, string, re
from pathlib import Path

host = "localhost"
port = 5000
server_socket = socket.socket()
server_socket.bind((host, port))
print("Starting...")
server_socket.listen(6)

def server_program(conn):
    connessione = sqlite3.connect(Path.cwd().parent / "database" / "database.db")
    c = connessione.cursor()
    c.execute("create table if not exists users (email varchar[50], token varchar[27])")
    carattere = ""

    while (carattere != 'r' and carattere != 'a') or carattere == "":
        conn.send("Vuoi registrarti o autenticarti? (r/a)".encode("utf-8"))
        carattere = conn.recv(1024).decode()

        if (carattere != 'r' and carattere != 'a') or (carattere == ""):
            conn.send("inserisci o la lettera a o la lettera r".encode("utf-8"))

    if carattere == "r":
        conn.send("invia la tua email per la registrazione: ".encode("utf-8"))
        email = conn.recv(1024).decode("utf-8")
        caratteri = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(caratteri) for _ in range(26))
        conn.send(("questo è il tuo token: %s" %token).encode("utf-8"))
        c.execute("insert into users (email, token) values (?, ?)", (email, token))
        connessione.commit()
    else:
        successo = False
        conn.send("invia l'email per il controllo: ".encode("utf-8"))
        while not successo:
            email = conn.recv(1024).decode()
            conn.send("invia il token per il controllo: ".encode("utf-8"))
            tkn = conn.recv(1024).decode()
            if c.execute("select * from users where email=? and token=?", (email, tkn)).fetchone() is not None:
                conn.send("autenticazione effettuata".encode("utf-8"))
                successo = True
            else:
                conn.send("utente non trovato, inserisci di nuovo l'email".encode("utf-8"))
    conn.send("chiusura connessione".encode("utf-8"))
    conn.close()

while True:
    con, address = server_socket.accept()
    print("Connection from: " + str(address))
    thread = (threading.Thread(target=server_program, args=(con,)))
    thread.start()