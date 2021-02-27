import socket as Socket
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import time

class Client:

    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.name = str(Socket.gethostbyname(Socket.gethostname()))
        self.receive_thread = None
        self.server_port = 9876
        self.server_host = ''
        self.groupchat_port = 0
        self.main()

    def main(self):
        self.server_host = input('Enter ip: ').strip()

        while True:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.server_port))
            while True:
                msg = input().strip()
                if msg == '/setname':
                    self.name = input().strip()

                elif msg == '/newgroup':
                    valid = False
                    while not valid:
                        self.client_socket.send(bytes('/newgroup', 'utf8'))
                        self.client_socket.send(bytes(input('Group name: '), 'utf8'))
                        self.client_socket.send(bytes(input('Password: '), 'utf8'))
                        valid = bool(self.client_socket.recv(1024).decode('utf8'))

                elif msg == '/connect':
                    self.client_socket.send(bytes('/getgroup', 'utf8'))
                    self.client_socket.send(bytes(input('Group name: '), 'utf8'))
                    self.groupchat_port = int(self.client_socket.recv(1024).decode('utf8'))
                    self.client_socket.close()
                    break

                elif msg == '/delete':
                    self.client_socket.send(bytes('/delete', 'utf8'))
                    self.client_socket.send(bytes(input('Group name: '), 'utf8'))
                    self.client_socket.send(bytes(input('Password: '), 'utf8'))

                else:
                    print('Unknown command!')

            if self.groupchat_port == -1:
                print('Group not found!')
                continue
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.groupchat_port))
            self.client_socket.send(bytes(input('Password: '), 'utf8'))
            if self.client_socket.recv(1024).decode('utf8') == '0':
                print('Wrong password!')
                self.client_socket.close()
                continue

            self.receive_thread = Thread(target=self.receive)
            self.receive_thread.start()
            while True:
                msg = input().strip()

                if msg == '/setname':
                    self.name = input().strip()

                elif msg == '/quit':
                    self.client_socket.close()
                    print('Disconnected')
                    break

                elif msg == '/data':
                    file = open('Test.txt','r')
                    fileData = file.read(1024)
                    self.client_socket.send(fileData, 'utf8')

                else:
                    self.client_socket.send(bytes(f'{self.name}: {msg}', 'utf8'))

    def send(self, msg):
        self.client_socket.send(bytes(msg, 'utf8'))

    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf8')
                print(msg)
            except OSError:
                break


if __name__ == '__main__':
    client = Client()
