import socket
import threading

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
	while True:
		try:
			# First we accept the new connection
			c, addr = s.accept()
			connections.update(connectionCounter = c)
			tNewClientHandler = threading.Thread(None, fClientHandler, None, (connectionCounter, c, addr), {})
			tNewClientHandler.start()
			connectionCounter += 1
		except err:
			print("We had a failed connection: %s", err)

def fClientHandler(connectionID, c, addr):
	with c:
		while running:
			data = c.recv(4096)
			if not data:
				del connections[connectionID]
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

