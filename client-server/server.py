import secrets
import socket
import threading
import re
import os

import sqlite3

from sqlite3 import IntegrityError


from consts import HOST, PORT, MAX_RETRIES, LEN_TOKEN, ALPHABET


def get_email(conn) -> str:
    conn.send("Please provide your email".encode("utf-8"))
    e_mail = conn.recv(1024).decode("utf-8")

    # Check if the provided email has a valid format
    while not re.match(r"\w+@\w+\.\w+", e_mail):
        conn.send("Email not with a correct format, retry".encode("utf-8"))
        e_mail = conn.recv(1024).decode("utf-8")

    return e_mail


def get_token(conn) -> str:
    conn.send("Please provide your token".encode("utf-8"))
    token = conn.recv(1024).decode("utf-8")
    return token


def register_client(db, email) -> str:
    cursor = db.cursor()
    token = None

    res = cursor.execute(f"SELECT id FROM users WHERE email = '{email}'")
    if res.fetchone() is not None:
        return ""

    while True:
        token = "".join(secrets.choice(ALPHABET) for _ in range(LEN_TOKEN))
        try:
            cursor.execute(f"INSERT INTO users VALUES (NULL, '{email}', '{token}')")
            db.commit()
            break
        except IntegrityError as ie:
            print(ie.sqlite_errorname, ie.args)
            break

    return token


def validate_client(db, email, token) -> bool:
    cursor = db.cursor()

    query = f"SELECT id FROM users WHERE email = '{email}' AND token = '{token}'"
    res = cursor.execute(query)
    if res.fetchone() is None:
        return False

    return True


def handle_client(conn, addr, dbname) -> None:
    """Manage connection with the client."""

    # Connect to the database
    db = sqlite3.connect(dbname)
    retries = 1

    conn.send("Please authenticate with 'a' or register with 'r'".encode("utf-8"))
    while True:
        data = conn.recv(1024).decode("utf-8")
        if data == "a":
            validated = False
            retries = 1
            while not validated:
                if retries > MAX_RETRIES:
                    break

                email = get_email(conn)
                token = get_token(conn)
                validated = validate_client(db, email, token)
                retries += 1

            if validated:
                conn.send("Client authenticated".encode("utf-8"))
                print(f"Client '{addr}' authenticated")
                break
            else:
                conn.send("Too many attempts. Reconnect".encode("utf-8"))
                conn.close()
                return
        elif data == "r":
            email = get_email(conn)

            # Register client
            token = register_client(db, email)
            if token:
                msg = f"Your token: '{token}'"
                print(f"New client '{email}' registered")
            else:
                msg = "Client already registered."
            msg += " Reconnect to authenticate"

            conn.send(msg.encode("utf-8"))
            conn.close()
            db.close()
            return
        elif retries > MAX_RETRIES:
            conn.send("Max retries reached, closing connection".encode("utf-8"))
            conn.close()
            db.close()
            print("User rejected. Too many retries")
            return
        else:
            conn.send("Wrong choice, please retry".encode("utf-8"))
            retries += 1

    conn.send("Ask me something".encode("utf-8"))
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from {addr}: {data.decode()}")

            data = input(f"Reply to {addr} -> ")
            conn.sendall(data.encode())
        except ConnectionResetError:
            print(f"Client {addr} has disconnected.")
            break

    conn.close()
    print(f"Connection with {addr} closed.")


def start_server():
    workdir = os.path.dirname(__file__)
    dbname = os.path.join(workdir, "cpto.db")

    # Check if the database exists
    dbinit = False
    if not os.path.exists(dbname):
        dbinit = True

    # Connect to the database
    db = sqlite3.connect(dbname)

    # Initialize database if needed
    if dbinit:
        with open(os.path.join(workdir, "init.sql")) as ifile:
            db.executescript(ifile.read())
            db.commit()
    db.close()

    # Initialize server
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        try:
            conn, addr = server.accept()
            conn.send("Welcome!".encode("utf-8"))
            print(f"Connection established with {addr}.")
        except KeyboardInterrupt:
            print("Server shutting down...")
            server.close()
            break

        thread = threading.Thread(target=handle_client, args=(conn, addr, dbname))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()
