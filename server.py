# Imports
import socket
import threading

class tcpServer(object):	
    
    # Variables & constants
    running = True
    connections = {} # Dictionary {key: connection} where key <- connectionCounter
    connectionCounter = 0
    
    
    def __init__(self, clientHandlerFunction, port = 80, socketTimeout = None):
        self.socketTimeout = socketTimeout
        self.port = port
        self.fClientHandler = clientHandlerFunction
    
    def recv(self, connectionID, size):
        return self.connections[connectionID].recv(size)
    
    def send(self, connectionID, msg):
        self.connections[connectionID].send(msg)
    
    def sendString(self, connectionID, string):
        self.connections[connectionID].send(str.encode(string))
    
    def killConnection(self, connectionID):
        self.connections[connectionID].close()
        del self.connections[connectionID]
    
    # Thread functions
    def fConnections(self):
        # Handles all connections.
        # Inserts the connection into the connections directory with the address as the key.
        while self.running:
            # First we accept the new connection
            try:
                c, addr = self.s.accept()
            except:
                continue
            c.settimeout(self.socketTimeout)
            self.connections.update({self.connectionCounter: c})
            tNewClientHandler = threading.Thread(None, self.fClientHandler, None, (self, self.connectionCounter, addr), {})
            tNewClientHandler.start()
            self.connectionCounter += 1
    
    def start(self):
        self.s = socket.socket()
        self.s.settimeout(self.socketTimeout)
        self.s.bind(("", self.port))
        self.s.listen(10)
        # Connection thread:         reserved,    function,             name,        args, kwargs
        tConnections = threading.Thread(None, self.fConnections, "Connections thread", (), {})
        #tConnections.daemon = True
        tConnections.start()
    
    def isRunning(self):
        return self.running
    
    def stop(self):
        self.running = False
        for _, c in self.connections.items():
            c.close()
        self.s.close()
    



