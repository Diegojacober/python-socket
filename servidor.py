import socket

HOST = "127.0.0.1"
PORT = 50000

#ipv4,tcp 
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind((HOST, PORT))
#modo de escuta
soc.listen()
print("Aguardando conexão de um cliente")

#aceitando uma conexão
conexao, endereco = soc.accept()

print(f"Conectado em {endereco}")

while True:
    #tamanho maximo dos dados que esperamos receber
    data = conexao.recv(1024)
    # if not data:
    #     print("Fechando conexão")
    #     conexao.close()
    #     break
    # print("Enviando dados de volta")
    print(data)
    conexao.sendall(data)
    