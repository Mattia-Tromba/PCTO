import socket

from consts import HOST, PORT

MSG_SERVER = "Server ->"
MSG_CLIENT = "You <- "


def main():
    conn = socket.socket()
    conn.connect((HOST, PORT))

    print(MSG_SERVER, conn.recv(1024).decode())
    while True:
        msgout = conn.recv(1024).decode()
        print(MSG_SERVER, msgout)

        # List of exit points
        if "Max retries reached" in msgout:
            break
        elif "Reconnect" in msgout:
            break
        elif "authenticated" in msgout:
            continue

        # Check input
        msgin = input(MSG_CLIENT)
        if msgin == "bye":
            break
        conn.send(msgin.encode("utf-8"))

    conn.close()


if __name__ == "__main__":
    main()
