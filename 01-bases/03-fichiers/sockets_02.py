import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # ⑥
    s.connect(("freechess.org", 5000))
    while True:
        data: bytes = s.recv(256)  # ⑦
        if len(data) == 0:  # ⑧
            break
        print(data.decode())  # ⑨
