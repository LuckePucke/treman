
# Imports
import sys
import time
import server
import random

class room(object):
    def __init__(self):
        self.diceA = 0
        self.diceB = 0
    def roll(self):
        self.diceA = random.choice([1, 2, 3, 4, 5, 6])
        self.diceB = random.choice([1, 2, 3, 4, 5, 6])
    def dice(self):
        return str(self.diceA) + " " + str(self.diceB)

rooms = {}

def responseHeader(len):
    
    return "HTTP/1.1 200 OK\nDate: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z") + "\nContent-Type: text/html; charset=UTF-8\nContent-Length: " + str(len) + "\nLast-Modified: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z") + "\nServer: Python/3.5.3 (Unix) (Raspbian 2018-11-13)\nETag: \"" + time.strftime("%a %d %b %Y %H %M %S") + "\"\nAccept-Ranges: bytes\nConnection: close\n\n"

def fClientHandler(server, connectionID, addr):
    
    print("connectionID: {}".format(connectionID))
    while server.isRunning():
        try:
            data = server.recv(connectionID, 4096)
        except:
            continue
        if not data:
            server.killConnection(connectionID)
            break
        sData = bytes.decode(data)
        print("\n#" + str(connectionID) + " Recieved:\n" + sData)
        if "text/html" not in sData:
            server.sendString(connectionID, "HTTP 404 Not found")
            server.killConnection(connectionID)
            break
        if "GET /treman HTTP" in sData:
            server.sendString(connectionID, responseHeader(len(index)) + index)
        elif "GET /treman?roomCode=" in sData:
            roomCode = sData[21:25]
            if roomCode not in rooms:
                rooms.update({roomCode: room()})
            page = "<html><body>\n"
            page += rooms[roomCode].dice()
            page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Roll\"></form>"
            page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Update\"></form>"
            page += "\n</body></html>"
            server.sendString(connectionID, responseHeader(len(page)) + page)
        elif "GET /treman?" in sData:
            roomCode = sData[12:16]
            if sData[17:21] == "Roll":
                rooms[roomCode].roll()
            page = "<html><body>\n"
            page += rooms[roomCode].dice()
            page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Roll\"></form>"
            page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Update\"></form>"
            page += "\n</body></html>"
            server.sendString(connectionID, responseHeader(len(page)) + page)
        else:
            server.sendString(connectionID, "HTTP 404 Not found")
            server.killConnection(connectionID)
            break


# Read index file into memory
try:
    fIndex = open("index.html", "r")
    index = fIndex.read()
except:
    print("couldn't open index.html")
    sys.exit()

s = server.tcpServer(fClientHandler, 80, 5)
s.start()
_ = input("Press enter to shutdown the server.\n")
s.stop()
print("Killing server. Please allow up to 6 seconds.")


