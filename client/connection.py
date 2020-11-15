import socket


class Connection:
    def __init__(self):
        self.sock = socket.socket()


    def connect(self, host='127.0.0.1', port=5000):
        self.sock.connect((host, port))


    def disconnect(self):
        self.sock.close()


    def recv(self, recv_size):
        msg = self.sock.recv(recv_size)
        return msg


    def send(self, msg):
        try:
            return self.sock.send(msg)
        except:
            return None

