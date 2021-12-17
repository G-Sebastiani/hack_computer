#! /bin/python
#   _____                                                   _     _           
#  / ____|                     /\                          | |   | |          
# | |     _ __ ___  ___ ___   /  \   ___ ___  ___ _ __ ___ | |__ | | ___ _ __ 
# | |    | '__/ _ \/ __/ __| / /\ \ / __/ __|/ _ \ '_ ` _ \| '_ \| |/ _ \ '__|
# | |____| | | (_) \__ \__ \/ ____ \\__ \__ \  __/ | | | | | |_) | |  __/ |   
#  \_____|_|  \___/|___/___/_/    \_\___/___/\___|_| |_| |_|_.__/|_|\___|_|   
#
# Usage:	casm.py [filename]
#				Inputs	[filename].asm file
#				Outputs	[filename].hack file
import sys
#==================================================
# Global variables for translation:
#==================================================
cinstr =     ["0",       "1",       "-1",      "D",       "A",       "!D",      "!A",      "-D",      "-A",      "D+1",     "A+1",     "D-1",     "A-1",     "D+A",     "D-A",     "A-D",     "D&A",     "D|A",     "M",       "!M",      "-M",      "M+1",     "M-1",     "D+M",     "D-M",     "M-D",     "D&M",     "D|M"]
cinstr_bin = ["0101010", "0111111", "0111010", "0001100", "0110000", "0001101", "0110001", "0001111", "0110011", "0011111", "0110111", "0001110", "0110010", "0000010", "0010011", "0000111", "0000000", "0010101", "1110000", "1110001", "1110011", "1110111", "1110010", "1000010", "1010011", "1000111", "1000000", "1010101"]
reg =     ["null", "M",   "D",   "MD",  "A",   "AM",  "AD",  "AMD"]
reg_bin = ["000",  "001", "010", "011", "100", "101", "110", "111"]
jump =     ["null", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
jump_bin = ["000",  "001", "010", "011", "100", "101", "110", "111"]
symbols =     ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "KBD",   "SCREEN", "SP", "LCL", "ARG", "THIS", "THAT"]
symbols_bin = ["0",  "1",  "2",  "3",  "4",  "5",  "6",  "7",  "8",  "9",  "10",  "11",  "12",  "13",  "14",  "15",  "24578", "16384",  "0",  "1",   "2",   "3",    "4"]
next_mem = 16
#==================================================
# Preprocess:
#==================================================
def preProcess(filename):
	addr = 0
	source = open(filename + ".asm", "r")
	for rad in source:
  		if rad.strip() != "":
			rad = rad.split("//")
    		rad = rad[0].strip()
    		if rad == "":
      			continue
    		elif rad[0] == "(":
      			label = rad[1:len(rad)-1]
      			symbols.append(label)
      			symbols_bin.append(addr)
    		else:
      			addr = addr + 1
	source.close()
#==================================================
# Get A-instruction:
#==================================================
def getAinstr(rad):
	global next_mem 
	if rad.isdigit():
		ret = "{0:00b}".format(int(rad))
	else:
		try:
			ret = str(symbols_bin[symbols.index(rad)])
			ret = "{0:00b}".format(int(ret))
		except:
			symbols.append(rad)
			symbols_bin.append(str(next_mem))
			ret = "{0:00b}".format(int(next_mem))
			next_mem = next_mem + 1
	while len(ret) < 16:
		ret = "0" + ret
	return ret
#==================================================
# Get C-instruction:
#==================================================
def getCinstr(rad):
	#--------------------------------------------------
	# Split string:
	#--------------------------------------------------
	try:
		j = str(rad.split(";")[1])
		temp = rad.split(";")[0]
	except:
		j = "null"
		temp = rad
	try:
		temp = temp.split("=")
		d = str(temp[0])
		c = str(temp[1])
	except:
		d = "null"
		c = temp[0]
	#--------------------------------------------------
	# Operation
	#--------------------------------------------------
	for i, data in enumerate(cinstr):
		if data == c:
			c = cinstr_bin[i]
	#--------------------------------------------------
	# Destination register
	#--------------------------------------------------
	for i, data in enumerate(reg):
		if data == d:
			d = reg_bin[i]
	#--------------------------------------------------
	# Jump
	#--------------------------------------------------
	for i, data in enumerate(jump):
		if data == j:
			j = jump_bin[i]
	ret = "111" + str(c) + str(d) + str(j)
	return ret
#==================================================
# Parse:
#==================================================
def parse(filename):
	addr = 0
	try:
		source = open(filename + ".asm", "r")
		dest = open(filename + ".hack", "w")
	except:
		print "casm.py [filename] <-- Missing argument"
		print "Provide name of .asm file (without extention) to create .hack file."
		source.close()
		dest.close()
	for i in source:
		if i.strip() != "":
			i = i.split("//")
			i = i[0].strip()
			if i == "":
				continue
			elif i[0] == "@":
				i = i.split("@")[1]
				binInstr = getAinstr(i)
				dest.write(binInstr + "\n")
				addr = addr + 1
			elif i[0] == "(":
				continue
			else:
				binInstr = getCinstr(i)
				dest.write(binInstr + "\n")
				addr = addr + 1
	source.close()
	dest.close()
#==================================================
# Main
#==================================================
def main():
	filename = sys.argv[1]
	preProcess(filename)
	parse(filename)
#==================================================
# Starting point 
#==================================================
main()


