import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('api.ipify.org', 80))
    request = b"GET / HTTP/1.1\r\nHost: api.ipify.org\r\n\r\n"
    s.send(request)
    print(s.recv(4096).decode())

main()
