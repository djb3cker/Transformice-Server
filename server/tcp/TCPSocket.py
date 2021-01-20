import socket
import threading
from utils import logging
from server.tcp.TCPClient import *

class TCPSocket(threading.Thread):
	def __init__(self, host, port):
		threading.Thread.__init__(self)

		self.__host__ = host
		self.__port__ = port
		self.__running__ = False
		self.__socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def bind(self):
		self.__socket__.bind((self.__host__, self.__port__))

	def listen(self, count):
		self.__socket__.listen(count)

	def run(self):
		self.__running__ = True

		while self.__running__:
			sock, address = self.__socket__.accept()

			client = TCPClient(sock, address)
			client.start()

			logging.debug("The client connection {} has been accepted.".format(
				address[0]
				)
			)