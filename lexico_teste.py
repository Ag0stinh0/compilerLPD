# Analisador Léxico - Compiladores
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

tokens = {}
count = 0
characters = []
arithmetics = ["+", "-", "*"]
operations = [">", "<", "="]
punctuation = [";", ",", "(", ")", ".", "[", "]"]
errors = ["/", "%", "!", "@", "#","$"]


# Define the symbol or the identifier
def defineSymbol(id):
	if id == "programa":
		symbol = "sprograma"
	elif id == "se":
		symbol = "sse"
	elif id == "entao":
		symbol = "sentao"
	elif id == "senao":
		symbol = "ssenao"
	elif id == "enquanto":
		symbol = "senquanto"
	elif id == "faca":
		symbol = "sfaca"
	elif id == "inicio":
		symbol = "sinicio"
	elif id == "fim":
		symbol = "sfim"
	elif id == "escreva":
		symbol = "sescreva"
	elif id == "leia":
		symbol = "sleia"
	elif id == "var":
		symbol = "svar"
	elif id == "inteiro":
		symbol = "sinteiro"
	elif id == "booleano":
		symbol = "sbooleano"
	elif id == "verdadeiro":
		symbol = "sverdadeiro"
	elif id == "falso":
		symbol = "sfalso"
	elif id == "procedimento":
		symbol = "sprocedimento"
	elif id == "funcao":
		symbol = "sfuncao"
	elif id == "div":
		symbol = "sdiv"
	elif id == "e":
		symbol = "se"
	elif id == "ou":
		symbol = "sou"
	elif id == "nao":
		symbol = "snao"
	else:
		symbol = "sidentificador"
	return symbol
	

# Function to Resolve Commentary Section
def resolveComments(index):
	while characters[index] is not "}":
		index += 1
		if index >= len(characters):
			break

	return index
	

# Function to Resolve Identifiers and Reserved Words
def resolveLetter(index):
	global count
	id = ""
	id += characters[index]
	index += 1
	while characters[index].isalpha() or characters[index] is "_" or characters[index].isnumeric():
		id += characters[index]
		index += 1
	
	lexeme = id
	symbol = defineSymbol(id)
	tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
	count += 1
	index -= 1
	return index

	
# Function to Resolve Digits
def resolveNumber(index):
	global count
	num = ""
	num += characters[index]
	index += 1
	while characters[index].isnumeric():
		num += characters[index]
		index += 1
		
	lexeme = num
	symbol = "snumero"
	tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
	count += 1
	index -= 1
	return index

	
# Function to Resolve Assignment characters
def resolveAssignment(index):
	global count
	id = ""
	id += characters[index]
	index += 1
	if characters[index] is "=":
		id += characters[index]
		
		lexeme = id
		symbol = "satribuicao"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
		return index
		
	else:
		lexeme = id
		symbol = "sdoispontos"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
		index -= 1
		return index
	
# Function to Resolve Arithmetics operators
def resolveOperators(index):
	global count
	
	if characters[index] is "+":
		lexeme = "+"
		symbol = "smais"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	elif characters[index] is "-":
		lexeme = "-"
		symbol = "smenos"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	elif characters[index] is "*":
		lexeme = "*"
		symbol = "smult"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
		

# Function to Resolve Relational operators
def resolveRelationals(index):
	global count
	id = ""
	
	if characters[index] is ">":
		id += characters[index]
		index += 1
		if characters[index] is "=":
			id += characters[index]
			
			lexeme = id
			symbol = "smaiorig"
			tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
			count += 1
		
		else:
			lexeme = id
			symbol = "smaior"
			tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
			count += 1
			index -= 1
			
	elif characters[index] is "<":
		id += characters[index]
		index += 1
		if characters[index] is "=":
			id += characters[index]
			
			lexeme = id
			symbol = "smenorig"
			tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
			count += 1
		
		else:
			lexeme = id
			symbol = "smenor"
			tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
			count += 1
			index -= 1
	
	elif characters[index] is "!":
		id += characters[index]
		index += 1
		if characters[index] is "=":
			id += characters[index]
		
			lexeme = id
			symbol = "sdif"
			tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
			count += 1
		else:
			index -= 1
	
	elif characters[index] is "=":
		id += characters[index]
		index += 1
		lexeme = id
		symbol = "sigual"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	return index

# Function to Resolve Punctuation
def resolvePunctuation(index):
	global count
	
	if characters[index] is "(":
		lexeme = "("
		symbol = "sabre_parenteses"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	elif characters[index] is ")":
		lexeme = ")"
		symbol = "sfecha_parenteses"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	elif characters[index] is ".":
		lexeme = "."
		symbol = "sponto"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	elif characters[index] is ";":
		lexeme = ";"
		symbol = "sponto_virgula"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1
	elif characters[index] is ",":
		lexeme = ","
		symbol = "svirgula"
		tokens[count] = {"Lexeme": lexeme, "Symbol": symbol}
		count += 1

	
# Starts to catch the Tokens
def catchTokens():
	index = 0
	
	while index < len(characters):
		if characters[index] is "{":
			index = resolveComments(index)
			
		elif characters[index].isnumeric():
			index = resolveNumber(index)
			
		elif characters[index].isalpha():
			index = resolveLetter(index)
			
		elif characters[index] == ":":
			index = resolveAssignment(index)
			
		elif characters[index] in arithmetics:
			resolveOperators(index)
			
		elif characters[index] in operations:
			index = resolveRelationals(index)
			
		elif characters[index] in punctuation:
			resolvePunctuation(index)
		
		elif characters[index] in errors:
			return characters[index]
		
		index += 1
	return "Success"

	
# Read the file and create the list of characters
def reader(lines):
	for line in lines: 	
		words = line.split()
		for word in words:
			for indexLetter in range(0,len(word)):
				characters.append(word[indexLetter])						
			characters.append(" ")
	
	returned = catchTokens()
	if returned != "Success":
		for line in lines: 
			if returned in line:
				print("Error in line " + str(lines.index(line) + 1) + ": Unexpected character " + returned)
				return False
	return True

# Open the file and call the File Reader
def main():
	n = input("Insert the number of the test (1-9): ")

	path = "./teste"+str(n)+".txt"
	file = open(path,'r')
	lines = file.readlines()

	if reader(lines) is True:	
		print("\nTokens:")
		for tok in tokens:
			print("\n" + str(tok + 1))
			print("|-Lexema: " + tokens[tok]["Lexeme"] + "\n" + "|-Símbolo: " + tokens[tok]["Symbol"])
			
			
if __name__ == '__main__':
	main()