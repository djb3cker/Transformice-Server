import time

class TCPClientManager:
	__clients__ = []

	@staticmethod
	def add(address):
		TCPClientManager.__clients__.append(address)

	@staticmethod
	def delete(address):
		TCPClientManager.__clients__.remove(address)

	@staticmethod
	def count():
		return len(TCPClientManager.__clients__)

	@staticmethod
	def check_all_clients_has_connected():
		while True:
			for client in TCPClientManager.__clients__:
				if int(time.time() - client.timer) > 30:
					client.close("The client {} ended the connection".format(
						client.address[0]
						)
					)
			time.sleep(5)