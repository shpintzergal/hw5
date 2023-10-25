import socket
import struct

class TCPClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_messages(self, *messages):
        messages_data = b"".join(struct.pack('!I', len(message)) + message.encode('utf-8') for message in messages)
        total_length = len(messages_data)
        self.client_socket.sendall(struct.pack('!I', total_length))
        self.client_socket.sendall(messages_data)

    def receive_messages(self):
        header_data = self.client_socket.recv(4)
        if not header_data:
            return None

        total_length = struct.unpack('!I', header_data)[0]

        data = b""
        while len(data) < total_length:
            chunk = self.client_socket.recv(total_length - len(data))
            if not chunk:
                break
            data += chunk

        messages = []
        index = 0
        while index < len(data):
            message_length = struct.unpack('!I', data[index:index + 4])[0]
            index += 4
            message = data[index:index + message_length].decode('utf-8')
            messages.append(message)
            index += message_length

        return messages

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    client = TCPClient('localhost', 6120)

    for i in range(100):
        client.send_messages("Hello, Server!", "Some data")
        server_response = client.receive_messages()
        print(f"Received from server: {server_response}")

    client.close()
