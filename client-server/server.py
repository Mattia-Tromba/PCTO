import socket, threading, sqlite3, secrets, string, re
from pathlib import Path

host = "localhost"
port = 5001
server_socket = socket.socket()
server_socket.bind((host, port))
print("Starting...")
server_socket.listen(6)


def server_program(conn):
    dbpath = sqlite3.connect(Path.cwd().parent / "database" / "data.db")
    c = dbpath.cursor()
    c.execute("""create table if not exists users
              (
               email varchar[50] unique not null,
               token varchar[27] unique not null
               )
              """)
    parola = ""
    conn.send("Registrazione (r), Autenticazione (a), Abbandono (quit)".encode("utf-8"))
    while parola != "quit":
        parola = conn.recv(1024).decode()
        while parola != "r" and parola != "a" and parola != "quit":
            conn.send("Comando invalido\nRegistrazione (r), Autenticazione (a), Abbandono (quit)".encode("utf-8"))
            parola = conn.recv(1024).decode()
        if parola == "r":
            if registrazione(conn, c, dbpath) == 2:
                conn.close()
                return
            if autenticazione(conn, c) == 3:
                conn.close()
                return
            comunicazione(conn)
            conn.close()
            return

        elif parola == "a":
            conn.send("invia l'email".encode("utf-8"))
            if autenticazione(conn, c) == 3:
                conn.close()
                return
            comunicazione(conn)
            conn.close()
            return

    conn.send("chiusura connessione".encode("utf-8"))
    conn.close()


def registrazione(conn, c, dbpath):
    uscita = 0
    while True:
        conn.send("invia la tua email per la registrazione: ".encode("utf-8"))
        email = conn.recv(1024).decode("utf-8")
        while not re.match(r'^\w+@\w+\.\w', email):
            if uscita == 2:
                conn.send("troppi tentativi, chiusura connessione".encode("utf-8"))
                return uscita
            conn.send("email non valida, inseriscine un'altra: ".encode("utf-8"))
            uscita += 1
            email = conn.recv(1024).decode("utf-8")
        try:
            caratteri = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(caratteri) for _ in range(26))
            c.execute("insert into users (email, token) values (?, ?)", (email, token))
            dbpath.commit()
            conn.send(
                ("questo è il tuo token: %s\naccedi al tuo account tramite autenticazione: invia l'email" % token).encode(
                    "utf-8"))
            return
        except:
            conn.send("email già registrata, inserirne un'altra\nRegistrazione (r), Autenticazione (a), Abbandono (quit)".encode("utf-8"))


def autenticazione(conn, c):
    uscita = 0
    while True:
        email = conn.recv(1024).decode()
        conn.send("invia il token per il controllo: ".encode("utf-8"))
        tkn = conn.recv(1024).decode()
        if c.execute("select * from users where email=? and token=?", (email, tkn)).fetchone() is not None:
            conn.send("autenticazione effettuata\n\ninizio comunicazione: invia un messaggio".encode("utf-8"))
            return uscita
        elif uscita < 2:
            conn.send("utente non trovato, inserisci di nuovo l'email".encode("utf-8"))
            uscita += 1
        else:
            conn.send("troppi tentativi, chiusura connessione".encode("utf-8"))
            return uscita


def comunicazione(conn):
    while True:
        messaggio = conn.recv(1024).decode()
        print(messaggio)
        if messaggio == "quit":
            return
        messaggio = input("-> ")
        while messaggio == "":
            messaggio = input("-> ")
        conn.send(messaggio.encode("utf-8"))


while True:
    con, address = server_socket.accept()
    print("Connection from: " + str(address))
    thread = (threading.Thread(target=server_program, args=(con,)))
    thread.start()