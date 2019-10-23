# Projeto Compilador - Analisador Lexico
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

token = {}
indexLine = 0
characters = []
arithmetics = ["+", "-", "*"]
operations = [">", "<", "=", "!"]
punctuation = [";", ",", "(", ")", "."]
errors = ["/", "%", "@", "#","$"]
lines = []
index = 0	# Stores the index of characters

def getLine(word):
	global indexLine
	global lines

	for i in range(indexLine,len(lines)):
		if "{" in lines[i] or "}" in lines[i]:
			if i >= indexLine:
				indexLine += 1
		elif lines[i] == "\n":
			if i >= indexLine:
				indexLine += 1
		elif word in lines[i]:
			if word == ";":
				indexLine += 1
				return indexLine-1
			elif len(lines[i].split()) == 1 and ";" not in lines[i]:
				indexLine += 1
				return indexLine-1
			elif word == "entao":
				indexLine += 1
				return indexLine-1
			elif "fim" in lines[i + 1] and ";" not in lines[i]:
				indexLine += 1
				return indexLine-1
			elif word == ".":
				return indexLine
			return indexLine
		return indexLine



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
def resolveComments():
	global index
	while characters[index] is not "}":
		index +=1
		if index >= len(characters):
			break


# Function to Resolve Identifiers and Reserved Words
def resolveLetter():
	global index

	id = ""
	id += characters[index]
	index += 1
	while characters[index].isalpha() or characters[index] is "_" or characters[index].isnumeric():
		id += characters[index]
		index += 1

	lexeme = id
	symbol = defineSymbol(id)
	line = getLine(lexeme) + 1

	token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}
	index -= 1
	return token


# Function to Resolve Digits
def resolveNumber():
	global index

	num = ""
	num += characters[index]
	index += 1
	while characters[index].isnumeric():
		num += characters[index]
		index += 1

	lexeme = num
	symbol = "snumero"
	line = getLine(lexeme) + 1
	token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	index -= 1
	return token


# Function to Resolve Assignment characters
def resolveAssignment():
	global index

	id = ""
	id += characters[index]
	index += 1
	if characters[index] is "=":
		id += characters[index]
		lexeme = id
		symbol = "satribuicao"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}
		return token
	else:
		lexeme = id
		symbol = "sdoispontos"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		index -= 1
		return token

# Function to Resolve Arithmetics operators
def resolveOperators():
	global index


	if characters[index] is "+":
		lexeme = "+"
		symbol = "smais"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		return token
	elif characters[index] is "-":
		lexeme = "-"
		symbol = "smenos"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		return token
	elif characters[index] is "*":
		lexeme = "*"
		symbol = "smult"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		return token


# Function to Resolve Relational operators
def resolveRelationals():
	global index

	id = ""

	if characters[index] is ">":
		id += characters[index]
		index += 1
		if characters[index] is "=":
			id += characters[index]

			lexeme = id
			symbol = "smaiorig"
			line = getLine(lexeme) + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}


		else:
			lexeme = id
			symbol = "smaior"
			line = getLine(lexeme) + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

			index -= 1

	elif characters[index] is "<":
		id += characters[index]
		index += 1
		if characters[index] is "=":
			id += characters[index]

			lexeme = id
			symbol = "smenorig"
			line = getLine(lexeme) + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}


		else:
			lexeme = id
			symbol = "smenor"
			line = getLine(lexeme) + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

			index -= 1

	elif characters[index] is "!":
		id += characters[index]
		index += 1
		if characters[index] is "=":
			id += characters[index]

			lexeme = id
			symbol = "sdif"
			line = getLine(lexeme) + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		else:
			index -= 1

	elif characters[index] is "=":
		id += characters[index]
		index += 1
		lexeme = id
		symbol = "sigual"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	return token

# Function to Resolve Punctuation
def resolvePunctuation():
	global index


	if characters[index] is "(":
		lexeme = "("
		symbol = "sabre_parenteses"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ")":
		lexeme = ")"
		symbol = "sfecha_parenteses"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ".":
		lexeme = "."
		symbol = "sponto"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ";":
		lexeme = ";"
		symbol = "sponto_virgula"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ",":
		lexeme = ","
		symbol = "svirgula"
		line = getLine(lexeme) + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	return token


# Starts to catch the Tokens
def getToken():
	global index

	while index < len(characters):
		if characters[index] is "{":
			resolveComments()
			if(index >= len(characters)):
				return "Error"
			index += 1

		elif characters[index].isnumeric():
			token = resolveNumber()
			index += 1
			return token

		elif characters[index].isalpha():
			token = resolveLetter()
			index += 1
			return token

		elif characters[index] == ":":
			token = resolveAssignment()
			index += 1
			return token

		elif characters[index] in arithmetics:
			token = resolveOperators()
			index += 1
			return token

		elif characters[index] in operations:
			token = resolveRelationals()
			index += 1
			return token

		elif characters[index] in punctuation:
			token = resolvePunctuation()
			index += 1
			return token

		elif characters[index] is not " ":
			error(characters[index])
		index +=1

	return "End"


# Open the file and call the File Reader
def getFile(filePath):
	global lines

	try:
		file = open(filePath,'r')
		lines = file.readlines()
		for line in lines:
			words = line.split()
			for word in words:
				for indexLetter in range(0,len(word)):
					characters.append(word[indexLetter])
				characters.append(" ")
		file.close()

	except:
		print ("Error opening file")
		file.close()
		exit()


def error(wrongChar):
	global lines
	for line in lines:
		if wrongChar in line:
			print("Found a error: Unexpected character " + wrongChar + " in line " + str(lines.index(line) + 1) )
	exit()
