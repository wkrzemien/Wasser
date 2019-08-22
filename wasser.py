"""Wasser module is created for providing https requests for Python 2.6,
   where you don't have pyOpenSSL, cryptography and SSL wrapper for socket.
   For using this module, you need to install OpenSSL"""

import json
from subprocess import Popen, PIPE
from urlparse import urlparse


class Wasser:
    """Class to create https requests for Python 2.6"""
    def __init__(self, user_cert, user_key):
        """For creating https request you need to provide path for your
        certificate and key"""
        self.user_cert = user_cert
        self.user_key = user_key
    def get(self, url):
        """GET request, provide fully qualified url
           as example - https://localhost:1027/
           not localhost:1027/"""
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        command = 'openssl s_client -cert {0} -key {1} -connect {2}'.format(self.user_cert, self.user_key, host)
        proc = Popen(command.split(' '), stdin=PIPE, stdout=PIPE)
        request_body = 'GET {0} HTTP/1.1\nAccept: text/plain\n\n'.format(path)
        response_of_process = proc.communicate(input=request_body)
        out = response_of_process[0]
        ind = out.find('HTTP/1.1')
        return out[ind:]
    def post_json(self, url, json_dict):
        """POST request, provide url and json to post"""
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        command = 'openssl s_client -cert {0} -key {1} -connect {2}'.format(self.user_cert, self.user_key, host)
        proc = Popen(command.split(' '), stdin=PIPE, stdout=PIPE)
        json_string = json.dumps(json_dict)
        json_len = len(json_string)
        request_body = 'POST {0} HTTP/1.1\nContent-Type: application/json\nContent-Length: {1}\n\n{2}'.format(path, json_len, json_string)
        print request_body
        response_of_process = proc.communicate(input=request_body)
        out = response_of_process[0]
        ind = out.find('HTTP/1.1')
        return out[ind:]


if __name__ == '__main__':
    test_json = {'wasser':'stein'}
    new_request = Wasser('user.crt', 'user.key')
    print '\nPOST request\n'
    print new_request.post_json('https://localhost:1027/', test_json)
    print '\nGET request\n'
    print new_request.get('https://localhost:1027/')
