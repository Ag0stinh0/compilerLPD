# Maquina Virtual - Compiladores
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import collections


stack = collections.deque([])
stack_pointer = 3
program_register = -1
program = []


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

	if line[0] == "START":
		print("\n"+ str(line))
		#stack_pointer = -1

	elif line[0] == "HLT":
		print("\n"+ str(line))
		return "End"

	elif line[0] == "LDC":
		if line[1].isnumeric():
			print("\n"+ str(line))
			push(int(line[1]))
			print (stack)
		else:
			return "Error"

	elif line[0] == "LDV":
		if line[1].isnumeric():
			print("\n"+ str(line))
			push(stack[int(line[1])])
			print (stack)
		else:
			return "Error"

	elif line[0] == "ADD":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			print(stack)
			x = pop()
			y = pop()
			r = y + x
			print(str(r))
			push(r)


	elif line[0] == "SUB":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			print(stack)
			x = pop()
			y = pop()
			r = y - x
			print(str(r))
			push(r)

	elif line[0] == "MULT":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			print(stack)
			x = pop()
			y = pop()
			r = y * x
			print(str(r))
			push(r)

	elif line[0] == "DIVI":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			print(stack)
			x = pop()
			y = pop()
			r = y / x
			#r = int(r)
			print(str(r))
			push(r)

	elif line[0] == "INV":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			stack[stack_pointer] *= -1
			print(stack)

	elif line[0] == "AND":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if x == 1 and y == 1:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "OR":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if x == 1 or y == 1:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "NEG":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			stack[stack_pointer] = 1 - stack[stack_pointer]
			print(stack)

	elif line[0] == "CME":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if y < x:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "CMA":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if y > x:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "CEQ":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if y == x:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "CDIF":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if y != x:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "CMEQ":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if y <= x:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "CMAQ":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = pop()
			y = pop()
			if y >= x:
				push(1)
				print(stack)
			else:
				push(0)
				print(stack)

	elif line[0] == "STR":
		if line[1].isnumeric():
			print("\n"+ str(line))
			x = pop()
			stack[int(line[1])] = x
			print (stack)
		else:
			return "Error"

	elif line[0] == "JMP":
		if line[1].isnumeric() and	int(line[1]) < len(program):
			print("\n"+ str(line))
			print (stack)
			program_register = int(line[1]) - 2
		elif line[1].isalnum():
			print("\n"+ str(line))
			for l in program:
				if l[0] == line[1]:
					program_register = program.index(l)
		else:
			return "Error"

	elif line[0] == "JMPF":
		if line[1].isnumeric() and	int(line[1]) < len(program) and stack[stack_pointer] == 0:
			print("\n"+ str(line))
			program_register = int(line[1]) - 2
			print (stack)
		elif line[1].isalnum():
			print("\n"+ str(line))
			print (stack)
			for l in program:
				if l[0] == line[1]:
					program_register = program.index(l)
		else:
			return "Error"

	elif line[0] == "NULL":
		if len(line) > 1:
			return "Error"
		print("\n"+ str(line))

	elif line[0] == "CALL":
		if line[1].isnumeric() and	int(line[1]) < len(program):
			print("\n"+ str(line))
			push(program_register + 2)
			print (stack)
			program_register = int(line[1]) - 2
		else:
			return "Error"

	elif line[0] == "RETURN":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			print (stack)
			program_register = pop()
			program_register -= 2

	elif line[0] == "PRN":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			print (stack)
			x = pop()
			print(x)

	elif line[0] == "RD":
		if len(line) > 1:
			return "Error"
		else:
			print("\n"+ str(line))
			x = int(input())
			push(x)
			print (stack)

	elif line[0] == "ALLOC":
		if line[1].isnumeric() and	line[2].isnumeric():
			print("\n"+ str(line))
			n = int(line[2])
			m = int(line[1])
			for k in range(0,n):
				push(0)
			print(stack)
		else:
			return "Error"

	elif line[0] == "DALLOC":
		if line[1].isnumeric() and	line[2].isnumeric():
			print("\n"+ str(line))
			n = int(line[2])
			m = int(line[1])
			for k in range(n-1,-1,-1):
				stack[m + k] = pop()
			print(stack)
		else:
			return "Error"

	return "OK"


def startVM():
	global program
	global program_register

	program_register += 1

	while program_register < len(program):
		ret = executeComand(program[program_register])
		if ret == "Error":
			print("\nError in line " + str(program_register + 1))
			break
		elif ret == "End":
			break
		program_register += 1


def main():
	global program
	path = "testeAssembly1.obj"
	file = open(path,"r")
	lines = file.readlines()
	for line in lines:
		if line != "\n":
			program.append(line.split())
	startVM()


if __name__ == "__main__":
	main()
