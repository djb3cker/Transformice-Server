import time
from utils import logging
from server.tcp.TCPSocket import *
from server.json.JSONServer import *
from server.managers.TCPClientManager import *
from server.managers.JSONManager import *

__author__ = "b3ckerdev"
__license__ = "MIT License"

class Transformice:
	__sockets__ = {}

	@staticmethod
	def run():
		logging.info("Transformice emulator (v1.{0} version by {1})".format(
			Transformice.version(),
			__author__
			)
		)

		running_ports = []
		for port_number in [11801, 12801, 13801, 14801]:
			Transformice.__sockets__[port_number] = TCPSocket("0.0.0.0", port_number)
			Transformice.__sockets__[port_number].bind()
			Transformice.__sockets__[port_number].listen(500000)
			running_ports.append(port_number)
			
		logging.debug("The following ports was opened for the server: {}".format(
			running_ports
			)
		)

		for sock in Transformice.__sockets__.values():
			sock.start()

		logging.info("All sockets were opened on dedicated threads.")

		json_server = JSONServer("0.0.0.0", 8010)
		json_server.bind()
		json_server.listen(500000)
		json_server.start()

		thread = threading.Thread(target=TCPClientManager.check_all_clients_has_connected, args=())
		thread.start()

		thread = threading.Thread(target=JSONManager.check_all_clients_has_connected, args=())
		thread.start()

		print("\n")

	@staticmethod
	def version():
		return 584

	@staticmethod
	def key():
		return "dlIsYVC"

	@staticmethod
	def time():
		return time.time()

if __name__ == "__main__":
	Transformice.run()