import socket

HOST = "127.0.0.1"
PORT = 50000

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect((HOST, PORT))

soc.sendall(str.encode('Boa noite Diego!!'))

data = soc.recv(1024)

print(f"Mensagem ecoada: {data.decode()}")