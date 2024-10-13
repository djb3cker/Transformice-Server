import random, time
from game.player.PlayerPackets import *
from room.RoomsManager import *
from room.Room import *

class Player:
	def __init__(self, tcp_client):
		self.tcp_client = tcp_client

		self.player_packets = PlayerPackets(self)

		self.id = 0
		self.code = random.randint(0, 1000000)
		self.connection_time = time.time()

		self.privilege = 0
		self.gender = 0
		self.titleNumber = 0
		self.titleStars = 0
		self.posX = 0
		self.posY = 0
		self.velX = 0
		self.velY = 0
		self.playerStartTimeMillis = 0

		self.nickname = ""
		self.playerLook = "1;0,0,0,0,0,0,0,0,0,0,0"
		self.mouseColor = "78583a"
		self.shamanColor = "95d9d6"

		self.logged = False
		self.isAfk = False
		self.isMovingRight = False
		self.isMovingLeft = False
		self.isJumping = False

		self.community = {
			"id": 0,
			"str": "en"
		}

		self.playerInfo = {
			"language": "",
			"system": "",
			"version": "",
			"pod": 0
		}

		self.round = {
			"dead" : True,
			"cheese" : False,
			"shaman" : False,
			"score" : 0
		}

		self.room = None

		self.lastAfkTime = time.time()

	def identification(self, nickname):
		self.nickname = nickname

		self.player_packets.identification(self.id, self.nickname, 0, self.community["id"], self.code, True, [])

	def join_room(self, roomName):
		if self.room != None:
			self.leaveRoom()
		
		roomName = "{}-{}".format(self.community["str"], roomName)
		roomName = roomName.replace("<", "&lt;")

		if roomName in RoomsManager.rooms():
			self.room = RoomsManager.rooms()[roomName]
		else:
			self.room = Room(roomName)

		self.room.addPlayer(self)

	def leaveRoom(self):
		self.room.removePlayer(self)

