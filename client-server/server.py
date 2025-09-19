import socket, threading, sqlite3
import secrets, string

def genera_token():
    caratteri = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caratteri) for _ in range(26))

host = "localhost"
port = 8888
server_socket = socket.socket()
server_socket.bind((host, port))
print("Starting...")
server_socket.listen(6)


def server_program(conn, address):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    entrata = ""
    while entrata != "r" and entrata != "a":
        conn.send("vuoi registrarti (scrivi r) o vuoi autenticarti (scrivi a)?".encode("utf-8"))
        entrata = conn.recv(1024).decode()
    if entrata == "r":
        conn.send("inserisci email".encode("utf-8"))
        email = conn.recv(1024).decode()
        token = genera_token()
        cur.execute("INSERT INTO users (nome, token, dataIscrizione) VALUES (?, ?, CURRENT_TIMESTAMP)", (email, token))
        con.commit()
        conn.send(("Registrazione completata. Token: %s (bye per uscire)" %token).encode())
        conn.close()
    if entrata == "a":
        conn.send("inserisci email".encode("utf-8"))
        email = conn.recv(1024).decode()
        conn.send("inserisci token".encode("utf-8"))
        token = conn.recv(1024).decode()
        cur.execute("SELECT * FROM users WHERE nome = ? AND token = ?", (email, token))
        if cur.fetchone() is None:
            conn.send("utente non trovato, ricontrolla il token o la email oppure registrati".encode("utf-8"))
            conn.close()
        else:
            conn.send("utente trovato".encode("utf-8"))
            conn.close()
    conn.close()

while True:
    conn, address = server_socket.accept()
    print("Connection from:", address)
    thread = threading.Thread(target=server_program, args=(conn, address))
    thread.start()