import sys

class search_query:
	preceeding_words = {}
	suceeding_words = {}  
	words = []
	locations = []
	corrected_location = (0,'') #Index and spelling of the correct location.
	def __init__(self, query):
		self.words = query.split(' ')
		self.locations = []
		self.corrected_location = (0,'Correct Spelling of the location')
		search_query.preceeding_words = {}
		search_query.succeeding_words = {}
	
	def findProbableLocations(self,list_of_words):
		for i in range(len(self.words)):
			word = self.words[i].lower()
			
			if word in list_of_words:
				continue
			self.locations.append((i,word))
		#print self.locations
		
	
	def correct_location(self,list_of_locations,hashmap,keys):
		# 1 If it is found in the list_of_locations, check the surrounding words update that list
		# 2 IF not found Check in the hashmap and get the list of probable places. Apply Edit-distance Algo and find the most similar one.
		#   and update the surrounding words
		# 3 Add the location 
		l = len(self.locations)
		n = len(self.words)
		if l==1:
			if self.locations[0][1] in list_of_locations: #Can be changed to Probability Model 
				self.update_surrounding_words(0)
				self.corrected_location = (self.locations[0][0],self.locations[0][1])
				return
			else:
				location_keys = self.get_location_keys(self.locations[0][1],keys)
				freq_table = {}
				for key in location_keys:
					loc = ''
					try:
						locs = hashmap[key]
						for loc in locs:
							try:
								freq_table[loc] += 1
							except KeyError:
								#print 'caught '
								freq_table[loc] = 1
					except KeyError:
						#print 'Key Error if 1'
						pass
					except ValueError:
						#print 'Value Error if 1'
						pass #Key not in the hashmap.. Figure a way out
				
				total = 0
				for value in freq_table.values():
						total += value
				for key in freq_table.keys():
					try:
						freq_table[key] = float(freq_table[key])/float(total)
						if freq_table[key]==1: #Can set a threshold here
							self.update_surrounding_words(0)
							#return
					except ZeroDivisionError:
						pass 
				#print freq_table
				probable_locations = freq_table.keys() #Need to sort with descending order of probability
				max_prob = 0
				max_prob_loc = 'TBD'
				for prob_location in probable_locations:
					if freq_table[prob_location] > max_prob:
						max_prob = freq_table[prob_location]
						max_prob_loc = prob_location
					pass
					#Measure the distance of this word Correction Algo goes here!
				self.corrected_location=(self.locations[0][0],max_prob_loc)
				#print self.corrected_location
				#Find maximum probability and minimum edits
				#set the current location to that.
				
				
		else:
			for location in self.locations:
				if location[1] in list_of_locations:
					pass
		
		#With these keys find a probable list of locations
		#If more than 1 locations are mapped use edit-distance or someother spell check and map it to the closest algo :D
		
	def get_location_keys(self,location, keys):
		k = []
		for key in keys:
			if key[1]==-1:
				k.append(location[key[0]:])
			else:
				k.append(location[key[0]:key[1]])
		return k
				
	def update_surrounding_words(self, index):
		n = len(self.words)
		#print 'Index = ',index,' n = ', n,'len(self.locations) = ',len(self.locations)
		if self.locations[0][0] < (n-1):
			try:
				search_query.suceeding_words[self.words[self.locations[index][0]+1]] += 1
			except KeyError:
				search_query.suceeding_words[self.words[self.locations[index][0]+1]] = 1
		if self.locations[0][0] > 1:
			try:
				search_query.preceeding_words[(self.words[self.locations[index][0]-1])] += 1
			except KeyError:
				search_query.preceeding_words[(self.words[self.locations[index][0]-1])] = 1
		
	def toString(self):
		output = ''
		for i in range(len(self.words)):
			if len(output)>0:
				output += ' '
			if i==self.corrected_location[0]:				
				output += '<loc>'+self.corrected_location[1]+'</loc>'
			else:
				output += self.words[i]
		return output	
			
				
		
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

def build_location_hashmap(list_of_locations, keys):
	map = {}
	
	for location in list_of_locations:
		for key in keys:
			try:
				if key[1] == -1:
					map[location[key[0]:]].add(location)
				else:
					map[location[key[0]:key[1]]].add(location)
			except KeyError:
				if key[1]==-1:
					map[location[key[0]:]] = {location}
				else:
					map[location[key[0]:key[1]]] = {location}		
	return map
def main():
	if (len(sys.argv) < 3):
		print 'Usage python location_finder.py query_file_name locations_file_name'
		exit()
	

	queries = initSearchQueries(sys.argv[1])
	locations = set([x.lower() for x in file_reader(sys.argv[2])])

	list_of_locations = locations#This is a class variable. This list will be initialized once and will be used by all quries.
	list_of_words = set(file_reader('list_of_words')) - locations
	keys=[(0,2),(0,3),(-3,-1),(-4,-1)]
	hashmap = build_location_hashmap(list_of_locations,keys)
	
	
	
	for query in queries:
		query.findProbableLocations(list_of_words)
		query.correct_location(list_of_locations,hashmap,keys)
		print query.toString()



if __name__=='__main__':
	main()