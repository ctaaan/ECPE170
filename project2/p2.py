"""This is a Python-based English text to Pig-Latin converter. It reads the a file and creates a Pig-Latinized output text in a new file.

Rules of Pig Latin:
1. If a word starts with a consonant and a vowel, put the first letter of the word at the end of the word and add "ay."

2. If a word starts with two consonants move the two consonants to the end of the word and add "ay."

3. If a word starts with a vowel add the word "way" at the end of the word.

4. The output file must retain all of the punctuations used in the input text file. """

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=argparse.FileType('r'))
parser.add_argument('outputfile', type=argparse.FileType('w'))
args = parser.parse_args()

def main():
	x = args.inputfile.readline()
	# reads the first line of the input file
	while x:
	# keeps reading the next line
		y = x.split(' ')
		# splits the read line by spaces
		new = ''
		# new variable to store pig latinized words
		for n in range(len(y)):
			p = pigLatin(y[n])
			new += p
			# pig latinizes word by word and appends it to p
		args.outputfile.write(new)
		# writes pig latinized line into output file
		x = args.inputfile.readline()
	args.inputfile.close()
	
def single(word):
	# single character words don't need to be changed in any way, only need 'ay' or 'way' added depending on letter
	if word[0].isalnum() == False:
		final = word + ' '
	else:
		if word[0] == 'a' or word[0] == 'e' or word[0] == 'i' or word[0] == 'o' or word[0] == 'u':
			final = word + 'way' + ' '
		else:
			final = word + 'ay' + ' '
	return final		

def multiple(word):
	word0 = ''
	frontPunc = ''
	if word[0].isalnum() == False:
		if word[1].isalnum() == False:
			frontPunc = word[0] + word[1]
			word0 = word[2:]
		else:
			frontPunc = word[0]
			word0 = word[1:]
	else:
		word0 = word
	# checks for punctutation at the front of the word, removes it and stores it in a separate variable, and word0 becomes word without punctuation

	word1 = ''
	backPunc = ''
	if word0[-1].isalnum() == False:
		if word0[-2].isalnum() == False:
			backPunc = word0[-2] + word0[-1]
			word1 = word0[:-2]
		else:
			backPunc = word0[-1]
			word1 = word0[:-1]
	else:
		word1 = word0
	# checks for punctutation at the back of the word, removes it and stores it in a separate variable, and word1 becomes word without punctuation
	
	hasUpper = 0
	word2 = ''
	if word1[0].isupper():
		hasUpper = 1
		word2 = word1[0].lower() + word1[1:]
	else:
		word2 = word1
	# checks if first letter is capitalized, so the new letter can be recapitalized later, word2 becomes word with uncapitalized letter
	
	if word2[0] == 'a' or word2[0] == 'e' or word2[0] == 'i' or word2[0] == 'o' or word2[0] == 'u':
		word2 += 'way'
		# if first letter is a vowel, add 'way'
	
	elif word2[1] == 'a' or word2[1] == 'e' or word2[1] == 'i' or word2[1] == 'o' or word2[1] == 'u':
		word2 = word2[1:] + word2[0] + 'ay'
		# at this point first letter must be constanant, so checks if second letter is vowel, if so, moves first letter to end and adds 'ay'
	
	else:
		word2 = word2[2:] + word2[0] + word2[1] + 'ay'
		# if this else is reaches, it must mean first two letters are constanants, so moves first two to end and adds 'ay'
	
	if hasUpper == 1:
		# capitalizes first letter if it was originally capitalized
		final = word2[0].upper() + word2[1:]
	else:
		final = word2

	
	final = frontPunc + final + backPunc + ' '
	# adds punctuation at front and back of word back in
	return final
	
def pigLatin(word):
	# a word with one character is treated differently, so a different function is called
	if len(word) == 1:
		final = single(word)

	else:
		final = multiple(word)
	return final

if __name__ == "__main__":
	main()
