from utils import logging

class BulleRoomsManager:
	__bulles__ = {}

	@staticmethod
	def count():
		return len(BulleRoomsManager.__bulles__)

	@staticmethod
	def join(bulle, room_name):
		if not bulle.bulle_ip in list(BulleRoomsManager.__bulles__):
			BulleRoomsManager.__bulles__[bulle.bulle_ip] = {}

		if room_name in BulleRoomsManager.__bulles__[bulle.bulle_ip]:
			bulle_room = BulleRoomsManager.__bulles__[bulle.bulle_ip][room_name]
		else:
			bulle_room = BulleRoom(bulle, room_name)
			BulleRoomsManager.__bulles__[bulle.bulle_ip][bulle_room] = bulle_room

			logging.info("New room {} with bulle: {}".format(
				bulle.bulle_ip,
				room_name
				)
			)

		return bulle_room 