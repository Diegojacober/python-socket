import threading
import socket


def get_option():
     while True:
            try: 
                opc = input(f'\n').strip()[0:1]
                opc = int(opc)
            except:
                print('\033[31mDigite apenas numeros\033[m')
            else:
                if opc > 0 and opc <= 9:
                    if opc == 1:
                        return '0,0'
                    elif opc == 2:
                        return '0,1'
                    elif opc == 3:
                        return '0,2'
                    elif opc == 4:
                        return '1,0'
                    elif opc == 5:
                        return '1,1'
                    elif opc == 6:
                        return '1,2'
                    elif opc == 7:
                        return '2,0'
                    elif opc == 8:
                        return '2,1'
                    elif opc == 9:
                        return '2,2'
                print('\033[31mDigite apenas um desses: 1, 2, 3, 4, 5, 6, 7, 8, 9\033[m')   
                

def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('10.21.58.85', 5000))
    except:
        return print("Não foi possível estabelecer uma conexão com o servidor")
    
    username = input('Usuário: ')
    print('\nConectado')
    

    thread2 = threading.Thread(target=sendMessages, args=[client, username])
    thread1 = threading.Thread(target=receiveMessage, args=[client])
    
    thread2.start()
    thread1.start()
    
    
def receiveMessage(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print("\x1b[2J\x1b[1;1H", end="")
            print('\n',msg,'\n')
        except:
            print('\n Não foi possível permancer conectado ao servidor')
            print('Pressione <Enter> para continuar')
            client.close()
            exit()
            
            
   
    
def sendMessages(client, username):
    while True:
        try:
            msg = ''
            while True:
                msg = get_option()
                client.send(f"{msg}".encode('utf-8'))
        except:
            return
        
        
if __name__ == "__main__":
    main()