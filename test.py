import json
from subprocess import Popen, PIPE

def wasser_request(user_cert, user_key, url, json_dict):
    command = 'openssl s_client -cert {0} -key {1} -connect {2}'.format(user_cert, user_key, url) 
    proc = Popen(command.split(' '), stdin=PIPE, stdout=PIPE)
    json_string=json.dumps(json_dict)
    json_len=len(json_string)
    request_body='POST / HTTP/1.1\nContent-Type: application/json\nContent-Length: {0}\n\n{1}'.format(json_len, json_string)
    a=proc.communicate(input=request_body)
    out = a[0]
    ind = out.find('HTTP/1.1')
    return out[ind:]

test_json={'wasser':'stein'}
print wasser_request('user.crt', 'user.key', 'localhost:1027',test_json)
