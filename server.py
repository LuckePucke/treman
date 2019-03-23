import socket
import threading
import sys
import time
import random

# Read index file into memory
try:
    fIndex = open("index.html", "r")
    index = fIndex.read()
except:
    print("couldn't open index.html")
    sys.exit()

# Setup the socket handling the HTTP requests.
s = socket.socket()
s.bind(("", 80))
s.listen(10)

# Global variables & constants
running = True
connections = {}
connectionCounter = 0
rooms = {}

def responseHeader(len):
    
    return "HTTP/1.1 200 OK\nDate: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z") + "\nContent-Type: text/html; charset=UTF-8\nContent-Length: " + str(len) + "\nLast-Modified: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z") + "\nServer: Python/3.5.3 (Unix) (Raspbian 2018-11-13)\nETag: \"" + time.strftime("%a %d %b %Y %H %M %S") + "\"\nAccept-Ranges: bytes\nConnection: close\n\n"

# Thread functions
def fConnections():
    # Handles all connections.
    # Inserts the connection into the connections directory with the address as the key.
    global connections
    global connectionCounter
    while True:
        try:
            # First we accept the new connection
            c, addr = s.accept()
            connections.update({connectionCounter: c})
            tNewClientHandler = threading.Thread(None, fClientHandler, None, (connectionCounter, c, addr), {})
            tNewClientHandler.start()
            connectionCounter += 1
        except err:
            print("We had a failed connection: %s", err)

class room(object):
    def __init__(self):
        self.diceA = 0
        self.diceB = 0
    def roll(self):
        self.diceA = random.choice([1, 2, 3, 4, 5, 6])
        self.diceB = random.choice([1, 2, 3, 4, 5, 6])
    def dice(self):
        return str(self.diceA) + " " + str(self.diceB)

def fClientHandler(connectionID, c, addr):
    global connections
    global rooms
    global running
    global index
    with c:
        while running:
            data = c.recv(4096)
            if not data:
                c.close()
                del connections[connectionID]
                break
            sData = bytes.decode(data)
            print("\n#" + str(connectionID) + " Recieved:\n" + sData)
            if "text/html" not in sData:
                c.send(str.encode("HTTP 404 Not found"))
                c.close()
                del connections[connectionID]
                break
            if "GET /treman HTTP" in sData:
                c.send(str.encode(responseHeader(len(index)) + index))
            elif "GET /treman?roomCode=" in sData:
                roomCode = sData[21:25]
                if roomCode not in rooms:
                    rooms.update({roomCode: room()})
                page = "<html><body>\n"
                page += rooms[roomCode].dice()
                page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Roll\"></form>"
                page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Update\"></form>"
                page += "\n</body></html>"
                c.send(str.encode(responseHeader(len(page)) + page))
            elif "GET /treman?" in sData:
                roomCode = sData[12:16]
                if sData[17:21] == "Roll":
                    rooms[roomCode].roll()
                page = "<html><body>\n"
                page += rooms[roomCode].dice()
                page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Roll\"></form>"
                page += "\n<form action=\"/treman\" method=\"GET\"><input type=\"submit\" name=\""+ roomCode +"\" value=\"Update\"></form>"
                page += "\n</body></html>"
                c.send(str.encode(responseHeader(len(page)) + page))
            else:
                c.send(str.encode("HTTP 404 Not found"))
                c.close()
                del connections[connectionID]
                break



# Connection thread:		 reserved,	function,			name,		args, kwargs
tConnections = threading.Thread(None, fConnections, "Connections thread", (), {})
tConnections.daemon = True
tConnections.start()
_ = input("Press enter to shutdown the server.")
running = False
for addr, c in connections.items():
    c.close()
s.close()
print("Safe program exit.")

