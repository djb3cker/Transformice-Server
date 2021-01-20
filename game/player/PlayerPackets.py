from server.tcp.ByteArray import *

class PlayerPackets:
	def __init__(self, player):
		self.player = player

	def identification(self, id, nickname, timestamp, language, code, guest=False, privs=[]):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(26)
		bytearray.writeUnsignedByte(2)
		bytearray.writeInt(id)
		bytearray.writeUTF(nickname)
		bytearray.writeInt(timestamp)
		bytearray.writeByte(language)
		bytearray.writeInt(code)
		bytearray.writeBoolean(not guest)
		bytearray.writeByte(len(privs))
		for priv in privs:
			bytearray.writeByte(priv)
		bytearray.writeBoolean(True)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def bulle(host):
		pass