import threading
import socket
import time


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
                board += "----------\n"

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



clients = []
addrs = []
jogo = Game()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 5000))
        # recebe somente duas conexões, se não passar ele recebe quantas conexões chegarem
        server.listen(2)
    except:
        return print('Não foi possível iniciar o servidor')

    while True:
        client, addr = server.accept()
      
        clients.append(client)
        addrs.append(addr[1])
        if len(clients) < 2:
            time.sleep(2)
            broadcast(msg='Aguardando jogadores', client=client)
        if len(clients) == 2:
            if jogo.player1_port == None or jogo.player2_port == None:
                jogo.player1_port = addrs[0]
                jogo.player2_port = addrs[1]
                
             

        thread = threading.Thread(target=messagesTreatment, args=[client,addr[1]])
        thread.start()


def delete_client(client):
    clients.remove(client)


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg.encode())
            except:
                delete_client(clientItem)
        else:
            ...


def messagesTreatment(client, port):
    while True:
        try:
            retorno = None
            msg = client.recv(2048)
            if jogo.turn == "X" and jogo.player1_port == port:
                posicoes = msg.decode().split(",")
                print(posicoes)
                if jogo.check_valid_move(posicoes):
                    jogo.apply_move(posicoes)
                    
            if jogo.turn == "O" and jogo.player2_port == port:
                posicoes = msg.decode().split(",")
                print(posicoes)
                if jogo.check_valid_move(posicoes):
                    jogo.apply_move(posicoes)
            
            print(jogo.print_board())
                    
                    
            broadcast(msg=msg, client=client)
        except:
            delete_client(client)
            break


if __name__ == "__main__":
    main()
