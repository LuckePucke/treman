import socket
import threading
import sys

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

def fClientHandler(connectionID, c, addr):
    global connections
    global running
    global index
    with c:
        while running:
            data = c.recv(4096)
            if not data:
                del connections[connectionID]
                break
            sData = bytes.decode(data)
            print("\n#" + str(connectionID) + " Recieved:\n" + sData)
            if "GET /" in sData:
                c.send(str.encode(index) + bytes([200]))
            else:
                c.send(str.encode("<html><body>This method is not yet implemented.</body></html>" + bytes([200])))



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

