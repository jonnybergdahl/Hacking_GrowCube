import socket
from growcube_client.growcubemessage import GrowcubeMessage


class GrowcubeSocketClient:
    def __init__(self, host: str, port: int):
        self.sock = None
        self.host = host
        self.port = port
        self.data = b''

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def disconnect(self):
        if self.sock is not None:
            self.sock.close()
        self.sock = None

    def send_message(self, message: str):
        if not self.sock:
            raise ValueError('Not connected')
        message_bytes = message.encode('utf-8')
        self.sock.sendall(message_bytes)

    def receive_message(self):
        if not self.sock:
            raise ValueError('Not connected')

        #print(f"Current data: {self.data}")
        while True:
            # read from the socket
            data = self.sock.recv(1024)
            if not data:
                # no more data, return the message so far
                print("no more data")
                return None
            # Remove all b'\x00' characters, seems to be used for padding?
            data = bytearray(filter(lambda c: c != 0, data))
            # add the data to the message buffer
            self.data += data
            # check if we have a complete message
            new_index, message = GrowcubeMessage.from_bytes(self.data)
            self.data = self.data[new_index:]

            if message is None:
                print(f"Not complete data {self.data}")
                return None

            #print("Complete message found")
            # we have a complete message, remove consumed data
            return message

        return None

