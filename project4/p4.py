import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('inputfile', type=argparse.FileType('r'))
args = parser.parse_args()

f = open("out_control.txt", "w")
# creates output file1

g = open("out_registers.txt", "w")
# creates output file2

def main():
	registers = [ 65536, 0, 0, 0, 0, 0, 0, 0, 0 ]
	# array for registers
	write(registers)
	# writes to out_registers before starting
	x = args.inputfile.readline()
	# reads the first line of the input file
	while x:
		opcode = x[:6]
		# gets first 6 of 32 (opcode)
		funct = x[26:]
		# gets last 6 of 32 (funct)
		registers[0] += 4
		# adds 4 to clock
		if registers[0] > 65936:
			args.inputfile.close()
			# if clock has been added to by 400 (100 times * 4 increment), exit program because >100 lines
		if (opcode == "001000"):
			addi(registers, x)
			# jumps to addi function
		elif (opcode == "000000"):
			addSub(registers, x, funct)	
			# jumps to add or sub function
		x = args.inputfile.readline()
		# reads next line
	args.inputfile.close()
	# closes file when no more lines to read


def addi(registers, x):
	imm = x[16:]
	# last 16 of 32 (immediate)
	val = int(imm, 2)
	# converts to decimal from binary
	
	rs = x[6:11]
	# index 6-10 (rs)
	intRS = int(rs, 2)
	# converts to decimal from binary
	
	rt = x[11:16]
	# index 11-15 (rt)
	intRT = int(rt, 2)
	# converts to decimal from binary
	
	registers[intRT + 1] = intRS + val
	# addi function
	
	controlOut = "0101000000"
	f.write(controlOut)
	f.write("\n")	
	# prints control (always the same for same op)
	
	write(registers)
	# function to write in out_register.txt
	

def addSub(registers, x, funct):
	rs = x[6:11]
	# index 6-10 (rs)
	intRS = int(rs, 2)
	# converts to decimal from binary
	
	rt = x[11:16]
	# index 11-15 (rt)
	intRT = int(rt, 2)
	# converts to decimal from binary
	
	rd = x[16:21]
	# index 16-10 (rd)
	intRD = int(rd, 2)
	# converts to decimal from binary
	
	fun = int(funct)
	
	if fun == 100000:
		registers[intRD + 1] = registers[intRS + 1] + registers[intRT + 1]
		# add function
	elif fun == 100010:
		registers[intRD + 1] = registers[intRS + 1] - registers[intRT + 1]
		# sub function
	
	controlOut = "1001000100"
	f.write(controlOut)
	f.write("\n")
	# prints control (always the same for same op)
	
	write(registers)
	# function to write in out_register.txt
	
	
def write(registers):
	outregisters = ""
	# creates variable for string
	for x in registers:
		y = str(x)
		outregisters += y
		outregisters += " | "
		# adds each element followed by " | "
	finalreg = outregisters[:-3]
	# deletes extra " | "
	g.write(finalreg)
	# writes final string into file
	g.write("\n")
	


	
if __name__ == "__main__":
	main()
