class Bulle:
	def __init__(self, bulle_ip):
		self.bulle_ip = bulle_ip

		self.bulle_rooms = []

	def add_room(self, bulle_room):
		self.bulle_rooms.append(bulle_room)