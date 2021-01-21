import time

class JSONManager:
	__clients__ = []

	@staticmethod
	def add(client):
		JSONManager.__clients__.append(client)

	@staticmethod
	def delete(client):
		JSONManager.__clients__.remove(client)

	@staticmethod
	def check_all_clients_has_connected():
		while True:
			for client in JSONManager.__clients__:
				if int(time.time() - client.timer) > 30:
					client.close("The client {} ended the connection".format(
						client.address[0]
						)
					)
			time.sleep(5)