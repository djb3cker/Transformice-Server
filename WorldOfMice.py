import time
from utils import logging
from server.tcp.TCPSocket import *
from server.managers.TCPClientManager import *

__author__ = "b3ckerdev"
__license__ = "MIT License"

class WorldOfMice:
	__sockets__ = {}

	@staticmethod
	def run():
		logging.info("World of Mice - emulator (v1.{0} version by {1})".format(
			WorldOfMice.version(),
			__author__
			)
		)

		running_ports = []
		for port_number in [11801, 12801, 13801, 14801]:
			WorldOfMice.__sockets__[port_number] = TCPSocket("0.0.0.0", port_number)
			WorldOfMice.__sockets__[port_number].bind()
			WorldOfMice.__sockets__[port_number].listen(100000)
			running_ports.append(port_number)
			
		logging.debug("The following ports was opened for the server: {}".format(
			running_ports
			)
		)

		for sock in WorldOfMice.__sockets__.values():
			sock.start()

		logging.info("All sockets were opened on dedicated threads.")

		thread = threading.Thread(target=TCPClientManager.check_all_clients_has_connected, args=())
		thread.start()
		thread.join()

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
	WorldOfMice.run()