# Maquina Virtual - Compiladores
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import collections
import os
from colorama import init, Fore, Back, Style


stack = collections.deque([])
stack_pointer = 0
program_register = -1
program = []
user_inputs = []
breaks = []
outputs = []
# print(Style.RESET_ALL, end = '')

def printInterface(e):
	global program
	global stack
	global program_register
	global breaks
	global outputs
	lenStack = len(stack)

	os.system('clear')
	if len(program) == 0:
		print("+-----------------------------------------------------------------+  +-------------+		Commands:")
		print("|                         Instructions                            |  |    Stack    |		o <file_name> => Open object")
		print("+-----------------------------------------------------------------+  +-------------+		b <line> => Set break point")
		for i in range(0,18):
			if i == 0:
				print("|                                                                 |  |             |		n => Execute next instruction")
			elif i == 1:
				print("|                                                                 |  |             |		s => Start Execution")
			else:
				print("|                                                                 |  |             |")
		print("+-----------------------------------------------------------------+  |             |")
		print("+-----------------------------------------------------------------+  |             |")
		print("|      Inputs      | |      Outputs       | |    Break Points     |  |             |")
		print("+------------------+ +--------------------+ +---------------------+  |             |")
		for i in range(0,9):
			print("|                  | |                    | |                     |  |             |")
		print("+------------------+ +--------------------+ +---------------------+  +-------------+")
		if e == 1:
			print("Wrong command")
		print(">> ", end='')
	else:
		# print(stack)
		# print(breaks)
		print("+-----------------------------------------------------------------+  +-------------+		Commands:")
		print("|                         Instructions                            |  |    Stack    |		o <file_name> => Open object")
		print("+-----------------------------------------------------------------+  +-------------+		b <line> => Set break point")
		for i in range(0,len(program)):
			if i == 0:
				if program_register == -1:
					print(Back.GREEN + "| " + str(i) + "  %-*s |  " %(60,program[i]) ,end ='')
					print(Style.RESET_ALL, end = '')
				else:
					print("| " + str(i) + "  %-*s |  " %(60,program[i]) ,end ='')
				if len(stack) > 0 and i < lenStack:
					print("| %-*s |		n => Execute next instruction" %(11,stack[i]))
				else:
					print("|             |		n => Execute next instruction")
			elif i == 1:
				if program_register == i:
					print(Back.GREEN + "| " + str(i) + "  %-*s |  " %(60,program[i]) ,end ='')
					print(Style.RESET_ALL, end = '')
				else:
					print("| " + str(i) + "  %-*s |  " %(60,program[i]) ,end ='')
				if len(stack) > 0 and i < lenStack:
					print("| %-*s |		s => Start Execution" %(11,stack[i]))
				else:
					print("|             |		s => Start Execution")
			else:
				if i >= 10:
					if program_register == i:
						print(Back.GREEN + "| " + str(i) + "  %-*s |  " %(59,program[i]) ,end ='')
						print(Style.RESET_ALL, end = '')
					else:
						print("| " + str(i) + " %-*s |  " %(60,program[i]) ,end ='')
					if len(stack) > 0 and i < lenStack:
						print("| %-*s |		" %(11,stack[i]))
					else:
						print("|             |")
				else:
					if program_register == i:
						print(Back.GREEN + "| " + str(i) + "  %-*s |  " %(60,program[i]) ,end ='')
						print(Style.RESET_ALL, end = '')
					else:
						print("| " + str(i) + "  %-*s |  " %(60,program[i]) ,end ='')
					if len(stack) > 0 and i < lenStack:
						print("| %-*s |		" %(11,stack[i]))
					else:
						print("|             |")
		print("+-----------------------------------------------------------------+  |             |")
		print("+-----------------------------------------------------------------+  |             |")
		print("|      Inputs      | |      Outputs       | |    Break Points     |  |             |")
		print("+------------------+ +--------------------+ +---------------------+  |             |")
		for i in range(0,9):
			if len(user_inputs) > 0 and i < len(user_inputs):
				if user_inputs[i] < 10:
					print("| %-*s | " %(16,user_inputs[i]), end='')
				else:
					print("| %-*s | " %(16,user_inputs[i]), end='')
			else:
				print("|                  | ", end='')

			if len(outputs) > 0 and i < len(outputs):
				if outputs[i] < 10:
					print("| %-*s | " %(18,outputs[i]), end='')
				else:
					print("| %-*s | " %(18,outputs[i]), end='')
			else:
				print("|                    | ", end ='')

			if len(breaks) > 0 and i < len(breaks):
				if breaks[i] < 10:
					print("| %-*s |  |             |" %(19,breaks[i]))
				else:
					print("| %-*s |  |             |" %(19,breaks[i]))
			else:
				print("|                     |  |             |")
			# print("|                  | |                    | |                     |  |             |")
		print("+------------------+ +--------------------+ +---------------------+  +-------------+")
		if e == 1:
			print("Wrong command")
		print(">> ", end='')



def push(value):
	stack.append(value)
	global stack_pointer
	stack_pointer += 1


def pop():
	global stack_pointer
	ret = stack.pop()
	stack_pointer -= 1
	return ret


def executeComand(line):
	global stack_pointer
	global stack
	global program_register
	global program

	# if line[0] == "START":
		# print("\n"+ str(line))
		#stack_pointer = -1

	if line[0] == "HLT":
		# print("\n"+ str(line))
		return "End"

	elif line[0] == "LDC":
		if line[1].isnumeric():
			# print("\n"+ str(line))
			push(int(line[1]))
			# print (stack)
		else:
			return "Error"

	elif line[0] == "LDV":
		if line[1].isnumeric():
			# print("\n"+ str(line))
			push(stack[int(line[1])])
			# print (stack)
		else:
			return "Error"

	elif line[0] == "ADD":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			# print(stack)
			x = pop()
			y = pop()
			r = y + x
			# print(str(r))
			push(r)


	elif line[0] == "SUB":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			# print(stack)
			x = pop()
			y = pop()
			r = y - x
			# print(str(r))
			push(r)

	elif line[0] == "MULT":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			# print(stack)
			x = pop()
			y = pop()
			r = y * x
			# print(str(r))
			push(r)

	elif line[0] == "DIVI":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			# print(stack)
			x = pop()
			y = pop()
			r = y / x
			#r = int(r)
			# print(str(r))
			push(r)

	elif line[0] == "INV":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			stack[stack_pointer] *= -1
			# print(stack)

	elif line[0] == "AND":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if x == 1 and y == 1:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "OR":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if x == 1 or y == 1:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "NEG":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			stack[stack_pointer] = 1 - stack[stack_pointer]
			# print(stack)

	elif line[0] == "CME":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if y < x:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "CMA":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if y > x:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "CEQ":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if y == x:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "CDIF":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if y != x:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "CMEQ":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if y <= x:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "CMAQ":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			x = pop()
			y = pop()
			if y >= x:
				push(1)
				# print(stack)
			else:
				push(0)
				# print(stack)

	elif line[0] == "STR":
		if line[1].isnumeric():
			# print("\n"+ str(line))
			x = pop()
			stack[int(line[1])] = x
			# print (stack)
		else:
			return "Error"

	elif line[0] == "JMP":
		if line[1].isnumeric() and	int(line[1]) < len(program):
			# print("\n"+ str(line))
			# print (stack)
			program_register = int(line[1]) - 2
		elif line[1].isalnum():
			# print("\n"+ str(line))
			for l in program:
				if l[0] == line[1]:
					program_register = program.index(l)
		else:
			return "Error"

	elif line[0] == "JMPF":
		if line[1].isnumeric() and	int(line[1]) < len(program) and stack[stack_pointer] == 0:
			# print("\n"+ str(line))
			program_register = int(line[1]) - 2
			# print (stack)
		elif line[1].isalnum():
			# print("\n"+ str(line))
			# print (stack)
			for l in program:
				if l[0] == line[1]:
					program_register = program.index(l)
		else:
			return "Error"

	elif line[0] == "NULL":
		if len(line) > 1:
			return "Error"
		# print("\n"+ str(line))

	elif line[0] == "CALL":
		if line[1].isnumeric() and	int(line[1]) < len(program):
			# print("\n"+ str(line))
			push(program_register + 2)
			# print (stack)
			program_register = int(line[1]) - 2
		else:
			return "Error"

	elif line[0] == "RETURN":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			# print (stack)
			program_register = pop()
			program_register -= 2

	elif line[0] == "PRN":
		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			# print (stack)
			x = pop()
			outputs.append(x)

	elif line[0] == "RD":
		global user_inputs

		if len(line) > 1:
			return "Error"
		else:
			# print("\n"+ str(line))
			printInterface(0)
			x = int(input())
			user_inputs.append(x)
			push(x)
			# print (stack)

	elif line[0] == "ALLOC":
		if line[1].isnumeric() and	line[2].isnumeric():
			# print("\n"+ str(line))
			n = int(line[2])
			m = int(line[1])
			for k in range(0,n):
				push(0)
			# print(stack)
		else:
			return "Error"

	elif line[0] == "DALLOC":
		if line[1].isnumeric() and	line[2].isnumeric():
			# print("\n"+ str(line))
			n = int(line[2])
			m = int(line[1])
			for k in range(n-1,-1,-1):
				stack[m + k] = pop()
			# print(stack)
		else:
			return "Error"

	return "OK"


def startVM():
	global program
	global program_register

	program_register += 1
	found = False

	while program_register < len(program):
		# for b in breaks:
		# 	if program_register == b:
		# 		found = True
		# 		break
		# if found:
		# 	break
		ret = executeComand(program[program_register])
		if ret == "Error":
			print("\nError in line " + str(program_register + 1))
			break
		elif ret == "End":
			break
		program_register += 1


def main():
	global program
	global program_register
	global breaks

	error = 0
	while True:
		printInterface(error)
		command = input()
		aux = command.split()
		if aux[0] == "o" and len(aux) > 1:
			error = 0
			path = aux[1] + ".obj"
			try:
				file = open(path,"r")
			except:
				print("No such file, try again")
			lines = file.readlines()
			for line in lines:
				if line != "\n":
					program.append(line.split())
			# startVM()
		elif aux[0] == "b" and len(aux) > 1:
			error = 0
			breaks.append(int(aux[1]))
		elif aux[0] == "s":
			error = 0
			startVM()
		elif aux[0] == "n":
			error = 0
			# printInterface(error)
			if program_register == -1:
				program_register += 1
			if program_register < len(program):
				ret = executeComand(program[program_register])
				if ret == "Error":
					print("\nError in line " + str(program_register + 1))
					break
				elif ret == "End":
					break
				program_register += 1
		elif aux[0] == "q":
			print("Bye")
			break
		else:
			error = 1


if __name__ == "__main__":
	main()
