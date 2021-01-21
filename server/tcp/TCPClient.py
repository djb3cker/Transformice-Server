import time
import threading
from transformice import *
from utils import logging
from utils.languages import *
from server.tcp.ByteArray import *
from game.player.Player import *
from server.managers.CaptchaManager import *
from server.managers.TCPClientManager import *
from server.managers.PlayersManager import *

class TCPClient(threading.Thread):
	def __init__(self, socket, address):
		threading.Thread.__init__(self)
		self.socket = socket
		self.address = address
		self.connected = False
		self.errors_count = 0
		self.timer = time.time()
		self.received_data = b""
		self.packetid = 0
		self.player = None

	def run(self):
		self.open()
		self.dataProcess()

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

	def open(self):
		self.connected = True

		TCPClientManager.add(self)

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

	def close(self, reason=""):
		if not self.connected:
			return

		if self.player != None and self.player.logged:
			PlayersManager.delete(self.player)

		self.connected = False

		self.socket.close()

		TCPClientManager.delete(self)

		if reason != "":
			logging.debug("The client connection {} has been closed ({}).".format(
				self.address[0],
				reason
				)
			)
		else:
			logging.debug("The client connection {} has been closed.".format(
				self.address[0]
				)
			)

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

		if packetcode1 == 8:
			if packetcode2 == 2:
				# community
				id = bytearray.readByte()
				go = bytearray.readByte()

				find_result = languages.find_by_id(id)

				if find_result != None:
					self.player.community["id"] = id
					self.player.community["str"] = find_result;
					
					logging.debug("{} -> community -> {}".format(
						self.address[0],
						find_result
						)
					)
				return

		elif packetcode1 == 26:
			if packetcode2 == 8:
				if self.player != None and self.player.logged:
					return

				# auth login
				nickname = bytearray.readUTF().capitalize()
				sha256 = bytearray.readUTF()
				url = bytearray.readUTF()
				room = bytearray.readUTF()
				xor = bytearray.readInt()
				data_key = bytearray.readByte()

				if len(nickname) == 0 or len(sha256) == 0:
					self.player.identification(nickname)
					self.player.join_room(room)

			elif packetcode2 == 20:
				if self.player != None and self.player.logged:
					return

				self.player.captcha = CaptchaManager.captcha()

				print(self.player.captcha)
				return
				
		elif packetcode1 == 28:
			if packetcode2 == 1:
				if self.player != None and self.player.logged:
					return

				# handshake
				version = bytearray.readShort()
				key = bytearray.readUTF()
				standType = bytearray.readUTF()
				traceI = bytearray.readUTF()
				intTyp = bytearray.readInt()
				strV = bytearray.readUTF()
				server_string = bytearray.readUTF()
				window = bytearray.readUTF()
				t = bytearray.readInt()
				y = bytearray.readInt()
				string = bytearray.readUTF()

				if version != Transformice.version():
					self.close()
				elif key != Transformice.key():
					self.close()
				else:
					self.player = Player(self)
					self.player.version = version
					self.player.key = key
					self.player.connection_time = Transformice.time()

					PlayersManager.add(self.player)

					logging.debug("The connection to the game requested by {} has been accepted.".format(
						self.address[0]
						)
					)

					self.send(ByteArray().writeUnsignedByte(26).writeUnsignedByte(3).writeInt(0).writeUTF("pt").writeUTF("pt").writeInt(0).writeBoolean(False).toByteArray(), True)
					self.send(ByteArray().writeUnsignedByte(20).writeUnsignedByte(4).writeBytes(b'\x00\x00').toByteArray(), True)
					self.send(ByteArray().writeUnsignedByte(16).writeUnsignedByte(9).writeBytes(b'\x014\x01\x00').toByteArray(), True)

				return

			elif packetcode2 == 17:
				if self.player.logged:
					return

				language = bytearray.readUTF()
				system = bytearray.readUTF()
				version = bytearray.readUTF()
				pod = bytearray.readByte()
				return