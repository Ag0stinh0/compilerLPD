# Projeto Compilador - Analisador Sintatico
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import lexical

token = {}

def analyzeBlock():
	global token
	print("analyzing block")
	token = lexical.getToken()
	print(token)
	analyzeVarDeclaration()

	analyzeSubRoutine()

	analyzeCommand()



def analyzeVarDeclaration():
	global token

	print("Var declaration")
	if token["Symbol"] == "svar":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			while token["Symbol"] == "sidentificador":
				analyzeVar()
				if token["Symbol"] == "sponto_virgula":
					token = lexical.getToken()
					print(token)
				else:
					error("a ;",token["Line"])
		else:
			error("an Identifier",token["Line"])


def analyzeVar():
	global token

	print("Analyzing Var")
	while True:
		if token["Symbol"] == "sidentificador":
			#search table for duplicity
			#if not Found
			#insert table
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "svirgula" or token["Symbol"] == "sdoispontos":
				if token["Symbol"] == "svirgula":
					token = lexical.getToken()
					print(token)
					if token["Symbol"] == "sdoispontos":
						error("an Identifier", token["Line"])
			else:
				error("an : or , ", token["Line"])
			#else error
		else:
			error("an Identifier", token["Line"])

		if token["Symbol"] == "sdoispontos":
			break
	token = lexical.getToken()
	print(token)
	analyzeType()


def analyzeType():
	global token

	print("Analyzing Type")
	if token["Symbol"] != "sinteiro" and token["Symbol"] != "sbooleano":
		error("'inteiro' or 'booleano'",token["Line"])
	else:
		#insere na tabela
		token = lexical.getToken()
		print(token)


def analyzeSubRoutine():
	global token
	#auxrot, flag inteiro

	print("Analyzing Sub")
	flag = 0
	if token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		# labels
		print("TODO")
	while token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		if token["Symbol"] == "sprocedimento":
			analyzeProcedureDeclaration()
		else:
			analyzeFunctionDeclaration()
		if token["Symbol"] == "sponto_virgula":
			token = lexical.getToken()
			print(token)
		else:
			error("an ;", token["Line"])
	if flag == 1:
		# generate
		print("TODO")


def analyzeProcedureDeclaration():
	global token

	print("Analyzing Proc declaration")
	token = lexical.getToken()
	# level
	if token["Symbol"] == "sidentificador":
		# searcj dec proc table
		# if not
		#insert table
		# generate
		#rot += 1
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sponto_virgula":
			analyzeBlock()
		else:
			error("an ;", token["Line"])
		#else error
	else:
		error("a Identifier", token["Line"])
	# back level


def analyzeFunctionDeclaration():
	global token

	print("Analyzing func declaration")
	token = lexical.getToken()
	print(token)
	# level
	if token["Symbol"] == "sidentificador":
		# searcj dec func table
		# if not
		#insert table
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sdoispontos":
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sinteiro" or token["Symbol"] == "sbooleano":
				# if sinteiro type in table is func inteiro
				# else func bool
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sponto_virgula":
					analyzeBlock()
			else:
				error("'inteiro' or 'booleano'", token["Line"])
		else:
			error("an :", token["Line"])
		#else error
	else:
		error("a Identifier", token["Line"])
	# back level



def analyzeCommand():
	global token

	print("Analyzing cmd")
	if token["Symbol"] == "sinicio":
		token = lexical.getToken()
		print(token)
		analyzeSimpleCommand()
		while token["Symbol"] != "sfim":
			if token["Symbol"] == "sponto_virgula":
				token = lexical.getToken()
				print(token)
				if token["Symbol"] != "sfim":
					analyzeSimpleCommand()
				else:
					token = lexical.getToken()
					print(token)
					break
			else:
				error("an ;", token["Line"])
			if token["Symbol"] == "sfim":
				token = lexical.getToken()
				print(token)
				break
			if token["Symbol"] != "sponto_virgula" :
				token = lexical.getToken()
				print(token)
		if token["Symbol"] != "sponto" and token["Symbol"] != "sponto_virgula":
			error("'fim'", token["Line"])

	else:
		error("'inicio'", token["Line"])


def analyzeSimpleCommand():
	global token

	print("Analyzing simple cmd")
	if token["Symbol"] == "sidentificador":
		analyzeProcedureAssignment()
	elif token["Symbol"] == "sse":
		analyzeIf()
	elif token["Symbol"] == "senquanto":
		analyzeWhile()
	elif token["Symbol"] == "sleia":
		analyzeRead()
	elif token["Symbol"] == "sescreva":
		analyzeWrite()
	else:
		analyzeCommand()


def analyzeProcedureAssignment():
	global token

	print("Analyzing Proc Assignment")
	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "satribuicao":
		analyzeAssignment()
	else:
		analyzeProcedureCall()


def analyzeAssignment():
	global token

	print("Analyzing Assignment")
	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sidentificador" or token["Symbol"] == "snumero":
		token = lexical.getToken()
		print(token)
		analyzeExpression()
	else:
		error("a Identifier or Number",token["Line"])

def analyzeProcedureCall():
	global token

	print("Analyzing proc call")
	token = lexical.getToken()
	print(token)


def analyzeRead():
	global token

	print("Analyzing read")
	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			# search declaration in the table
			#search all table
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sfecha_parenteses":
				token = lexical.getToken()
				print(token)
			else:
				error("an )", token["Line"])
			# error
		else:
			error("a Identifier", token["Line"])
	else:
		error("an (", token["Line"])


def analyzeWrite():
	global token

	print("Analyzing write")
	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			# search declaration var func
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sfecha_parenteses":
				token = lexical.getToken()
				print(token)
			else:
				error("an )", token["Line"])
			# error
		else:
			error("a Identifier", token["Line"])
	else:
		error("an (", token["Line"])


def analyzeWhile():
	global token
	# auxrot1, auxrot2
	print("Analyzing while")
	#auxrot1 = rotulo
	# generate label
	token = lexical.getToken()
	print(token)
	analyzeExpression()
	if token["Symbol"] == "sfaca":
		#auxrot2 = rot
		# generate label
		#rot += 1
		token = lexical.getToken()
		print(token)
		analyzeSimpleCommand()
		# generate
		#generate
	else:
		eerror("'faca'", token["Line"])


def analyzeIf():
	global token

	print("Analyzing if")
	token = lexical.getToken()
	print(token)
	analyzeExpression()
	if token["Symbol"] == "sentao":
		token = lexical.getToken()
		print(token)
		analyzeSimpleCommand()
		if token["Symbol"] == "sentao":
			token = lexical.getToken()
			print(token)
			analyzeSimpleCommand()
	else:
		error("'entao'", token["Line"])


def analyzeExpression():
	global token

	print("Analyzing Expression")
	analyzeSimpleExpression()
	if token["Symbol"] == "smaior" or token["Symbol"] == "smaiorig" or token["Symbol"] == "sigual" or token["Symbol"] == "smenor" or token["Symbol"] == "smenorig" or token["Symbol"] == "sdif":
		token = lexical.getToken()
		print(token)
		analyzeSimpleExpression()


def analyzeSimpleExpression():
	global token

	print("Analyzing simple expression")
	if token["Symbol"] == "smais" or token["Symbol"] == "smenos":
		token = lexical.getToken()
		print(token)
		analyzeTerm()
		while token["Symbol"] == "smais" or token["Symbol"] == "smenos" or token["Symbol"] == "sou":
			token = lexical.getToken()
			print(token)
			analyzeTerm()


def analyzeTerm():
	global token
	print("Analyzing term")
	analyzeFactor()
	while token["Symbol"] == "smult" or token["Symbol"] == "sdiv" or token["Symbol"] == "se":
		token = lexical.getToken()
		print(token)
		analyzeFactor()


def analyzeFactor():
	global token
	print("Analyzing factor")
	if token["Symbol"] == "sidentificador":
		# search table
		# if func inteiro or func bool
		analyzeFunctionCall()
		#else token
		#else error
	elif token["Symbol"] == "snumero":
		token = lexical.getToken()
		print(token)
	elif token["Symbol"] == "snao":
		token = lexical.getToken()
		print(token)
		analyzeFactor()
	elif token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		analyzeExpression()
		if token["Symbol"] == "sfecha_parenteses":
			token = lexical.getToken()
			print(token)
		else:
			error("an )", token["Line"])
	elif token["Symbol"] == "sverdadeiro" or token["Symbol"] == "sfalso":
		token = lexical.getToken()
		print(token)
	else:
		error("a Identifier, or Number, or 'nao', or (, or 'verdadeiro', or 'false'", token["Line"])


def analyzeFunctionCall():
	global token

	print("Analyzing function call")
	token = lexical.getToken()
	print(token)




def error(string,line):
    print("Found a error: Expected " + string + " in line " + str(line))
    exit()
