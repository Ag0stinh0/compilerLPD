# Projeto Compilador - Analisador Sintatico
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import lexical
import codegeneration
import symboltable
import posfixa

scope = 0
token = {}
label = 1
expression = []
symbolVerify = ["+", "-", "*", ">", "<", "=", "<=", ">=", "!=", "ou", "e", "div"]
especialSymbol = ["-u", "+u", "nao"]
resultTypeInteger = ["+", "-", "*", "div"]
resultTypeBoolean = [">", "<", "=", "<=", ">=", "!="]
verifyForBoolean = ["=", "!=", "ou", "e"]

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
	global scope

	while True:
		if token["Symbol"] == "sidentificador":
			if not symboltable.searchDuplicity(token["Lexeme"],scope):
				symboltable.insert(token["Lexeme"],"variable",scope,True)
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
				errorTable(token["Lexeme"], token["Line"])
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
		symboltable.insertVarType(token["Lexeme"])
	token = lexical.getToken()
	print(token)

def analyzeSubRoutine():
	global token
	global label

	flag = 0
	#if token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		#auxLabel = label
		#codegeneration.generate(None,"JMP",label,None)
		#label += 1
		#flag = 1
	while token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		if token["Symbol"] == "sprocedimento":
			analyzeProcedureDeclaration()
		else:
			analyzeFunctionDeclaration()
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sponto_virgula":
			symboltable.seeAllTable()
			token = lexical.getToken()
			print(token)
		else:
			error("an ;", token["Line"])
	if flag == 1:
		codegeneration.generate(auxLabel,"NULL",None,None)

def analyzeProcedureDeclaration():
	global token
	global scope

	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sidentificador":
		if not symboltable.searchDuplicity(token["Lexeme"],scope):
			symboltable.insert(token["Lexeme"],"procedure",scope,None)
			scope += 1
			#codegeneration.generate(label,"NULL",None,None)
			#label += 1
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sponto_virgula":
				analyzeBlock()
			else:
				error("an ;", token["Line"])
		else:
			errorTable(token["Lexeme"], token["Line"])
	else:
		error("a Identifier", token["Line"])
	symboltable.seeAllTable()
	symboltable.restoreLevel(scope)
	scope -= 1

def analyzeFunctionDeclaration():
	global token
	global scope

	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sidentificador":
		if not symboltable.searchDuplicity(token["Lexeme"],scope):
			symboltable.insert(token["Lexeme"],"function",scope,None)
			scope += 1
			token = lexical.getToken()
			print(token)
			if token["Symbol"] == "sdoispontos":
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sinteiro" or token["Symbol"] == "sbooleano":
					if token["Symbol"] == "sinteiro":
						symboltable.insertFuncType("inteiro")
					else:
						symboltable.insertFuncType("booleano")
					token = lexical.getToken()
					print(token)
					if token["Symbol"] == "sponto_virgula":
						analyzeBlock()
					else:
						error("an ;",token["Line"])
				else:
					error("'inteiro' or 'booleano'", token["Line"])
			else:
				error("an :", token["Line"])
		else:
			errorTable(token["Lexeme"],token["Line"])
	else:
		error("a Identifier", token["Line"])
	symboltable.seeAllTable()
	symboltable.restoreLevel(scope)
	scope -= 1

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
				error("an ;", token["Line"])
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
		if token["Symbol"] == "sfim":
			token = lexical.getToken()
			print(token)

def analyzeProcedureAssignment():
	global token

	if symboltable.isVariable(token["Lexeme"]):
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "satribuicao":
			analyzeAssignment()
		else:
			error("a :=", token["Line"])
	else:
		#Is it right pass functions in this case?
		if symboltable.isProcedure(token["Lexeme"]):
			token = lexical.getToken()
			print(token)
			#analyzeProcedureCall()
		else:
			print("Found an error: " + token["Lexeme"] + " was not declared as variable or procedure")
			exit()

def analyzeAssignment():
	global token
	global expression

	token = lexical.getToken()
	print(token)
	analyzeExpression()
	print("\n Expression:")
	print(expression)
	print("")
	posfixa.getPosFixa(expression)
	expression.clear()

# It is necessary think what happened here
# def analyzeProcedureCall():

def analyzeRead():
	global token

	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			if symboltable.hasIdentifier(token["Lexeme"]):
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sfecha_parenteses":
					token = lexical.getToken()
					print(token)
				else:
					error("a )", token["Line"])
			else:
				print("Found an error: " + token["Lexeme"] + " was not declared as variable or function")
				exit()
		else:
			error("an identifier", token["Line"])
	else:
		error("a (", token["Line"])

def analyzeWrite():
	global token

	token = lexical.getToken()
	print(token)
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		print(token)
		if token["Symbol"] == "sidentificador":
			if symboltable.isVariable(token["Lexeme"]):
				token = lexical.getToken()
				print(token)
				if token["Symbol"] == "sfecha_parenteses":
					token = lexical.getToken()
					print(token)
				else:
					error("a )", token["Line"])
			else:
				print("Found an error: " + token["Lexeme"] + " was not declared as variable")
				exit()
		else:
			error("an identifier", token["Line"])
	else:
		error("a (", token["Line"])

def analyzeWhile():
	global token
	global label
	global expression

	#auxLabel1 = label
	#codegeneration.generate(label,"NULL",None,None)
	#label += 1
	token = lexical.getToken()
	print(token)
	analyzeExpression()
	print("\n Expression:")
	print(expression)
	print("")
	expressionPosFixa = posfixa.getPosFixa(expression)
	validateContentExpression(expressionPosFixa)
	expression.clear()
	if token["Symbol"] == "sfaca":
		#auxLabel2 = label
		#codegeneration.generate(None,"JMPF",label,None)
		#label += 1
		token = lexical.getToken()
		print(token)
		analyzeSimpleCommand()
		#codegeneration.generate(None,"JMP",auxLabel1,None)
		#codegeneration.generate(auxLabel2,"NULL",None,None)
	else:
		error("'faca'", token["Line"])

def analyzeIf():
	global token
	global expression

	token = lexical.getToken()
	print(token)
	analyzeExpression()
	print("\n Expression:")
	print(expression)
	print("")
	expressionPosFixa = posfixa.getPosFixa(expression)
	validateContentExpression(expressionPosFixa)
	expression.clear()
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
	global expression

	analyzeSimpleExpression()
	if token["Symbol"] == "smaior" or token["Symbol"] == "smaiorig" or token["Symbol"] == "sigual" or token["Symbol"] == "smenor" or token["Symbol"] == "smenorig" or token["Symbol"] == "sdif":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
		analyzeSimpleExpression()

def analyzeSimpleExpression():
	global token
	global expression

	if token["Symbol"] == "smais" or token["Symbol"] == "smenos":
		expression.append(token["Lexeme"] + "u")
		token = lexical.getToken()
		print(token)
	analyzeTerm()
	while token["Symbol"] == "smais" or token["Symbol"] == "smenos" or token["Symbol"] == "sou":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
		analyzeTerm()

def analyzeTerm():
	global token
	global expression

	analyzeFactor()
	while token["Symbol"] == "smult" or token["Symbol"] == "sdiv" or token["Symbol"] == "se":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
		analyzeFactor()

def analyzeFactor():
	global token
	global expression

	if token["Symbol"] == "sidentificador":
		expression.append(token["Lexeme"])
		if symboltable.hasIdentifier(token["Lexeme"]):
			if symboltable.isFunctionCall(token["Lexeme"]):
				analyzeFunctionCall()
			else:
				token = lexical.getToken()
				print(token)
		else:
			print("Found an error: " + token["Lexeme"] + " was not declared as variable or function")
			exit()
	elif token["Symbol"] == "snumero":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
	elif token["Symbol"] == "snao":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
		analyzeFactor()
	elif token["Symbol"] == "sabre_parenteses":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
		analyzeExpression()
		if token["Symbol"] == "sfecha_parenteses":
			expression.append(token["Lexeme"])
			token = lexical.getToken()
			print(token)
		else:
			error("an )", token["Line"])
	elif token["Symbol"] == "sverdadeiro" or token["Symbol"] == "sfalso":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		print(token)
	else:
		error("a Identifier, or Number, or 'nao', or (, or 'verdadeiro', or 'false'", token["Line"])

def analyzeFunctionCall():
	global token

	token = lexical.getToken()
	print(token)
	
def validateContentExpression(expressionPosFixa):
	global token
	variableList = []
	typeResult = []
	
	for position in range(0,len(expressionPosFixa)):
		if expressionPosFixa[position] in symbolVerify:
			for count in range(0,2):
				if variableList[-1] == "inteiro" or variableList[-1] == "booleano":
					typeResult.append(variableList[-1])
				elif variableList[-1].isalpha():
					typeResult.append(symboltable.getType(variableList[-1]))
				else:
					typeResult.append("inteiro")
				variableList.pop()
			if typeResult[0] == "inteiro" and typeResult[1] == "inteiro":
				if expressionPosFixa[position] in resultTypeInteger:
					typeResult.clear()
					variableList.append("inteiro")
				elif expressionPosFixa[position] in resultTypeBoolean:
					typeResult.clear()
					variableList.append("booleano")
				else:
					errorExpression(token["Line"])
			elif typeResult[0] == "booleano" and typeResult[1] == "booleano":
				if expressionPosFixa[position] in verifyForBoolean:
					typeResult.clear()
					variableList.append("booleano")
				else:
					errorExpression(token["Line"])
			else:
				errorExpression(token["Line"])
		elif expressionPosFixa[position] in especialSymbol:
			if expressionPosFixa[position] == "nao":
				if variableList[-1] == "booleano":
					variableList.pop()
					variableList.append("booleano")
				elif variableList[-1] == "inteiro":
					errorExpression(token["Line"])
				elif variableList[-1].isalpha():
					if symboltable.getType(variableList[-1]) == "booleano":
						variableList.pop()
						variableList.append("booleano")
					else:
						errorExpression(token["Line"])
				else:
					errorExpression(token["Line"])
			else:
				if variableList[-1] == "booleano":
					errorExpression(token["Line"])
				elif variableList[-1] == "inteiro":
					variableList.pop()
					variableList.append("inteiro")
				elif variableList[-1].isalpha():
					if symboltable.getType(variableList[-1]) == "booleano":
						errorExpression(token["Line"])
					else:
						variableList.pop()
						variableList.append("inteiro")
				else:
					variableList.pop()
					variableList.append("inteiro")
		else:
			variableList.append(expressionPosFixa[position])
	if variableList[0] == "inteiro":
		errorExpression(token["Line"])
	else:
		print("Expression Validate\n")

def error(string,line):
    print("Found an error: Expected " + string + " in line " + str(line))
    exit()

def errorTable(string,line):
	print("Found an error: Duplicity " + string + " in line " + str(line))
	exit()

def errorExpression(line):
	print("Found an error: Wrong type variable to resolve the expression in line " + str(line))
	exit()
