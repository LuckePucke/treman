import socket

s = socket.socket()

s.bind(("", 80))
s.listen(10)

while True:

    c, addr = s.accept()
    
    c.send(str.encode("sug min röv azco"))
    c.close()


