PROJECT 2 - Web Crawler
*****************************************************************************************************
README
-----------------------------------------------------------------------------------------------------
Objective-
"""""""""
Implemented the Web Crawler in Python and successfully tested it on a Linux platform. 
It traverses HTML pages and collects five secret flags without using standard libraries
 to build HTTP request-response messages
1)	A TCP socket is created to connect to a server at port 80.
2)	Next a HTTP GET message is sent to the server to request the login page.
3)	Cookie id and session id are then fetched from the HTTP 200 success response from the server. 
4)	A well formatted POST message is then sent to the server with login credentials in it. 
        Server sends a success response with HTTP 302 found message. 
5)	The HTTP web page is then traversed to fetch all the links in it and store them in a list.
6)	Each element (links) of this link is then sent to server one-by-one and also compared with already visited pages to eliminate loops.
7)      The process is repeated untill five sectret flags are printed.
-----------------------------------------------------------------------------------------------------
Challenges faced-
""""""""""""""""
1)	To send HTTP POST and GET messages in proper format.
2)      To handle the connection close problem while program execution.
3)      To raise exceptions wherever necessary.
-----------------------------------------------------------------------------------------------------
Overview of code test procedure-
"""""""""""""""""""""""""""""""
1)	Checked the desired response codes at all steps.
2)      A function for socket creation is created to handle the connection close problem while code execution.s

