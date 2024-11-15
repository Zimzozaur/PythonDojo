from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SO_REUSEADDR,
    SOL_SOCKET
)

from fib import fib


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        res = sock.accept()
        client, addr = res
        print("Connection", addr)
        fib_handler(client)


def fib_handler(client):
    while True:
        req = client.recv(100)
        print(req.decode("ascii").strip())
        if req.decode("ascii").strip() in ["^]" ""]:
            print("Continue")
            continue
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode("ascii") + b'\n'
        client.send(resp)
    print("Closed")


if __name__ == "__main__":
    fib_server(("", 25000))
