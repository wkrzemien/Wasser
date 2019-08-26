'''This is simple server, which is based on sockets and ssl '''

import ssl
import socket
import sys

class Server:
    """Class for receiving and answering data from TLS connection"""
    def __init__(self, addr, cert, key, CA):
        """Creating socket"""
        self.addr = addr
        self.cert = cert
        self.key = key
        self.ca = CA
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(addr)
    def listen(self):
        """Listening on socket"""
        print 'Begin listening\n'
        self.sock.listen(5)
        while True:
            self.handle()
    def handle(self):
        """Simple handler for TLS connection"""
        connection_stream, fromaddr = self.sock.accept()

        ssl_socket = ssl.wrap_socket(connection_stream,
                                     certfile=self.cert,
                                     keyfile=self.key,
                                     ca_certs=self.ca,
                                     cert_reqs=ssl.CERT_REQUIRED,
                                     server_side=True)
        data = ssl_socket.read()
        print '\n\nThis person sending message to us - {0}'.format(fromaddr)
        cert = ssl_socket.getpeercert()
        print 'Certificate of person:'
        print cert
        print 'Message:'
        print data
        ssl_socket.write('Hello')
        ssl_socket.close()
    def close(self):
        self.sock.close()

if __name__ == '__main__':
    addr = ('127.0.0.1', 1027)
    server_cert = '/certs/server.crt'
    server_key = '/certs/server.key'
    ca = '/certs/CAcert.pem'
    server = Server(addr, server_cert, server_key, ca)
    try:
        server.listen()
    except KeyboardInterrupt:
        server.close()
        print '\nConnection closed'
        sys.exit()

