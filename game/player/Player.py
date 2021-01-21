from game.player.PlayerPackets import *
from server.managers.BulleManager import *
from server.managers.BulleRoomsManager import *

class Player:
	def __init__(self, tcp_client):
		self.tcp_client = tcp_client

		self.player_packets = PlayerPackets(self)

		self.connection_time = 0

		self.community = {
			"id": 0,
			"str": "en"
		}

		self.captcha = {
			"letters": "",
			"data": b""
		}

		self.id = 0
		self.code = 0

		self.nickname = ""
		self.privilege = 0

		self.logged = False

		self.bulle_room = None

	def identification(self, nickname):
		self.nickname = nickname

		self.player_packets.identification(self.id, self.nickname, 0, self.community["id"], self.code, True, [])

	def join_room(self, room):
		if self.bulle_room != None:
			self.bulle_room.leave(self)
			
		if BulleManager.count() > 0:
			bulle = BulleManager.get_bulle(room)

			self.bulle_room = BulleRoomsManager.join(bulle, room)

			print(self.bulle_room)