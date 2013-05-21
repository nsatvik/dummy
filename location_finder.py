import sys

class search_query:
	
	words = []
	locations = []
	def __init__(self, query):
		self.words = query.split(' ')
		self.locations = []
	
	def findProbableLocations(self,list_of_words):
		for i in range(len(self.words)):
			word = self.words[i].lower()
			
			if word in list_of_words:
				print word,'in dictionary'
				continue
			self.locations.append((i,word))
			
		
	
	def correct_location(self,list_of_locations,hashmap):
		# 1 If it is found in the list_of_locations, check the surrounding words update that list
		# 2 IF not found Check in the hashmap and get the list of probable places. Apply Edit-distance Algo and find the most similar one.
		#   and update the surrounding words
		# 3 Add the location 
		l = len(self.locations)
		if l > 1: #More that one location in the query! :(
			pass#Check in the neighbouring words list and take a decision for each word...
		if l==1:
			#This is the location and update the neighbouring words list.
			pass
		keys = self.get_location_keys()
		
		#With these keys find a probable list of locations
		#If more than 1 locations are mapped use edit-distance or someother spell check and map it to the closest algo :D
		
	
	def toString(self):
		print 'Coming Soon'
		
def initSearchQueries(query_file_name):
	lines = []
	queries = []
	try:
		f = open(query_file_name)
		lines = f.read().split('\n')
		del lines[-1] #delete the blank string at the end.
	except IOError:
		print query_file_name,': File Not found'
		pass
	for line in lines:
		query = search_query(line)
		queries.append(query)
	return queries

def file_reader(file_name):
	words = {}
	try:
		words = open(file_name).read().split('\n')
	except IOError:
		print file_name,' : File not found'
		pass
	return words

def build_location_hashmap(list_of_locations):
	map = {}
	
	for location in list_of_locations:
		try:
			map[location[:3]].add(location)
		except KeyError:
			map[location[:3]] = {location}
		try:
			map[location[-4:]].add(location)
		except KeyError:
			map[location[-4:]] = {location}
		except IndexError:
			pass
		try:
			map[location[3:]].add(location)
		except KeyError:
			map[location[3:]] = {location}
		try:
			map[location[:2]].add(location)
		except KeyError:
			map[location[:2]] = {location}
		try:
			map[location[-2:]].add(location)
		except KeyError:
			map[location[-2:]] = {location}
def main():
	if (len(sys.argv) < 3):
		print 'Usage python location_finder.py query_file_name locations_file_name'
		exit()
	

	queries = initSearchQueries(sys.argv[1])
	locations = set(file_reader(sys.argv[2]))

	list_of_locations = locations#This is a class variable. This list will be initialized once and will be used by all quries.
	list_of_words = set(file_reader('list_of_words')) - locations
	hashmap = build_location_hashmap(list_of_locations)
	print len(list_of_words)
	
	for query in queries:
		query.findProbableLocations(list_of_words)



if __name__=='__main__':
	main()