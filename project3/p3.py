import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=argparse.FileType('r'))
args = parser.parse_args()

f = open("out_code.txt", "w")
# creates output file

regNum = {"$0" : 0, "$1" : 1, "$2" : 2, "$3": 3, "$4" : 4, "$5" : 5, "$6" : 6, "$7" : 7, "$8" : 8, "$9" : 9, "$10" : 10, "$11": 11, "$12" : 12, "$13" : 13, "$14" : 14, "$15" : 15, "$16" : 16, "$17" : 17, "$18" : 18, "$19": 19, "$20" : 20, "$21" : 21, "$22" : 22, "$23" : 23, "$24" : 24, "$25" : 25, "$26" : 26, "$27": 27, "$28" : 28, "$29" : 29, "$30" : 30, "$31" : 31, "$32" : 32, "$33" : 33, "$34" : 34, "$35" : 35, "$36" : 36, "$37" : 37, "$38" : 38, "$39" : 39, "$40" : 40, "$41" : 41, "$42" : 42, "$43" : 43, "$44" : 44, "$45" : 45, "$46" : 46, "$47" : 47, "$48" : 48, "$49": 49, "$50" : 50, "$51" : 51, "$52" : 52, "$53" : 53, "$54" : 54, "$55" : 55, "$56" : 56, "$57" : 57, "$58" : 58, "$59": 59, "$60" : 60, "$61" : 61, "$62" : 62, "$63" : 63, "1" : 1, "2" : 2, "3": 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "11": 11, "12" : 12, "13" : 13, "14" : 14, "15" : 15, "16" : 16, "17" : 17, "18" : 18, "19": 19, "20" : 20, "21" : 21, "22" : 22, "23" : 23, "24" : 24, "25" : 25, "26" : 26, "27": 27, "28" : 28, "29" : 29, "30" : 30, "31" : 31, "32" : 32, "33" : 33, "34" : 34, "35" : 35, "36" : 36, "37" : 37, "38" : 38, "39" : 39, "40" : 40, "41" : 41, "42" : 42, "43" : 43, "44" : 44, "45" : 45, "46" : 46, "47" : 47, "48" : 48, "49": 49, "50" : 50, "51" : 51, "52" : 52, "53" : 53, "54" : 54, "55" : 55, "56" : 56, "57" : 57, "58" : 58, "59": 59, "60" : 60, "61" : 61, "62" : 62, "63" : 63, "$zero" : 0, "$v0" : 2, "$v1": 3, "$a0" : 4, "$a1" : 5, "$a2" : 6, "$a3" : 7, "$t0" : 8, "$t1" : 9, "$t2" : 10, "$t3": 11, "$t4" : 12, "$t5" : 13, "$t6" : 14, "$t7" : 15, "$s0" : 16, "$s1" : 17, "$s2" : 18, "$s3": 19, "$s4" : 20, "$s5" : 21, "$s6" : 22, "$s7" : 23, "$t8" : 24, "$t9" : 25, "$gp" : 28, "$sp" : 29, "$fp" : 30, "$ra" : 31}
# dictionary for register numbers

def main():
	x = args.inputfile.readline()
	# reads the first line of the input file
	while x:
	# keeps reading the next line
		y = x.split(' ')
		# splits the read line by spaces
		list0 = []	
		# creates empty list to store broken up input		
		for n in y:
			if n.strip():
				list0.append(n)
		# removes all whitespace and stores it in array
		arguments = list0[1].replace('\n', '')
		# removes newline character at end
		list1 = arguments.split(',')
		# splits arguments up and stores them in array
		list1.insert(0,list0[0])		
		# adds command to array
		
		if len(list1) == 3:
			next = convert3(list1)
		# if the input contains parenthesis, two arguments will still be connected and need to be separates still, goes to different function to convert			
		else:
			next = convert4(list1)
		# converts into opcode and stores in variable
		f.write(next)
		f.write("\n")
		# adds machine code and newline to out_code.txt
		
		x = args.inputfile.readline()
		# reads next line
	args.inputfile.close()
	# closes file when done reading
	
def convert3(list):
	converted = ''
	# variable to store amchine code
	removed = list[2].replace(')', '')
	# removes the back parenthesis
	new = removed.split('(')
	# creates a new list that contains the two connected arguments separately
	new.insert(0, list[1])
	# adds back in first argument
	new.insert(0, list[0])
	# adds back in command
	
	if list[0] == 'lw':
		converted += '100011' #opcode
		converted += binary5(regNum[new[3]]) #rs
		converted += binary5(regNum[new[1]]) #rt
		converted += binary16(int(new[2])) #offset
	elif list[0] == 'sw':
		converted += '101011' #opcode
		converted += binary5(regNum[new[3]]) #rs
		converted += binary5(regNum[new[1]]) #rt
		converted += binary16(int(new[2])) #offset
	else:
		f.write("!!! Invalid Input !!! \n") 
		sys.exit()
		# exits if command is incorrect
	return converted

def convert4(list):
	converted = ''
	
	if list[0] == 'add':
		converted += '000000' #opcode
		converted += binary5(regNum[list[2]]) #rs
		converted += binary5(regNum[list[3]]) #rt
		converted += binary5(regNum[list[1]]) #rd
		converted += '00000100000' #shamt and funct
		
	elif list[0] == 'sub':
		converted += '000000' #opcode
		converted += binary5(regNum[list[2]]) #rs
		converted += binary5(regNum[list[3]]) #rt
		converted += binary5(regNum[list[1]]) #rd
		converted += '00000100010' #shamt and funct
		
	elif list[0] == 'slt':
		converted += '000000' #opcode
		converted += binary5(regNum[list[2]]) #rs
		converted += binary5(regNum[list[3]]) #rt
		converted += binary5(regNum[list[1]]) #rd
		converted += '00000101010' #shamt and funct
		
	elif list[0] == 'sll':
		converted += '000000'
		converted += binary5(regNum[list[2]]) #rt
		converted += binary5(regNum[list[1]]) #rd
		converted += '00000000000'
		
	elif list[0] == 'srl':
		converted += '000000'
		converted += binary5(regNum[list[2]]) #rt
		converted += binary5(regNum[list[1]]) #rd
		converted += '00000000010'
	
	elif list[0] == 'bne':
		converted += '000101' #opcode
		converted += binary5(regNum[list[1]]) #rs
		converted += binary5(regNum[list[2]]) #rt
		div = int(list[3])/4
		# div by 4 to get offset
		converted += binary16(int(div)) #offset
		
	elif list[0] == 'beq':
		converted += '000100' #opcode
		converted += binary5(regNum[list[1]]) #rs
		converted += binary5(regNum[list[2]]) #rt
		div = int(list[3])/4
		# div by 4 to get offset
		converted += binary16(int(div)) #offset
		
	elif list[0] == 'addi':
		converted += '001000' #opcode
		converted += binary5(regNum[list[2]]) #rs
		converted += binary5(regNum[list[1]]) #rt
		converted += binary16(int(list[3])) #imm
	
	else:
		f.write("!!! Invalid Input !!! \n")
		sys.exit()
		# exits if command is incorrect
	return converted

	
def binary5(num):
	converted = bin(num)
	# converts num to binary
	binary = converted[2:]
	# takes out the 0b in the front
	check = str(binary)
	# converts to string to concatenate
	
	if len(check) > 5:
		f.write("!!! Invalid Input !!! \n")
		sys.exit()
		# exits if number is out of range
		
	numZeros = 5 - len(check)
	for n in range(numZeros):
		check = '0' + check
	# adds leading zeros
		
	return check
	
def binary16(num):
	if num < 0:
		number = int(num)
		tmp = 0
		tmp |= (number & 0b00000000000000001111111111111111)
		binary = format(tmp, '016b')
	# calculates twos complement
		
	else:
		converted = bin(num)
		# converts to binary
		binary = converted[2:]
		# takes out 0b in front
	
	check = str(binary)
	# converts to string to concatenate
	
	if num > 32767 or num < -32767:
		f.write("!!! Invalid Input !!! \n")
		sys.exit()
		# exits if number is out of range
		
	numZeros = 16 - len(check)
	for n in range(numZeros):
			check = '0' + check
	# adds leading zeros
		
	return check


if __name__ == "__main__":
	main()
