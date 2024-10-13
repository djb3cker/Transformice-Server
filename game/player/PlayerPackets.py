import zlib
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

	def enteredRoom(self, roomName):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(5)
		bytearray.writeUnsignedByte(21)
		bytearray.writeBoolean(False)
		bytearray.writeUTF(roomName)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def activeScreens(self):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(29)
		bytearray.writeUnsignedByte(1)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def showPlayerInMap(self):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(144)
		bytearray.writeUnsignedByte(1)
		bytearray.writeShort(len(self.player.room.players))
		for player in self.player.room.players.values():
			bytearray.writeUTF(player.nickname)
			bytearray.writeInt(player.code)
			bytearray.writeBoolean(player.round["shaman"])
			bytearray.writeBoolean(player.round["dead"])
			bytearray.writeShort(player.round["score"])
			bytearray.writeBoolean(player.round["cheese"])
			bytearray.writeShort(player.titleNumber)
			bytearray.writeByte(player.titleStars)
			bytearray.writeByte(player.gender)
			bytearray.writeUTF("")
			bytearray.writeUTF(player.playerLook)
			bytearray.writeBoolean(False)
			bytearray.writeInt(int(player.mouseColor, 16))
			bytearray.writeInt(int(player.shamanColor, 16))
			bytearray.writeInt(0)
			bytearray.writeInt(-1)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def newPlayerInRoom(self, nickname, code, isShaman, isDead, playerScore, hasCheese, titleNumber, titleStars, gender, playerLook, mouseColor, shamanColor):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(144)
		bytearray.writeUnsignedByte(2)
		bytearray.writeUTF(nickname)
		bytearray.writeInt(code)
		bytearray.writeBoolean(isShaman)
		bytearray.writeBoolean(isDead)
		bytearray.writeShort(playerScore)
		bytearray.writeBoolean(hasCheese)
		bytearray.writeShort(titleNumber)
		bytearray.writeByte(titleStars)
		bytearray.writeByte(gender)
		bytearray.writeUTF("")
		bytearray.writeUTF(playerLook)
		bytearray.writeBoolean(False)
		bytearray.writeInt(int(mouseColor, 16))
		bytearray.writeInt(int(shamanColor, 16))
		bytearray.writeInt(0)
		bytearray.writeInt(-1)
		bytearray.writeBoolean(False)
		bytearray.writeBoolean(True)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def showMap(self, mapCode, onlinePlayers, currentRound, mapXML, mapName, mapPerma, mapInverted):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(5)
		bytearray.writeUnsignedByte(2)
		bytearray.writeInt(mapCode)
		bytearray.writeShort(onlinePlayers)
		bytearray.writeUnsignedByte(currentRound)
		bytearray.writeShort(0)
		bytearray.writeUTF(mapXML)
		bytearray.writeUTF(mapName)
		bytearray.writeByte(mapPerma)
		bytearray.writeBoolean(mapInverted)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def showRoundTime(self, time):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(5)
		bytearray.writeUnsignedByte(22)
		bytearray.writeShort(time)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def lockMouseMoviment(self, enable):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(5)
		bytearray.writeUnsignedByte(10)
		bytearray.writeBoolean(enable)
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def mouseMoviemnt(self, playerCode, roundCode, droiteEnCours, gaucheEnCours, px, py, vx, vy, jump, jump_img, portal, isAngle, angle, vel_angle, loc_1):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(4)
		bytearray.writeUnsignedByte(4)
		bytearray.writeInt(playerCode)
		bytearray.writeInt(roundCode)
		bytearray.writeBoolean(droiteEnCours)
		bytearray.writeBoolean(gaucheEnCours)
		bytearray.writeInt(px)
		bytearray.writeInt(py)
		bytearray.writeUnsignedShort(vx)
		bytearray.writeUnsignedShort(vy)
		bytearray.writeBoolean(jump)
		bytearray.writeByte(jump_img)
		bytearray.writeByte(portal)
		if isAngle:
			bytearray.writeUnsignedShort(angle)
			bytearray.writeUnsignedShort(vel_angle)
			bytearray.writeBoolean(loc_1)
		for player in self.player.room.getAllPlayers():
			if player != self.player:
					player.tcp_client.send(bytearray.toByteArray(), True)

	def getCheese(self, playerCode, withCheese):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(144)
		bytearray.writeUnsignedByte(6)
		bytearray.writeInt(playerCode)
		bytearray.writeBoolean(withCheese)
		for player in self.player.room.getAllPlayers():
			if player != self.player:
					player.tcp_client.send(bytearray.toByteArray(), True)

	def enterHole(self, playerCode, score, place, timeTaken):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(8)
		bytearray.writeUnsignedByte(6)
		bytearray.writeByte(0)
		bytearray.writeInt(playerCode)
		bytearray.writeShort(score)
		bytearray.writeUnsignedByte(255 if place >= 255 else place)
		bytearray.writeUnsignedShort(65535 if timeTaken >= 65535 else timeTaken)
		for player in self.player.room.getAllPlayers():
			player.tcp_client.send(bytearray.toByteArray(), True)

	def playerDied(self, code, score):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(1)
		bytearray.writeUnsignedByte(1)
		bytearray.writeUTF(chr(1).join(map(str, ["".join(map(chr, [8, 5]))] + [code, score])))
		self.player.tcp_client.send(bytearray.toByteArray(), True)

	def playerDisconnected(self, code):
		bytearray = ByteArray()
		bytearray.writeUnsignedByte(1)
		bytearray.writeUnsignedByte(1)
		bytearray.writeUTF(chr(1).join(map(str, ["".join(map(chr, [8, 7]))] + [code])))
		self.player.tcp_client.send(bytearray.toByteArray(), True)