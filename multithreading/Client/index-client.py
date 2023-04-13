import threading
import socket

def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 5000))
    except:
        return print("Não foi possível estabelecer uma conexão com o servidor")
    
    username = input('Usuário: ')
    print('\n Conectado')
    
    thread1 = threading.Thread(target=receiveMessage, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])
    
    thread1.start()
    thread2.start()
    
def receiveMessage(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg,'\n')
        except:
            print('\n Não foi possível permancer conectado ao servidor')
            print('Pressione <Enter> para continuar')
            client.close()
            break
            
            
   
    
def sendMessages(client, username):
    while True:
        try:
            msg = input("\n")
            client.send(f"{msg}".encode('utf-8'))
        except:
            return
        
        
if __name__ == "__main__":
    main()