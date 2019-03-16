import socket
import threading

# Setup the socket handling the HTTP requests.
s = socket.socket()
s.bind(("", 80))
s.listen(10)

# Global variables & constants
running = True
connections = []

# Thread functions
def fConnections():
	while running:
		try:
			c, addr = s.accept()
			tNewClientHandler = threading.Thread(None, fClientHandler, None, (c, addr), {})
			tNewClientHandler.daemon = True
			connections.append((c, addr))
			tNewClientHandler.start()
		except err:
			print("We had a failed connection: %s", err)
	for c, _ in connections:
		c.close()

def fClientHandler(c, addr):
	while running:
		inp = str.decode(c.recv(4096))
		c.send(str.encode("Du skickade: " + inp))

# Beginning of execution

# Connection thread:         reserved,  function,           name,       args, kwargs
tConnections = threading.Thread(None, fConnections, "Connections thread", (), {})
tConnections.start()
# TODO: modify running variable here.
tConnections.join()
print("Safe program exit.")

