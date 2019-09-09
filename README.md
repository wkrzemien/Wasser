Module wasser
============
Wasser module is created for providing https requests for Python 2.6,
where you don't have pyOpenSSL, cryptography.
Here  SSL wrapper for socket is used.

Functions
---------
### get(url, cert, CA='certs/CAcert.pem', verify=True)
    GET method for https request, please provide:
    url - url which you want to connect,
    cert - tuple of your certificate and key, in this order
    verify - do you want to verify server certificate,
    CA - CA certificate which you want to use in verifying (only if verify = True)

### post(url, data, cert, CA='certs/CAcert.pem', verify=True)
    POST method for https request, please provide:
    url - url which you want to connect,
    data - message to POST,
    cert - tuple of your certificate and key, in this order
    verify - do you want to verify server certificate,
    CA - CA certificate which you want to use in verifying (only if verify = True)

Classes
-------
### RequestException 
    Exception for requests

    Ancestors (in MRO)
    ------------------
    wasser.RequestException
    exceptions.Exception
    exceptions.BaseException
    __builtin__.object

    Class variables
    ---------------
    args

    Instance variables
    ------------------
    message

    url

    Methods
    -------
    __init__(self, url, message)

### Response 
    Class for representation of server response, and manipulating data in it

    Ancestors (in MRO)
    ------------------
    wasser.Response
    __builtin__.object

    Instance variables
    ------------------
    body

    head

    headers

    Methods
    -------
    __init__(self, data)
        Creating and parsing response on
        headers,
        body,
        code of response,
        date of response,
        content_length,
        content_type,
        encoding,
        server



### Example of usage
```python
import wasser as request
get_response = request.get('https://example.com/', ('certs/mycert.crt', 'certs/mycert.key'))
print get_response
text_message = 'Hello'
post_text_response = request.post('https://example.com/', text_message, ('certs/mycert.crt', 'certs/mycert.key'), 'certs/MyCAcert.pem')
print post_text_responce
json_message = {'key':'value'}
post_json_response = request.post(url='https://example.com/', data=json_message, cert=('certs/mycert.crt', 'certs/mycert.key'), verify=False)
print post_json_responce

```
