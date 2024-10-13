import random

class RoomsManager:
	__bulles__ = []

	@staticmethod
	def get():
		return RoomsManager.__bulles__

	@staticmethod
	def count():
		return len(RoomsManager.__bulles__)
		
	@staticmethod
	def add(bulle_ip):
		RoomsManager.__bulles__.append(bulle_ip)

	@staticmethod
	def remove(bulle_ip):
		RoomsManager.__bulles__.remove(bulle_ip)

	@staticmethod
	def get_bulle(room):
		for bulle in RoomsManager.__bulles__:
			if room in bulle.bulle_rooms:
				return bulle
		return random.choice(RoomsManager.__bulles__)