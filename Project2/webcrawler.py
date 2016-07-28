#!/usr/bin/env python

import sys
import socket
import re
from bs4 import BeautifulSoup

username = sys.argv[1]
password = sys.argv[2]

def sock_get(a,token,session):
    get_msg = 'GET '+a+' HTTP/1.0\r\nConnection: Keep-Alive\r\n'\
              'Referer: http://cs5700sp15.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n'\
              'Cookie: csrftoken=' + token + "; sessionid=" +session+'\r\n'\
              '\r\n'
    #print(get_msg.encode())
    s.send(get_msg)
    h = s.recv(100000000).decode()
    return h

host ="cs5700sp15.ccs.neu.edu"
port = 80

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
except:
    print('Socket creation error')

#Initial HTTP GET request
s.send("GET /accounts/login/?next=/fakebook/. HTTP/1.0\r\nConnection: Keep-Alive\r\n\r\n".encode())
data = s.recv(1000000).decode()
#resend if received message is truncated
while data.find("</html>") == -1:
    s.send("GET /accounts/login/?next=/fakebook/. HTTP/1.0\r\nConnection: Keep-Alive\r\n\r\n".encode())
    data = s.recv(1000000).decode()
#if server closes the connection in between	
a = data.find("Connection: Keep-Alive")
while a == -1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send("GET /accounts/login/?next=/fakebook/. HTTP/1.0\r\nConnection: Keep-Alive\r\n\r\n".encode())
    data = s.recv(1000000).decode()
    while data.find("</html>") == -1:
	s.send("GET /accounts/login/?next=/fakebook/. HTTP/1.0\r\nConnection: Keep-Alive\r\n\r\n".encode())
	data = s.recv(1000000).decode()
    a = data.find("Connection: Keep-Alive")

#To fetch cookie id and session ID
soup = BeautifulSoup(data)
token = soup.find('input', dict(name='csrfmiddlewaretoken'))['value'] 

b = re.search("sessionid=",data)
session = data[b.end(): b.end()+32]

#POST message to request login
post_msg = 'POST /accounts/login/ HTTP/1.0\r\nHost: cs5700sp15.ccs.neu.edu\r\n'\
           'Connection: keep-alive\r\nContent-Length: 107\r\n'\
           'Origin: http://cs5700sp15.ccs.neu.edu\r\n'\
           'Content-Type: application/x-www-form-urlencoded\r\n'\
           'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'\
           'Referer: http://cs5700sp15.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n'\
           'Accept-Encoding: gzip, deflate\r\n'\
           'Cookie: csrftoken=' + token + "; sessionid=" +session+'\r\n'\
           '\r\n'\
           'csrfmiddlewaretoken='+token+'&username='+username+'&password='+password+'&next=/fakebook/\r\n'

s.send(post_msg.encode())
abc = str(s.recv(100000))
#To fetch updated session ID
b = re.search("sessionid=",abc)
session = abc[b.end(): b.end()+32]

url = "/fakebook/"

urls = [url]
visited = [url]
count = 0
#Crawling code
while len(urls)>0:
    try:
        url123 = urls[0]
	h = sock_get(url123, token, session)	
	if h.find("</html>") == -1:
	 	h = sock_get(url123,token, session)
        a = h.find("Connection: Keep-Alive")            		
        while a == -1:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            h = sock_get(url123,token,session)
            a = h.find("Connection: Keep-Alive")

	soup = BeautifulSoup(h)
        urls.pop(0)

	p = str(soup.find('h2', attrs={'class': 'secret_flag'}))
	if(p != 'None'):
            print(p[47:112])
	    count = count+1
	if(count == 5):            
	    sys.exit()
        for tag in soup.findAll('a',href=True):
            #print(tag['href'])
            if url in tag['href'] and tag['href'] not in visited:
            	urls.append(tag['href'])
		visited.append(tag['href'])
        #print(len(urls))
	#print(urls)
    except Exception as msg:
        print(msg)

