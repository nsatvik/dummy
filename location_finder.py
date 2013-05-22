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
				#print 'Length of Suggesstions = ',len(probable_locations)
				if len(probable_locations)==1:
					self.corrected_location=(self.locations[0][0],probable_locations[0])
					return
				max_prob = 0
				max_prob_loc = 'TBD'
				for prob_location in probable_locations:
					if freq_table[prob_location] > max_prob:
						max_prob = freq_table[prob_location]
						max_prob_loc = prob_location
					pass
					#Measure the distance of this word Correction Algo goes here!
				edit_distances = []
				min = sys.maxint
				edit_dist_loc = ''
				for loc in probable_locations:
					edit_distances.append(levenshtein(self.locations[0][1], loc))
					if edit_distances[-1]<min:
						min = edit_distances[-1]
						edit_dist_loc = loc
				
				self.corrected_location=(self.locations[0][0],max_prob_loc)
				#print self.corrected_location
				#Find maximum probability and minimum edits
				#set the current location to that.
				
				
		else:
			global_probability = 0
			global_most_probable = ''
			edit_dist_loc = ''
			edit_dist = sys.maxint
			edit_dist_index = -1
			index = -1
			for i in range(len(self.locations)):
				if self.locations[i][1] in list_of_locations:
					if self.check_neighbouring_words(i):
						self.corrected_location=(self.locations[i][0],self.locations[i][1])
						return
					else:
						continue
						
				location_keys = self.get_location_keys(self.locations[i][1],keys)
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
						#if freq_table[key]==1: #Can set a threshold here
						#	if self.check_neighbouring_words(i):
						#		self.update_surrounding_words(i)
							#return
					except ZeroDivisionError:
						pass 
				#print freq_table
				probable_locations = freq_table.keys() #Need to sort with descending order of probability
				max_prob = 0
				max_prob_loc = 'TBD'
				nums = len(probable_locations)
				if nums == 0:
					#print 'location discarded ', self.locations[i][1]
					continue
				elif nums == 1:
					edistance = levenshtein(self.locations[i][1], probable_locations[0])
					#print 'edistance = ',edistance
					if edistance < edit_dist:
						edit_dist = edistance
						edit_dist_loc = self.locations[i][1]
						edit_dist_index = i
						continue
				
				
				#print self.locations[i][1],' -> ',probable_locations
				#print freq_table
				for prob_location in probable_locations:
					if freq_table[prob_location] > max_prob:
						
						max_prob = freq_table[prob_location]
						max_prob_loc = prob_location
					pass
				edit_distances = []
				for loc in probable_locations:
					edit_distances.append(levenshtein(self.locations[i][1], loc))
					if edit_distances[-1] < edit_dist:
						edit_dist = edit_distances[-1]
						edit_dist_loc = loc
						edit_dist_index = i
						
				if max_prob > global_probability:
					global_probability = max_prob
					global_most_probable = max_prob_loc
					index = i
			if edit_dist <= 3 :
				self.corrected_location=(self.locations[edit_dist_index][0],edit_dist_loc)
			elif index == edit_dist_index:
				self.corrected_location=(self.locations[index][0],global_most_probable)
			else:
				self.corrected_location=(self.locations[index][0],global_most_probable)
					
		
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
	def check_neighbouring_words(self, index):
		loc = self.locations[index][0]
		pos = 0
		n = len(self.words)
		if loc < (n-1):
			try :
				if search_query.suceeding_words[self.words[loc+1]]:
					pos += 1
			except KeyError:
				pass
		if loc > 1:
			try:
				if search_query.preceeding_words[self.words[loc-1]]:
					pos += 1
			except KeyError:
				pass
		return pos
	def update_surrounding_words(self, index):
		n = len(self.words)
		#print 'Index = ',index,' n = ', n,'len(self.locations) = ',len(self.locations)
		if self.locations[index][0] < (n-1):
			try:
				search_query.suceeding_words[self.words[self.locations[index][0]+1]] += 1
			except KeyError:
				search_query.suceeding_words[self.words[self.locations[index][0]+1]] = 1
		if self.locations[index][0] > 1:
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
				output += '<loc>'+str(self.corrected_location[1])+'</loc>'
			else:
				output += self.words[i]
		return output	
			
def levenshtein(s1, s2):
	if len(s1)<len(s2):
		return levenshtein(s2, s1)
	
	if len(s2)==0:
		return len(s1)
	previous_row = xrange(len(s2)+1)
	for i,c1 in enumerate(s1):
		current_row = [i+1]
		for j,c2 in enumerate(s2):
			insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
			deletions = current_row[j] + 1       # than s
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row
	return previous_row[-1]
		
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
	keys=[(0,2),(0,3),(-3,-1),(-4,-1),(-2,-1)]
	hashmap = build_location_hashmap(list_of_locations,keys)
	
	
	
	for query in queries:
		query.findProbableLocations(list_of_words)
		query.correct_location(list_of_locations,hashmap,keys)
		print query.toString()
	


if __name__=='__main__':
	main()