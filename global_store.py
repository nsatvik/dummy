

class global_info:
	list_of_words = []
	list_of_locations = []

	def __init__(self):
		global_info.list_of_words = []
		global_info.list_of_locations = []
	def setLocations(self, locations):
		global_info.list_of_locations = locations
	
	def setWords(self, words):
		global_info.list_of_words = words
