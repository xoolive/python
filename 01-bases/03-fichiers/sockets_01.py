# Dans un terminal différent, entrer la commande suivante:
#  $ nc localhost 12345

from datetime import datetime, timezone
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # ①
    s.bind(("127.0.0.1", 12345))  # ②
    s.listen()  # ③
    conn, addr = s.accept()  # ④
    with conn:
        now: datetime = datetime.now(tz=timezone.utc)
        conn.sendall(str(now).encode())  # ⑤
