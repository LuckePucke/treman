import socket
import threading

# Setup the socket handling the HTTP requests.
s = socket.socket()
s.bind(("", 80))
s.listen(10)

# Global variables & constants
running = True
connections = {}

# Thread functions
def fConnections():
	# Handles all connections.
	# Inserts the connection into the connections directory with the address as the key.
	while True:
		try:
			# First we accept the new connection
			c, addr = s.accept()
			connections.update(addr = c)
			tNewClientHandler = threading.Thread(None, fClientHandler, None, (c, addr), {})
			tNewClientHandler.start()
		except err:
			print("We had a failed connection: %s", err)

def fClientHandler(c, addr):
	with c:
		while running:
			data = c.recv(4096)
			if not data:
				del connections[addr]
				break
			c.send(str.encode( "Du skickade: " + bytes.decode(data) ))

# Beginning of execution

# Connection thread:         reserved,  function,           name,       args, kwargs
tConnections = threading.Thread(None, fConnections, "Connections thread", (), {})
tConnections.daemon = True
tConnections.start()
_ = input("Press enter to shutdown the server.")
for addr, c in connections.items():
	c.close()
print("Safe program exit.")

