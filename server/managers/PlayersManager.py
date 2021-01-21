class PlayersManager:
	__players__ = []

	@staticmethod
	def add(player):
		PlayersManager.__players__.append(player)

	@staticmethod
	def delete(player):
		PlayersManager.__players__.remove(player)

	@staticmethod
	def get():
		return PlayersManager.__players__

	@staticmethod
	def connected_count():
		return len(PlayersManager.__players__)