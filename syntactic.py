# Projeto Compilador - Analisador Sintatico
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import lexical
import codegeneration


token = {}
label = 1

def analyzeBlock():
	global token

	token = lexical.getToken()
	print(token)
	analyzeVarDeclaration()
	analyzeSubRoutine()
	analyzeCommand()



def analyzeVarDeclaration():
	global token

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

	while True:
		if token["Symbol"] == "sidentificador":
			if not symboltable.searchVarDuplicity(token["Lexeme"]):
				symboltable.insert(token["Lexeme"],"variavel")
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
			else:
				print("FOUND duplicity")
		else:
			error("an Identifier", token["Line"])

		if token["Symbol"] == "sdoispontos":
			break
	token = lexical.getToken()
	print(token)
	analyzeType()


def analyzeType():
	global token

	if token["Symbol"] != "sinteiro" and token["Symbol"] != "sbooleano":
		error("'inteiro' or 'booleano'",token["Line"])
	else:
		symboltable.insertType(token["Lexeme"])
	token = lexical.getToken()
	print(token)


def analyzeSubRoutine():
	global token
	global label

	flag = 0
	if token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		auxLabel = label
		codegeneration.generate(None,"JMP",label,None)
		label += 1
		flag = 1
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
		codegeneration.generate(auxLabel,"NULL",None,None)


def analyzeProcedureDeclaration():
	global token

	token = lexical.getToken()
	level = "L"
	if token["Symbol"] == "sidentificador":
		if not symboltable.searchProcDeclaration(token["Lexeme"]):
			symboltable.insert(token["Lexeme"],"procedimento",level,label)
			codegeneration.generate(label,"NULL",None,None)
			label += 1
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sponto_virgula":
				analyzeBlock()
			else:
				error("an ;", token["Line"])
		else:
			print("Proc Declared")
	else:
		error("a Identifier", token["Line"])
	symboltable.restoreLevel()


def analyzeFunctionDeclaration():
	global token

	token = lexical.getToken()
	print(token)
	level = "L"
	if token["Symbol"] == "sidentificador":
		if not symboltable.searchFuncDeclaration(token["Lexeme"]):
			symboltable.insert(token["Lexeme"],None,level,label)
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sdoispontos":
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sinteiro" or token["Symbol"] == "sbooleano":
					if token["Symbol"] == "sinteiro":
						symboltable.defineFuncType("inteiro")
					else:
						symboltable.defineFuncType("booleano")
					token = lexical.getToken()
					print(token)
					if token["Symbol"] == "sponto_virgula":
						analyzeBlock()
				else:
					error("'inteiro' or 'booleano'", token["Line"])
			else:
				error("an :", token["Line"])
		else:
			print("Func declared")
	else:
		error("a Identifier", token["Line"])
	symboltable.restoreLevel()


def analyzeCommand():
	global token


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

	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "satribuicao":
		analyzeAssignment()
	else:
		analyzeProcedureCall()


def analyzeAssignment():
	global token

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


	token = lexical.getToken()
	print(token)


def analyzeRead():
	global token

	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			if symboltable.searchVarDeclaration(token["Lexeme"]):
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sfecha_parenteses":
					token = lexical.getToken()
					print(token)
				else:
					error("an )", token["Line"])
			else:
				print("Var no declared")
		else:
			error("a Identifier", token["Line"])
	else:
		error("an (", token["Line"])


def analyzeWrite():
	global token


	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			if symboltable.searchVarFuncDeclaration(token["Lexeme"]):
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sfecha_parenteses":
					token = lexical.getToken()
					print(token)
				else:
					error("an )", token["Line"])
			else:
				print("Var Func not declared")
		else:
			error("a Identifier", token["Line"])
	else:
		error("an (", token["Line"])


def analyzeWhile():
	global token
	global label

	auxLabel1 = label
	codegeneration.generate(label,"NULL",None,None)
	label += 1
	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sidentificador" or token["Symbol"] == "snumero":
		token = lexical.getToken()
		print(token)
		analyzeExpression()
	else:
		error("a Identifier or Number",token["Line"])
	if token["Symbol"] == "sfaca":
		auxLabel2 = label
		codegeneration.generate(None,"JMPF",label,None)
		label += 1
		token = lexical.getToken()
		print(token)
		analyzeSimpleCommand()
		codegeneration.generate(None,"JMP",auxLabel1,None)
		codegeneration.generate(auxLabel2,"NULL",None,None)
	else:
		error("'faca'", token["Line"])


def analyzeIf():
	global token

	print("Analyzing if")
	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sidentificador" or token["Symbol"] == "snumero":
		token = lexical.getToken()
		print(token)
		analyzeExpression()
	else:
		error("a Identifier or Number",token["Line"])
	if token["Symbol"] == "sentao":
		token = lexical.getToken()
		print(token)
		analyzeSimpleCommand()
		if token["Symbol"] == "ssenao":
			token = lexical.getToken()
			print(token)
			analyzeSimpleCommand()
	else:
		error("'entao'", token["Line"])


def analyzeExpression():
	global token

	analyzeSimpleExpression()
	if token["Symbol"] == "smaior" or token["Symbol"] == "smaiorig" or token["Symbol"] == "sigual" or token["Symbol"] == "smenor" or token["Symbol"] == "smenorig" or token["Symbol"] == "sdif":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador" or token["Symbol"] == "snumero":
			token = lexical.getToken()
			print(token)
			analyzeSimpleExpression()
		else:
			error("a Identifier or Number",token["Line"])


def analyzeSimpleExpression():
	global token

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

	analyzeFactor()
	while token["Symbol"] == "smult" or token["Symbol"] == "sdiv" or token["Symbol"] == "se":
		token = lexical.getToken()
		print(token)
		analyzeFactor()


def analyzeFactor():
	global token

	if token["Symbol"] == "sidentificador":
		if symboltable.search(token["Lexeme"],level,ind):
			if symboltable.get(ind)["Type"] == "booleano" or if symboltable.get(ind)["Type"] == "inteiro":
				analyzeFunctionCall()
			else:
				token = lexical.getToken()
		else:
			print("Not in table")
	elif token["Symbol"] == "snumero":
		token = lexical.getToken()
		print(token)
	elif token["Symbol"] == "snao":
		token = lexical.getToken()
		print(token)
		analyzeFactor()
	elif token["Symbol"] == "sabre_parenteses":
		print("ok")
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


	token = lexical.getToken()
	print(token)




def error(string,line):
    print("Found a error: Expected " + string + " in line " + str(line))
    exit()
