import socket, time
import threading as thread

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
clientes = [None,None]
def conectado(con, cliente):
    print('Conectado por', cliente)

    while True:
        msg = con.recv(1024)
        retorno = ''
        if not msg: break
        if clientes[0] == None:
            clientes[0] = cliente[1]
            print('Jogador 1 conectado')
        elif clientes[1] == None:
            clientes[1] = cliente[1]
            print('Jogador 2 conectado')
        else:
            print("Jogadores conectados")
        
        if cliente[1] == clientes[1]:
            print(f"O jogador O enviou a seguinte mensagem: {msg}")
            retorno = 'Olá jogador 2'
        elif cliente[1] == clientes[0]:
            print(f"O jogador X enviou a seguinte mensagem: {msg}")
            retorno = 'Olá jogador 1'
        else:
            print("Outro jogador tentou invadir o jogo")
            retorno = 'Desculpa você está tentando entrar em uma sala cheia'
            
        time.sleep(2)
        con.sendall(retorno.encode())
        # print (cliente[1])

    print ('Finalizando conexao do cliente', cliente)
    con.close()
    thread._exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread._start_new_thread(conectado, tuple([con, cliente]))
tcp.close()