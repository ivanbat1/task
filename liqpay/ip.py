import http.client
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
print conn.getresponse().read()
import socket
print(socket.gethostname())

import socket
print socket.gethostname() # host name
print socket.gethostbyname(socket.gethostname()) # IPv4
import getpass
print getpass.getuser() # user name
# import os
# os.remove('test_string.py')