import socket
import threading

# Setup the socket handling the HTTP requests.
s = socket.socket()
s.bind(("", 80))
s.listen(10)

# Global variables & constants
running = True
connections = []

# Connection thread:         reserved,  function,           name,       args, kwargs
tConnections = threading.Thread(None, fConnections, "Connections thread", (), {})

# Thread functions
def fConnections():
	while running:
		c, addr = s.accept()
		tNewClientHandler = threading.Thread(None, fClientHandler, None, (c, addr), {})
		tNewClientHandler.daemon = True
		connections.append(c, addr)
		tNewClientHandler.start()
	for c, _ in connections:
		c.close()

def fClientHandler(c, addr):
	while running:
		inp = str.decode(c.recv(4096))
		c.send(str.encode("Du skickade: " + inp))

# Beginning of execution

tConnections.start()
# TODO: modify running variable here.
tConnections.join()
print("Safe program exit.")

