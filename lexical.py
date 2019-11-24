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
contentLines = []
content = 0
count = 0
index = 0	# Stores the index of characters

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
	global count
	global content
	
	while characters[index] is not "}":
		index +=1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1
		if index >= len(characters):
			break

# Function to Resolve Identifiers and Reserved Words
def resolveLetter():
	global index
	global count
	global content

	id = ""
	id += characters[index]
	index += 1
	content += 1
	if content == (contentLines[count]):
		content = 0
		count += 1
	while characters[index].isalpha() or characters[index] is "_" or characters[index].isnumeric():
		id += characters[index]
		index += 1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1
	lexeme = id
	symbol = defineSymbol(id)
	line = count + 1

	token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}
	index -= 1
	content -= 1
	if content == -1:
		count -= 1
		content = (contentLines[count]-1)
		
	return token


# Function to Resolve Digits
def resolveNumber():
	global index
	global count
	global content

	num = ""
	num += characters[index]
	index += 1
	content += 1
	if content == (contentLines[count]):
		content = 0
		count += 1
	while characters[index].isnumeric():
		num += characters[index]
		index += 1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1

	lexeme = num
	symbol = "snumero"
	line = count + 1
	token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	index -= 1
	content -= 1
	if content == -1:
		count -= 1
		content = (contentLines[count]-1)
	return token


# Function to Resolve Assignment characters
def resolveAssignment():
	global index
	global count
	global content

	id = ""
	id += characters[index]
	index += 1
	content += 1
	if content == (contentLines[count]):
		content = 0
		count += 1
	if characters[index] is "=":
		id += characters[index]
		lexeme = id
		symbol = "satribuicao"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}
		return token
	else:
		lexeme = id
		symbol = "sdoispontos"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		index -= 1
		content -= 1
		if content == -1:
			count -= 1
			content = (contentLines[count]-1)
		return token

# Function to Resolve Arithmetics operators
def resolveOperators():
	global index
	global count


	if characters[index] is "+":
		lexeme = "+"
		symbol = "smais"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		return token
	elif characters[index] is "-":
		lexeme = "-"
		symbol = "smenos"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		return token
	elif characters[index] is "*":
		lexeme = "*"
		symbol = "smult"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		return token


# Function to Resolve Relational operators
def resolveRelationals():
	global index
	global count
	global content

	id = ""

	if characters[index] is ">":
		id += characters[index]
		index += 1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1
		if characters[index] is "=":
			id += characters[index]

			lexeme = id
			symbol = "smaiorig"
			line = count + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}


		else:
			lexeme = id
			symbol = "smaior"
			line = count + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

			index -= 1
			content -= 1
			if content == -1:
				count -= 1
				content = (contentLines[count]-1)

	elif characters[index] is "<":
		id += characters[index]
		index += 1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1
		if characters[index] is "=":
			id += characters[index]

			lexeme = id
			symbol = "smenorig"
			line = count + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}


		else:
			lexeme = id
			symbol = "smenor"
			line = count + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

			index -= 1
			content -= 1
			if content == -1:
				count -= 1
				content = (contentLines[count]-1)

	elif characters[index] is "!":
		id += characters[index]
		index += 1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1
		if characters[index] is "=":
			id += characters[index]

			lexeme = id
			symbol = "sdif"
			line = count + 1
			token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

		else:
			index -= 1
			content -= 1
			if content == -1:
				count -= 1
				content = (contentLines[count]-1)

	elif characters[index] is "=":
		id += characters[index]
		index += 1
		content += 1
		if content == (contentLines[count]):
			content = 0
			count += 1
		lexeme = id
		symbol = "sigual"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	return token

# Function to Resolve Punctuation
def resolvePunctuation():
	global index
	global count

	if characters[index] is "(":
		lexeme = "("
		symbol = "sabre_parenteses"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ")":
		lexeme = ")"
		symbol = "sfecha_parenteses"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ".":
		lexeme = "."
		symbol = "sponto"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ";":
		lexeme = ";"
		symbol = "sponto_virgula"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	elif characters[index] is ",":
		lexeme = ","
		symbol = "svirgula"
		line = count + 1
		token = {"Lexeme": lexeme, "Symbol": symbol, "Line": line}

	return token


# Starts to catch the Tokens
def getToken():
	global index
	global content
	global count

	while index < len(characters):
		if characters[index] is "{":
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			resolveComments()
			if(index >= len(characters)):
				errorComment()

		elif characters[index].isnumeric():
			token = resolveNumber()
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			return token

		elif characters[index].isalpha():
			token = resolveLetter()
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			return token

		elif characters[index] == ":":
			token = resolveAssignment()
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			return token

		elif characters[index] in arithmetics:
			token = resolveOperators()
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			return token

		elif characters[index] in operations:
			token = resolveRelationals()
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			return token

		elif characters[index] in punctuation:
			token = resolvePunctuation()
			index += 1
			content += 1
			if content == (contentLines[count]):
				content = 0
				count += 1
			return token

		elif characters[index] is not " ":
			error(characters[index])
		index +=1
		content +=1
		if content == (contentLines[count]):
			content = 0
			count += 1

	return "End"


# Open the file and call the File Reader
def getFile(filePath):
	global lines
	global contentLines

	try:
		file = open(filePath,'r')
		lines = file.readlines()
		for line in lines:
			if line == "\n":
				contentLines.append(1)
				characters.append(" ")
			else:
				contentLines.append(len(line))
				for indexLetter in range(0,len(line)):
					if line[indexLetter] != "\n":
						characters.append(line[indexLetter])
					else:
						characters.append(" ")		
		file.close()

	except:
		print ("Error opening file")
		file.close()
		exit()


def error(wrongChar):
	global count
	
	print("Found a error: Unexpected character " + wrongChar + " in line " + str(count + 1))	
	exit()
	
def errorComment():
	print("Found an error: Expected } to finish the comment!")
	exit()
