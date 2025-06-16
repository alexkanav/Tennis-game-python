import pytest
import socket
from unittest import mock

from client.client_socket import ClientSocket


class TestClientSocket:
    def setup_method(self):
        self.host, self.port = '127.0.0.1', 9090
        self.client = ClientSocket(self.host, self.port)

    def test_client_socket_initialization(self):
        """Check if the socket is initialized with correct host and port """
        assert self.client.host == self.host
        assert self.client.port == self.port
        assert isinstance(self.client.sock, socket.socket)

    def test_socket_connect(self):
        # Mock socket creation to avoid making a real connection
        with mock.patch('socket.socket', autospec=True) as mock_socket:
            mock_sock_instance = mock_socket.return_value
            client = ClientSocket(self.host, self.port)
            client.connect()
            # Assert that the connect method on the mock socket was called with the correct parameters
            mock_sock_instance.connect.assert_called_once_with((self.host, self.port))

    def test_socket_connect_error(self):
        # Mock socket creation and simulate a connection error
        with mock.patch('socket.socket') as mock_socket:
            mock_sock_instance = mock_socket.return_value
            mock_sock_instance.connect.side_effect = socket.error("Connection failed")

            client = ClientSocket(self.host, self.port)
            # Verify that the exception is raised when calling connect
            with pytest.raises(socket.error, match="Connection failed"):
                client.connect()

    def test_client_socket_send(self):
        # Mocking the socket's send method to simulate sending data
        mock_sock = mock.Mock()
        self.client.sock = mock_sock
        self.client.send('Hello, Server!')
        mock_sock.send.assert_called_with(b'Hello, Server!')

    def test_client_socket_receive(self):
        # Mocking the socket's recv method to simulate receiving data
        mock_sock = mock.Mock()
        mock_sock.recv.return_value = b'Hello, Client!'
        self.client.sock = mock_sock
        received_data = self.client.receive()
        assert received_data == 'Hello, Client!'

    def test_socket_close(self):
        # Mock socket creation to avoid directly patching the socket's close method
        mock_sock = mock.Mock()
        self.client.sock = mock_sock
        self.client.close()
        mock_sock.close.assert_called_once()

