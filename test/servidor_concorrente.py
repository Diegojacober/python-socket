import socket, time
import threading as thread


class Game():
    def __init__(self) -> None:
        self.__board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.__game_over = False
        self.__player1_port = None
        self.__player2_port = None
        self.counter = 0 

    @property
    def player1_port(self):
        return self.__player1_port
    
    @player1_port.setter
    def player1_port(self, val):
        self.__player1_port = val
        
    @property
    def player2_port(self):
        return self.__player2_port
    
    @player2_port.setter
    def player2_port(self, val):
        self.__player2_port = val
        
        
    def print_board(self):
        board = ''
        for row in range(3):
            board += (" | ".join(self.__board[row])+"\n")
            if row != 2:
                board+="----------\n"
        
        return board
    
    
    def check_valid_move(self, move):
        return self.__board[int(move[0])][int(move[1])] == " "
    
    def check_if_won(self):
        for row in range(3):
            if self.__board[row][0] == self.__board[row][1] == self.__board[row][2] != " ":
                self.__winner = self.__board[row][0]
                self.__game_over = True
                return True
        for col in range(3):
            if self.__board[0][col] == self.__board[1][col] == self.__board[2][col] != " ":
                self.__winner = self.__board[0][col]
                self.__game_over = True
                return True
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != " ":
            self.__winner = self.__board[0][0]
            self.__game_over = True
            return True
        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != " ":
            self.__winner = self.__board[0][2]
            self.__game_over = True
            return True
        return False
    
    def apply_move(self, move):
        if self.__game_over:
            return
        self.counter += 1
        self.__board[int(move[0])][int(move[1])] = self.turn
        # self.print_board()
        self.turn = "O" if self.turn == "X" else "X"
        if self.check_if_won():
            if self.__winner == "X":
                return "Player X won"
                # exit()
            elif self.__winner == "O":
                return "Player O won"
        else:
            if self.counter == 9:
                return "It is a tie"
    

HOST = '127.0.0.1'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
clientes = [None,None]
conexoes = []
jogo = Game()
def conectado(con, cliente):
    print('Conectado por', cliente)
    
    while True:
        
        retorno = None
        msg = con.recv(1024)
        retorno = ''
        if not msg: break
        if clientes[0] == None:
            clientes[0] = cliente[1]
            jogo.player1_port = clientes[0]
            conexoes.append(cliente)
            print('Jogador 1 conectado')
        elif clientes[1] == None:
            clientes[1] = cliente[1]
            jogo.player2_port = clientes[1] 
            conexoes.append(cliente)
            print('Jogador 2 conectado')
            
        if jogo.player1_port != None and jogo.player2_port != None:
            if cliente[1] == clientes[0]:
                #jogador 1
                # con.sendto("oi".encode(),("127.0.0.1",clientes[1]))
                if jogo.turn == "X":
                    posicoes = msg.decode().split(",")
                    if jogo.check_valid_move(posicoes):
                        jogo.apply_move(posicoes)
                        retorno = jogo.print_board()
                        print("Jogadores conectados")
                        
                else:
                    retorno = "Jogador 1 tentou jogar na vez do jogador 2"
            if cliente[1] == clientes[1]:
                # jogador 2
                if jogo.turn == "O":
                    print(msg.decode())
                    posicoes = msg.decode().split(",")
                    print(posicoes)
                    if jogo.check_valid_move(posicoes):
                        jogo.apply_move(posicoes)
                        retorno = jogo.print_board()
                        print("Adicionado no board")
                        print(con)
                else:
                    retorno = "Jogador 2 tentou jogar na vez do jogador 1"
        else:
            print(f"Jogadores conectados: {clientes}")
            retorno = "Aguardando jogadores"
        # else:
        #     print("Outro jogador tentou invadir o jogo")
        #     retorno = 'Desculpa você está tentando entrar em uma sala cheia'
            
        time.sleep(2)
        con.sendall(retorno.encode())

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