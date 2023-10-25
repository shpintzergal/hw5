import socket
import threading
import struct

class TCPServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

    def handle_client(self, client_socket):
        try:
            for i in range(100):
                messages = self.receive_messages(client_socket)
                print(f"Received messages: {messages}")

                response = "Message received: " + ", ".join(messages)
                self.send_messages(client_socket, response)

        finally:
            client_socket.close()

    def send_messages(self, client_socket, *messages):
        messages_data = b"".join(struct.pack('!I', len(message)) + message.encode('utf-8') for message in messages)
        total_length = len(messages_data)
        client_socket.sendall(struct.pack('!I', total_length))
        client_socket.sendall(messages_data)

    def receive_messages(self, client_socket):
        header_data = client_socket.recv(4)
        if not header_data:
            return None

        total_length = struct.unpack('!I', header_data)[0]

        data = b""
        while len(data) < total_length:
            chunk = client_socket.recv(total_length - len(data))
            if not chunk:
                break
            data += chunk

        messages = []
        index = 0
        while index < total_length:
            message_length = struct.unpack('!I', data[index:index + 4])[0]
            index += 4
            message = data[index:index + message_length].decode('utf-8')
            messages.append(message)
            index += message_length

        return messages

    def start(self):
        print(f"Server is waiting for client {self.server_socket.getsockname()}")

        while True:
            client_socket, _ = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    server = TCPServer('localhost', 6120)
    server.start()
