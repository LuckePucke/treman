import socket
import threading

# Setup the socket handling the HTTP requests.
s = socket.socket()
s.bind(("", 80))
s.listen(10)

# Global variables & constants
running = True
clientHandlers = []

# Thread functions
def fConnections():
	while running:
		try:
			c, addr = s.accept()
			tNewClientHandler = threading.Thread(None, fClientHandler, None, (c, addr), {})
			clientHandlers.append(tNewClientHandler)
			tNewClientHandler.start()
		except err:
			print("We had a failed connection: %s", err)

def fClientHandler(c, addr):
	with c:
		while running:
			data = c.recv(4096)
			if not data:
				break
			c.send(str.encode( "Du skickade: " + bytes.decode(data) ))

# Beginning of execution

# Connection thread:         reserved,  function,           name,       args, kwargs
tConnections = threading.Thread(None, fConnections, "Connections thread", (), {})
tConnections.start()
input("Press enter to shutdown the server.")
tConnections.join()
print("Safe program exit.")

