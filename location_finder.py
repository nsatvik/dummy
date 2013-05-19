import sys

class search_query:
	words = []
	stop_words = []
	locations = []
	def __init__(self, query):
		self.words = query.split(' ')
		print self.words
	
	def findLocations(self):
		print 'To be Implemented'
	
	def correct_location(self):
		print 'To be implemented'
	
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

def initLocations(locations_file_name):
	locations = []
	try:
		locations = open(locations_file_name).read().split('\n')
	except IOError:
		print locations_file_name,' : File not found'
		pass
	return locations

def main():
	if (len(sys.argv) < 3):
		print 'Usage python location_finder.py query_file_name locations_file_name'
		exit()
	

	queries = initSearchQueries(sys.argv[1])
	locations = initLocations(sys.argv[2])

	search_query.locations = locations #This is a class variable. This list will be initialized once and will be used by all quries.


	



if __name__=='__main__':
	main()
