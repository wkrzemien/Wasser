'''This is simple server, which is based on sockets and ssl '''

import json
import ssl
import socket
import sys
import re

class SimpleServer(object):
    """Class for receiving and answering data from TLS connection"""
    def __init__(self, addr, cert, key, CA, path_array):
        """Creating socket"""
        self.addr = addr
        self.cert = cert
        self.key = key
        self.ca = CA
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.path = path_array
    def listen(self):
        """Listening on socket"""
        print 'Begin listening\n'
        self.sock.listen(5)
        while True:
            self.handle()
    def handle(self):
        """Simple handler for TLS connection"""
        connection_stream, fromaddr = self.sock.accept()

        self.ssl_socket = ssl.wrap_socket(connection_stream,
                                     certfile=self.cert,
                                     keyfile=self.key,
                                     ca_certs=self.ca,
                                     cert_reqs=ssl.CERT_REQUIRED,
                                     server_side=True)
        data = self.ssl_socket.read()
        print '\n\nThis person sending message to us - {0}'.format(fromaddr)
        cert = self.ssl_socket.getpeercert()
        print 'Certificate of person:'
        print cert
        print 'Message:'
        print data
        for path in self.path:
            if re.search('GET {0} HTTP/1.1'.format(path), data):
                self.get(path)
            if re.search('POST {0} HTTP/1.1'.format(path), data):
                [head, self.message] = data.split('\n\n')
                self.post(path)
        self.ssl_socket.close()
    def close(self):
        """Close socket"""
        self.sock.close()
    def get(self, path):
        """GET path handler"""
        pass
    def post(self, path):
        """POST path handler"""
        pass

class Server(SimpleServer):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
    def get(self, path):
        if path == '/':
            print 'GET /'
            response = """HTTP/1.0 200 OK
                       Content-Type: text/html


                       <head>Test message ...</head>
                       <body>Hello there, general Kenobi</body>
                       """
            self.ssl_socket.send(response)
        elif path == '/hi':
            self.ssl_socket.send('HTTP/1.0 200 OK\n')
            self.ssl_socket.send('Content-Type: text/html\n\n')
            self.ssl_socket.send("""<body>Hi. How are you ?</body>""")
        else:
            self.ssl_socket.send('HTTP/1.0 404 Not Found\n')
            self.ssl_socket.send('Content-Type: text/html\n\n')
            self.ssl_socket.send("""<body>There is no get method for this page</body>""")
    def post(self, path):
        print self.message
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




if __name__ == '__main__':
    addr = ('127.0.0.1', 1027)
    server_cert = 'certs/server.crt'
    server_key = 'certs/server.key'
    ca = 'certs/CAcert.pem'
    server = Server(addr, server_cert, server_key, ca, ['/', '/hi', '/2'])
    try:
        server.listen()
    except KeyboardInterrupt:
        server.close()
        print '\nConnection closed'
        sys.exit()

