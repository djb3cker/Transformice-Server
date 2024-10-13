class RoomsManager:
	__rooms = {}

	@staticmethod
	def rooms():
		return RoomsManager.__rooms

	@staticmethod
	def add(room, roomName):
		RoomsManager.__rooms[roomName] = room

	@staticmethod
	def remove(roomName):
		del RoomsManager.__rooms[roomName]