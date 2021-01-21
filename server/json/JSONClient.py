import threading
from utils import logging
from server.tcp.ByteArray import *
from server.managers.JSONManager import *

class JSONClient(threading.Thread):
	def __init__(self, socket, address):
		threading.Thread.__init__(self)

		self.socket = socket
		self.address = address

		self.connected = False

		self.errors_count = 0

		self.received_data = b""

	def run(self):
		self.open()
		self.dataProcess()

	def open(self):
		self.connected = True

		JSONManager.add(client)

	def close(self):
		if not self.connected:
			return

		self.connected = False

		JSONManager.delete(client)

	def dataProcess(self):
		while self.connected:
			try:
				data = self.socket.recv(8192)
			except:
				if self.errors_count >= 3:
					self.close("The client {} ended the connection".format(
						self.address)
					)
					break

				self.errors_count += 1
				continue

			if len(data) > 0:
				self.dataReceive(data)

		self.close()

	def send(self, data, encode=False):
		if not self.connected:
			return

		if not type(data) == bytes:
			data = data.encode()

		try:
			self.socket.sendall(self.encodeData(data) if encode else data)

			logging.debug("{} - send packet data: {}".format(
				self.address[0],
				repr(data)
				)
			)
		except:
			if self.errors_count >= 3:
				self.close("The client {} ended the connection".format(
					self.address[0]
					)
				)

			self.errors_count += 1
			self.send(data, encode)

	def encodeData(self, data):
		bytearray_encode = ByteArray()
		data_size = len(data)
		calc = data_size >> 7

		while calc != 0:
			bytearray_encode.writeByte(((data_size & 0x7F) | 0x80))
			data_size = calc
			calc = (calc >> 7)

		bytearray_encode.writeByte(data_size & 0x7F)
		bytearray_encode.writeBytes(data)
		return bytearray_encode.toByteArray()

	def dataReceive(self, data):
		self.received_data += data

		if len(self.received_data) < 1:
			return
		elif self.received_data == b"<policy-file-request/>\x00":
			self.received_data = b""
			self.send(b"<cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\" /></cross-domain-policy>")
			self.close()
		else:
			bytearray = ByteArray(self.received_data)

			x = 0
			length = 0

			byte1 = (bytearray.readUnsignedByte() & 0xFF)
			length = (length | ((byte1 & 0x7F) << (x * 7)))
			x += 1
			
			while (byte1 & 128) == 128 and x < 5:
				if not bytearray.bytesAvailable():
					return
				byte1 = (bytearray.readUnsignedByte() & 0xFF)
				length = (length | ((byte1 & 0x7F) << (x * 7)))
				x += 1

			length += 1

			if length == 0:
				self.received_data = b""
			elif length == bytearray.length():
				self.packetProcess(bytearray.readBytes(length))
				self.received_data = bytearray.toByteArray()
			elif length > bytearray.length():
				self.packetProcess(bytearray.readBytes(length))
				self.received_data = bytearray.toByteArray()

				if bytearray.length() > 1:
					self.dataReceive(b"")
			else:
				self.received_data = self.received_data

	def packetProcess(self, data):
		bytearray = ByteArray(data)

		packetid = bytearray.readByte()

		#if packetid != self.packetid:
		#	return

		self.packetid = (self.packetid + 1) % 100

		packetcode1 = bytearray.readUnsignedByte()
		packetcode2 = bytearray.readUnsignedByte()

		self.timer = time.time()

		logging.debug("{} - receive packet code: {} - {}, data {}".format(
			self.address[0],
			packetcode1,
			packetcode2,
			repr(bytearray.toByteArray())
			)
		)