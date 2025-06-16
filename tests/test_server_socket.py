import pytest
import socket
from unittest import mock

from server.server_socket import ServerSocket


class TestServerSocket:
    def setup_method(self):
        self.host, self.port = '127.0.0.1', 9090

    def test_server_socket_initialization(self):
        """Check if the socket is initialized with correct host and port """
        with mock.patch('socket.socket') as mock_socket:
            mock_sock_instance = mock_socket.return_value
            server = ServerSocket(self.host, self.port)
            mock_sock_instance.bind.assert_called_once_with((self.host, self.port))
            mock_sock_instance.listen.assert_called_once_with(1)
            assert server.sock == mock_sock_instance

    def test_server_socket_accept_connection(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_sock_instance = mock_socket.return_value
            mock_conn = mock.Mock()
            mock_addr = ('127.0.0.1', 12345)
            mock_sock_instance.accept.return_value = (mock_conn, mock_addr)
            server = ServerSocket(self.host, self.port)
            result = server.connection()
            assert server.conn == mock_conn
            assert server.addr == mock_addr
            assert result == f'connected: {mock_addr}'

    def test_server_socket_receive(self):
        server = ServerSocket.__new__(ServerSocket)  # avoid running __init__
        mock_conn = mock.Mock()
        mock_conn.recv.return_value = b'Hello, Server!'
        server.conn = mock_conn
        data = server.receive()
        assert data == 'Hello, Server!'
        mock_conn.recv.assert_called_once_with(1024)

    def test_server_socket_send(self):
        server = ServerSocket.__new__(ServerSocket)
        mock_conn = mock.Mock()
        server.conn = mock_conn
        server.send("Hello, Client!")
        mock_conn.send.assert_called_once_with(b'Hello, Client!')

    def test_server_socket_close(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_sock_instance = mock_socket.return_value
            server = ServerSocket(self.host, self.port)
            server.sock = mock_sock_instance
            server.close()
            mock_sock_instance.close.assert_called_once()

    def test_server_accept_raises_exception(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_sock_instance = mock_socket.return_value
            mock_sock_instance.accept.side_effect = OSError("Accept failed")
            server = ServerSocket('127.0.0.1', 9090)
            with pytest.raises(OSError, match="Accept failed"):
                server.connection()
