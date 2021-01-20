class languages:
	__list__ = {}
	__list__[0] = "EN"
	__list__[1] = "FR"
	__list__[2] = "RU"
	__list__[3] = "BR"
	__list__[4] = "ES"
	__list__[5] = "CN"
	__list__[6] = "TR"
	__list__[7] = "VK"
	__list__[8] = "PL"
	__list__[9] = "HU"
	__list__[10] = "NL"
	__list__[11] = "RO"
	__list__[12] = "ID"
	__list__[13] = "DE"
	__list__[14] = "E2"
	__list__[15] = "AR"
	__list__[16] = "PH"
	__list__[17] = "LT"
	__list__[18] = "JP"
	__list__[19] = "CH"
	__list__[20] = "FI"
	__list__[21] = "CZ"
	__list__[22] = "SK"
	__list__[23] = "HR"
	__list__[24] = "BU"
	__list__[25] = "LV"
	__list__[26] = "HE"
	__list__[27] = "IT"
	__list__[29] = "ET"
	__list__[30] = "AZ"
	__list__[31] = "PT"

	@staticmethod
	def get():
		return languages.__list__

	@staticmethod
	def find_by_id(id):
		return languages.__list__[id] if (id in list(languages.__list__)) else None

	@staticmethod
	def checkExistLangueStr(langueStr):
		for id, langue in languages.__list__.items():
			if langue.lower() == langueStr.lower():
				return True
		return False

	@staticmethod
	def getLangue(langueByte):
		return languages.__list__[langueByte]

	@staticmethod
	def getLangueByName(langue):
		for langueID, l in languages.__list__.items():
			if l.lower() == langue.lower():
				return langueID
		return 0