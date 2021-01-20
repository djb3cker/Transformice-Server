class BulleRoom:
	def __init__(self, bulle, room_name):
		self.bulle = bulle
		self.room_name = room_name

		self.players = []

		self.bulle.add_room(self)

	def join_player(self, player):
		self.players.append(player)