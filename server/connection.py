import socket
import _thread as thread


class Connection:
    def __init__(self):
        self.sock = socket.socket()
        self.clients = []


    def start_server(self, port=5000):
        self.sock.bind(('', port))
        self.sock.listen(0)
        self.start_accept_thread()


    def disconnect(self):
        for c in self.clients:
            c.close()
        self.sock.close()


    def set_all_timeouts(self, timeout=10):
        for client in self.clients:
            client.settimeout(timeout)


    def accept_client(self):
        while True:
            client, addr = self.sock.accept()
            self.clients.append(client)

    def start_accept_thread(self):
        thread.start_new_thread(self.accept_client, ())


    def recv(self, client_index, recv_size):
        msg = self.clients[client_index].recv(recv_size)
        return msg


    def send(self, client_index, msg):
        try:
            return self.clients[client_index].send(msg)
        except:
            return None

    def send_by_thread(self, client_index, msg):
        thread.start_new_thread(self.send, (client_index, msg, ))

    def send2all(self, msg):
        for i in range(len(self.clients)):
            self.send_by_thread(i, msg)
