Module wasser
-------------
Wasser module is created for providing https requests for Python 2.6,
where you don't have pyOpenSSL, cryptography and SSL wrapper for socket.
For using this module, you need to install OpenSSL


Classes
-------
Response 

Class for representation of server response, and manipulating data in it

Ancestors (in MRO)
------------------
wasser.Response

Instance variables
------------------

head - headers of http response

body - body of http response

code - code of http response

date - date of http response

content_length - length of body 

content_type - type of body

encoding - encoding of body

server - type of server, from which we get response

Methods
-------
```python
__init__(self, data)
```

    Creating and parsing response on
    headers,
    body,
    code of response,
    date of response,
    content_length,
    content_type,
    encoding,
    server



Wasser 
    Class to create https requests for Python 2.6


Instance variables
------------------

ca - path to your CA certificate for checking server certificate

user_cert - path to your certificate for connection

user_key - path to your key for connection

Methods
-------
```python
__init__(self, user_cert, user_key)
```
For creating https request you need to provide path for your certificate and key
```python
get(self, url)
```
GET request, provide fully qualified url
      as example - `https://localhost:1027/`
      not `localhost:1027/`

```python      
post(self, url, message)
```
POST request, provide url(as in ```get(self, url)``` method) and message to post
if type of message is dict -> request Content-Type will be application/json, else request will post text/plain

Example of usage
----------------
```python
from wasser import Wasser
request = Wasser('test.crt', 'test.key')
get_response = request.get('https://example.com/')
print get_response
text_message = 'Hello'
post_text_response = request.post('https://example.com/', text_message)
print post_text_responce
json_message = {'key':'value'}
post_json_response = request.post('https://example.com/', json_message)
print post_json_responce

```
