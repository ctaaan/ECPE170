import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, required=True)
parser.add_argument('--nway', type=str, required=False)
parser.add_argument('--cache_size', type=int, required=True)
parser.add_argument('--block_size', type=int, required=True)
parser.add_argument('--memfile', type=argparse.FileType('r'), required=True)
args = parser.parse_args()

f = open("cache.txt", "w")
# creates output file

hex4 = { '0' : '0000', '1' : '0001', '2' : '0010', '3' : '0011', '4' : '0100', '5' : '0101', '6' : '0110', '7' : '0111', '8' : '1000', '9' : '1001', 'a' : '1010', 'b' : '1011', 'c' : '1100', 'd' : '1101', 'e' : '1110', 'f' : '1111' }
# dictionary for hex conversion

def main():
	global hitCount
	hitCount = 0
	# hit counter for hit rate calculation
	count = 0
	# counter for hit rate calculation
	first = True
	# variable to makeCache on first read
	x = args.memfile.readline()
	# reads the first line of the input file
	while x:
	# keeps reading the next line
		count += 1
		# counter increment
		if first == True:
			makeCache(x)
			first = False
			# if first read, make Cache, and make first False to skip over this in future
		choose(x)
		# decides path based on type
		x = args.memfile.readline()
	f.write('\nHit Rate: ')
	f.write(str(100*(hitCount/count)))
	f.write('% ')
	# hit rate calc and write
	args.memfile.close()
	# closes file when no more lines to read
	
def choose(x):
	if (args.type == 'd'):
		indexBits = int(math.log2(int(args.cache_size) / int(args.block_size)))
		# number of index bits
		map(x, indexBits)
	elif (args.type == 's'):
		indexBits = int(math.log2(int(args.cache_size) / (int(args.block_size) * int(args.nway))))
		# number of index bits
		map(x, indexBits)
	else:
		print('Invalid type')
		quit()
		# other letter (invalid)
		
def makeCache(x):
	global validList
	validList = []
	# list for valid bit
	global tagList
	tagList = []
	# list for tag bits
	

	if (args.type == 'd'):
		indexBits = int(math.log2(int(args.cache_size) / int(args.block_size)))
		# number of index bits
		numSpots = 2**indexBits
		# number of slots in cache
		for n in range(numSpots):
			validList.append('')
			tagList.append('')
			# creating list with correct numner of spots, all with '' as starting string
	elif (args.type == 's'):
		indexBits = int(math.log2(int(args.cache_size) / (int(args.block_size) * int(args.nway))))
		# number of index bits
		numSpots = (2**indexBits) * int(args.nway)
		# number of spots in cache, where the next 'way' starts after the previous one ends
		for n in range(numSpots):
			validList.append('')
			tagList.append('')
			# creating list with correct numner of spots, all with '' as starting string
			
	
def hitOrMiss(decIndex, tag, isAligned, indexBits):
	global validList
	global tagList
	global RU
	global hitCount
	
	HM = ''
	# variable to return hit or miss
	hit = False
	# variable for second check
	empty = False
	# variable for third check
	if (args.type == 'd'):
		if validList[decIndex] == '':
			HM = 'MISS'
			validList[decIndex] = '1'
			tagList[decIndex] = tag
			# if no valid bit, cache slot is empty, so return miss and update cache
		elif validList[decIndex] == '1':
			if tagList[decIndex] == tag:
				HM = 'HIT'
				hitCount += 1
				# if tag bits match, return hit and increment hit counter
			else:
				HM = 'MISS'
				tagList[decIndex] = tag
				# if tag bits don't match, return miss and update cache
				
	elif (args.type == 's'):
		for n in range(int(args.nway)):
			if validList[(n*(2**indexBits))+decIndex] == '1':
				if tagList[(n*(2**indexBits))+decIndex] == tag:
					hit = True
					RU = n
					break
					# checks if theres a hit at all by checking each way at index, exits if finds hit, updates recently used
					
		if hit == True:
			HM = 'HIT'
			hitCount += 1
			# if hit, return hit and increment hit counter
		else:
			for n in range(int(args.nway)):
				if validList[(n*(2**indexBits))+decIndex] == '':
					empty = True
					validList[(n*(2**indexBits))+decIndex] = '1'
					tagList[(n*(2**indexBits))+decIndex] = tag
					RU = n
					break
					# if no hit, finds an empty cache slot and puts tag there, updates recently used
			
			if empty == True:
				HM = 'MISS'
				# updates miss
			else:
				for n in range(int(args.nway)):
					if n != RU:
						validList[(n*(2**indexBits))+decIndex] = '1'
						tagList[(n*(2**indexBits))+decIndex] = tag
						RU = n
						break
						# if no hit and no empty slots, finds and empty slot that was not the recently used and puts it there, updates recently used
				HM = 'MISS'
						
	if isAligned == False:
		HM = 'U'
		# returns U instead of hit/miss if unaligned
		
	return HM
	

def map(x, indexBits):

	memAdd = ''
	# variable for memory address
	
	offsetBits = int(math.log2(int(args.block_size)))
	# number of bits taking away
	tagSlice = 32 - (offsetBits + indexBits)
	# num where slicing

	decNum = int(x, 16)
	if (decNum % 4) == 0:
		isAligned = True
	else:
		isAligned = False
	# checking if aligned
	
	for n in range(8):
		string = str(x[n]).strip()
		memAdd += hex4[string]
		# converts each number into 4 bit binary translation using dictionary and appends string
	
	tag = memAdd[0:tagSlice]
	# tag bits
	index = memAdd[tagSlice:(tagSlice + indexBits)]
	# index bits
	decIndex = int(index, 2)
	# converts index to decimal for list accessing
		
	f.write(x.strip())
	f.write(" | ")
	f.write(tag)
	f.write(" | ")
	f.write(index)
	f.write(" | ")
	f.write(hitOrMiss(decIndex, tag, isAligned, indexBits))
	f.write('\n')
	# writes output
	

if __name__ == "__main__":
	main()
