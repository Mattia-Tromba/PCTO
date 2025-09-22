import socket, threading, sqlite3
import secrets, string
import re


def autenticazione(con, cur):
    entrata=""
    x=0
    y=0
    while (entrata != "r" and entrata != "a") or entrata == "":
        conn.send("vuoi registrarti (scrivi r) o vuoi autenticarti (scrivi a)?".encode("utf-8"))
        entrata = conn.recv(1024).decode()
    if entrata == "r":
        while x != 1:
            conn.send("inserisci email".encode("utf-8"))
            email = conn.recv(1024).decode("utf-8")
            if re.match(r'^\w+@\w+\.\w', email):
                token = genera_token()
                cur.execute("INSERT INTO users (nome, token, dataIscrizione) VALUES (?, ?, CURRENT_TIMESTAMP)",
                            (email, token))
                con.commit()
                conn.send(("Registrazione completata. Token: %s (bye per uscire)\nOra scrivendo un messaggio puoi iniziare la conversazione" % token).encode())
                x = 1
            else:
                conn.send("email non valida, riprova. ".encode())

    elif entrata == "a":
        while x!=1:
            conn.send("inserisci email".encode("utf-8"))
            email = conn.recv(1024).decode("utf-8")
            conn.send("inserisci token".encode("utf-8"))
            token = conn.recv(1024).decode()
            cur.execute("SELECT * FROM users WHERE nome = ? AND token = ?", (email, token))
            if y >= 3:
                conn.send("hai superato i tentativi possibili, registrati".encode("utf-8"))
                conn.close()
            if cur.fetchone() is None:
                conn.send("utente non trovato, ricontrolla il token o la email oppure registrati\n".encode("utf-8"))
                y+=1
            else:
                conn.send("utente trovato\nOra scrivendo un messaggio puoi iniziare la conversazione".encode())
                x=1

def genera_token():
    caratteri = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caratteri) for _ in range(26))

host = "localhost"
port = 8999
server_socket = socket.socket()
server_socket.bind((host, port))
print("Starting...")
server_socket.listen(6)


def server_program(conn, address):
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS users
                (
                    nome varchar primary key not null,
                    token varchar unique not null,
                    dataIscrizione varchar not null
                )
                """)

    con.commit()

    autenticazione(con, cur)
    entrata=""
    while entrata !="bye":
        entrata = (conn.recv(1024).decode())
        print("client dice:", entrata)
        invio=input(" -> ")
        while invio =="":
            invio = input(" -> ")
        conn.send(invio.encode("utf-8"))
    conn.close()

while True:
    conn, address = server_socket.accept()
    print("Connection from:", address)
    thread = threading.Thread(target=server_program, args=(conn, address))
    thread.start()

