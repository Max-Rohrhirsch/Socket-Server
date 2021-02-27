#!/usr/bin/python3
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from GroupChat import GroupChat


class SocketServer:
    def __init__(self, port):
        self.current_port = 9999
        self.group_list = {}
        self.client_list = []
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen()
        Thread(target=self.accept_clients).start()
        Thread(target=self.exit_thread).start()

    def close(self):
        self.server_socket.close()
        for client in self.client_list:
            client.close()
        for group_chat in self.group_list.values():
            group_chat.close()

    def exit_thread(self):
        while True:
            input()
            self.close()
            return

    def accept_clients(self):
        try:
            while True:
                client, addr = self.server_socket.accept()
                print(addr, 'connected to socket_server')
                self.client_list.append(client)
                Thread(target=self.handle_client, args=(client, addr,)).start()
        except:
            return

    def handle_client(self, client, addr):
        try:
            while True:
                msg = client.recv(1024).decode('utf8')

                if msg == '/newgroup':
                    groupname = client.recv(1024).decode('utf8')
                    password = client.recv(1024).decode('utf8')
                    print(f'new group "{groupname}" created')
                    while groupname in self.group_list:
                        client.send(bytes('0', 'utf8'))
                        groupname = client.recv(1024).decode('utf8')
                    client.send(bytes('1', 'utf8'))
                    self.group_list[groupname] = GroupChat(self.current_port, password)
                    self.current_port -= 1

                elif msg == '/getgroup':
                    groupname = client.recv(1024).decode('utf8')

                    if groupname in self.group_list:
                        client.send(bytes(str(self.group_list[groupname].server_socket.getsockname()[1]), 'utf8'))
                        print(f'get group {groupname}')
                    else:
                        client.send(bytes('-1', 'utf8'))

                elif msg == '/delete':
                    groupname = client.recv(1024).decode('utf8')
                    password = client.recv(1024).decode('utf8')
                    if groupname in self.group_list and self.group_list[groupname].password == password:
                        self.group_list[groupname].close()
                        del self.group_list[groupname]
                        print(f'{groupname} deleted.')

                else:
                    client.send(bytes('Unknown command!', 'utf8'))


        except (ConnectionResetError, OSError):
            client.close()
            print(addr, 'disconnected from socket_server')
            return


if __name__ == '__main__':
    socketServer = SocketServer(9876)
