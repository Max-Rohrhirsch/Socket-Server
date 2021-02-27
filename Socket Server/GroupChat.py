#!/usr/bin/python3
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class GroupChat:
    def __init__(self, port, password):
        self.password = password
        self.client_list = []
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen()
        Thread(target=self.accept_clients).start()

    def close(self):
        self.server_socket.close()
        for client in self.client_list:
            client.close()

    def accept_clients(self):
        try:
            while True:
                client, addr = self.server_socket.accept()
                if client.recv(1024).decode('utf8') != self.password:
                    client.send(bytes('0', 'utf8'))
                    client.close()
                else:
                    print(addr, 'connected to GroupChat')
                    client.send(bytes('1', 'utf8'))
                    self.client_list.append(client)
                    Thread(target=self.handle_client, args=(client, addr,)).start()

        except OSError:
            return

    def handle_client(self, client, addr):
        try:
            while True:
                msg = client.recv(1024).decode('utf8')
                self.broadcast(msg)

        except (ConnectionResetError, OSError):
            client.close()
            del self.client_list[self.client_list.index(client)]
            print(addr, 'disconnected from GroupChat')
            return

    def broadcast(self, msg):
        for client in self.client_list:
            client.send(bytes(msg, 'utf8'))
