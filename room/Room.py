import random, threading, time
from utils import logging
from room.RoomsManager import *

class Room:
	def __init__(self, roomName):
		self.roomName = roomName

		self.players = {}

		self.map = {
			"time" : 120,
			"current_round" : 0,
			"map": 900,
			"inverted" : False,
			"xml": "",
			"by": "",
			"place": 0,
			"gameStartTimeMillis": 0
		}

		self.autoRespawn = False

		self.vanillaMaps = [31, 41, 42, 55, 59, 60, 62, 89, 92, 99, 114, 144, 145, 146, 147, 148, 104]

		self.newRoundTime = None

		RoomsManager.add(self, roomName)

		logging.debug("New room created: {}".format(
			self.roomName
			)
		)

	def getAllPlayers(self):
		players = []
		for key in self.players.copy().keys():
			if not self.players[key]:
				del self.players[key]
			else:
				players.append(self.players[key])
		return players

	def addPlayer(self, player):
		self.players[player.nickname] = player

		player.player_packets.enteredRoom(self.roomName)
		player.player_packets.activeScreens()

		if len(self.players) < 4:
			self.newRound()
		else:
			for player2 in self.getAllPlayers():
				player2.player_packets.newPlayerInRoom(player.nickname, player.code, player.round["shaman"], player.round["dead"], player.round["score"], player.round["cheese"], player.titleNumber, player.titleStars, player.gender, player.playerLook, player.mouseColor, player.shamanColor)

			player.player_packets.showMap(self.map["map"], len(self.players), self.map["current_round"], self.map["xml"], self.map["by"], self.map["inverted"], self.map["inverted"])
			player.player_packets.showRoundTime(self.map["time"])
			player.player_packets.lockMouseMoviment(player.round["dead"])

	def removePlayer(self, player):
		player.round["dead"] = True
		player.round["score"] = 0

		del self.players[player.nickname]

		if len(self.players) == 0:
			self.newRoundTime.cancel()

			RoomsManager.remove(self.roomName)

			logging.debug("New room deleted: {}".format(
				self.roomName
				)
			)
		else:
			for player2 in self.getAllPlayers():
				player2.player_packets.playerDisconnected(player.code)

	def checkAllDead(self):
		dead = True
		for player in self.getAllPlayers():
			if not player.round["dead"]:
				dead = False
				break
		return dead

	def newRound(self):
		if self.newRoundTime != None:
			self.newRoundTime.cancel()

		if len(self.players) == 0:
			return

		self.map["current_round"] += (self.map["current_round"] + 1) % 127

		logging.debug("New round on room: {} ({})".format(
			self.roomName,
			self.map["current_round"]
			)
		)

		#self.map["map"] = random.choice(self.vanillaMaps)
		self.map["place"] = 0
		self.map["gameStartTimeMillis"] = time.time()

		for player in self.getAllPlayers():
			player.round["cheese"] = False
			player.round["dead"] = False

		for player in self.getAllPlayers():
			player.player_packets.showMap(self.map["map"], len(self.players), self.map["current_round"], self.map["xml"], self.map["by"], self.map["inverted"], self.map["inverted"])
			player.player_packets.showRoundTime(self.map["time"])
			player.player_packets.showPlayerInMap()
			player.player_packets.lockMouseMoviment(player.round["dead"])

		self.newRoundTime = threading.Timer(self.map["time"], self.newRound)
		self.newRoundTime.start()