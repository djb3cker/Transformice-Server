import random

class BulleManager:
	__bulles__ = []

	@staticmethod
	def get():
		return BulleManager.__bulles__

	@staticmethod
	def count():
		return len(BulleManager.__bulles__)
		
	@staticmethod
	def add(bulle_ip):
		BulleManager.__bulles__.append(bulle_ip)

	@staticmethod
	def remove(bulle_ip):
		BulleManager.__bulles__.remove(bulle_ip)

	@staticmethod
	def get_bulle(room):
		for bulle in BulleManager.__bulles__:
			if room in bulle.bulle_rooms:
				return bulle
		return random.choice(BulleManager.__bulles__)