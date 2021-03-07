import socket
from io import BytesIO

content = BytesIO()  # création du flux de données binaires

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("towel.blinkenlights.nl", 666))
    while True:
        data: bytes = s.recv(1024)
        if len(data) == 0:
            break
        content.write(data)  # écriture séquentielle

content.seek(0)  # On se place au début du flux
data = content.read()  # puis on lit l'intégralité du flux

clear_idx = data.find(b"\x1b[")
while clear_idx != -1:
    # Effacement du contenu jusqu'au dernier caractère de contrôle
    data = data[clear_idx + 3 :]
    clear_idx = data.find(b"\x1b[")

print(data.decode())  # passage en chaîne de caractères
