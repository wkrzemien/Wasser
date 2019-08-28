"""Tests for wasser module"""
from multiprocessing import Process
from time import sleep
import unittest
import json
from wasser import Wasser
from simple_ssl_server import SimpleServer


class TestServer(SimpleServer):
    """Server for tests"""
    def __init__(self, *args, **kwargs):
        super(TestServer, self).__init__(*args, **kwargs)
    def get(self, path):
        if path == '/':
            response = """HTTP/1.0 200 OK
                       Content-Type: text/html


                       <head>Test message ...</head>
                       <body>Hello there, general Kenobi</body>
                       """
            self.ssl_socket.send(response)
        elif path == '/second':
            reponse = """HTTP/1.1 200 OK
            Content-Type: text/plain


            Hello there"""
            self.ssl_socket.send(response)
    def post(self, path):
        if path == '/':
            if isinstance(self.message, dict):
                json_string = json.dumps(self.message)
                message_len = len(json_string)
                response = "HTTP/1.0 200 OK\nContent-Type: application/json\nContent-Length: {0}\n\n{1}".format(message_len, json_string)
            else:
                message = str(self.message)
                message_len = len(message)
                response = "HTTP/1.0 200 OK\nContent-Type: text/plain\nContent-Length: {0}\n\n{1}".format(message_len, message)
        self.ssl_socket.send(response)


class TestWasserRequest(unittest.TestCase):
    """Test for wasser requests"""
    def setUp(self):
        self.request = Wasser('certs/user.crt', 'certs/user.key', 'certs/CAcert.pem')
    def test_post_json_success(self):
        """Test for POST application/json success"""
        test_json = {'wasser':'stein'}
        json_string = json.dumps(test_json)
        message_len = len(json_string)
        expecting_response = "HTTP/1.0 200 OK\nContent-Type: text/plain\nContent-Length: {0}\n\n{1}".format(message_len, json_string)
        wasser_post_json_response = self.request.post('https://localhost:1027/', test_json)
        self.assertEqual(expecting_response, wasser_post_json_response)
    def test_post_text_success(self):
        """Test for POST text/plain success"""
        message = 'How are you'
        message_len = len(message)
        expecting_response = "HTTP/1.0 200 OK\nContent-Type: text/plain\nContent-Length: {0}\n\n{1}".format(message_len, message)
        wasser_post_text_response = self.request.post('https://localhost:1027/', message)
        self.assertEqual(expecting_response, wasser_post_text_response)
    def test_get_success(self):
        """Test for GET */* success"""
        expecting_response = """HTTP/1.0 200 OK
                       Content-Type: text/html


                       <head>Test message ...</head>
                       <body>Hello there, general Kenobi</body>
                       """
        wasser_get_response = self.request.get('https://localhost:1027/')
        self.assertEqual(expecting_response, wasser_get_response)
    def tearDown(self):
        pass


if __name__ == '__main__':
    addr = ('127.0.0.1', 1027)
    server_cert = 'certs/server.crt'
    server_key = 'certs/server.key'
    ca = 'certs/CAcert.pem'
    server = TestServer(addr, server_cert, server_key, ca, ['/', '/second'])
    server_process = Process(target=server.listen)
    server_process.start()
    sleep(1)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestWasserRequest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    server_process.terminate()
