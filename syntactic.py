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
toAlloc = 0
countAlloc = 0
listFunctionName = []
hasCallReturn = False
expression = []
symbolVerify = ["+", "-", "*", ">", "<", "=", "<=", ">=", "!=", "ou", "e", "div"]
especialSymbol = ["-u", "+u", "nao"]
resultTypeInteger = ["+", "-", "*", "div"]
resultTypeBoolean = [">", "<", "=", "<=", ">=", "!="]
verifyForBoolean = ["=", "!=", "ou", "e"]

def analyzeBlock():
	global token

	token = lexical.getToken()
	analyzeVarDeclaration()
	analyzeSubRoutine()
	analyzeCommand()

def analyzeVarDeclaration():
	global token
	global toAlloc
	global countAlloc

	countAlloc = 0
	if token["Symbol"] == "svar":
		old = toAlloc
		token = lexical.getToken()
		if token["Symbol"] == "sidentificador":
			while token["Symbol"] == "sidentificador":
				analyzeVar()
				if token["Symbol"] == "sponto_virgula":
					token = lexical.getToken()
				else:
					error("a ;",token["Line"])
			codegeneration.generate(None,"ALLOC",old,countAlloc)
		else:
			error("an Identifier",token["Line"])

def analyzeVar():
	global token
	global scope
	global toAlloc
	global countAlloc

	while True:
		if token["Symbol"] == "sidentificador":
			if not symboltable.searchDuplicity(token["Lexeme"],scope):
				symboltable.insert(token["Lexeme"],"variable",scope,None,toAlloc)
				countAlloc += 1
				toAlloc += 1
				token = lexical.getToken()
				if token["Symbol"] == "svirgula" or token["Symbol"] == "sdoispontos":
					if token["Symbol"] == "svirgula":
						token = lexical.getToken()
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
	analyzeType()

def analyzeType():
	global token

	if token["Symbol"] != "sinteiro" and token["Symbol"] != "sbooleano":
		error("'inteiro' or 'booleano'",token["Line"])
	else:
		symboltable.insertVarType(token["Lexeme"])
	token = lexical.getToken()

def analyzeSubRoutine():
	global token
	global label
	global toAlloc

	flag = 0
	if token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		auxLabel = label
		codegeneration.generate(None,"JMP",label,None)
		label += 1
		flag = 1
	while token["Symbol"] == "sprocedimento" or token["Symbol"] == "sfuncao":
		toAlloc += 1
		if token["Symbol"] == "sprocedimento":
			analyzeProcedureDeclaration()
		else:
			analyzeFunctionDeclaration()
		token = lexical.getToken()
		if token["Symbol"] == "sponto_virgula":
			token = lexical.getToken()
		else:
			error("an ;", token["Line"])
	if flag == 1:
		codegeneration.generate(auxLabel,"NULL",None,None)

def analyzeProcedureDeclaration():
	global token
	global scope
	global label
	global toAlloc

	token = lexical.getToken()
	if token["Symbol"] == "sidentificador":
		if not symboltable.searchDuplicity(token["Lexeme"],scope):
			symboltable.insert(token["Lexeme"],"procedure",scope,label,None)
			scope += 1
			codegeneration.generate(label,"NULL",None,None)
			label += 1
			token = lexical.getToken()
			if token["Symbol"] == "sponto_virgula":
				analyzeBlock()
			else:
				error("an ;", token["Line"])
		else:
			errorTable(token["Lexeme"], token["Line"])
	else:
		error("a Identifier", token["Line"])
	dalloc = symboltable.restoreLevel(scope)
	if dalloc != 0:
		codegeneration.generate(None,"DALLOC",(toAlloc-dalloc),dalloc)
		toAlloc = toAlloc - dalloc
	codegeneration.generate(None,"RETURN",None,None)
	toAlloc -= 1
	scope -= 1

def analyzeFunctionDeclaration():
	global token
	global scope
	global label
	global toAlloc
	global listFunctionName
	global hasCallReturn
	
	token = lexical.getToken()
	if token["Symbol"] == "sidentificador":
		listFunctionName.append(token["Lexeme"])
		if not symboltable.searchDuplicity(token["Lexeme"],scope):
			symboltable.insert(token["Lexeme"],"function",scope,label,None)
			scope += 1
			codegeneration.generate(label,"NULL",None,None)
			label += 1
			token = lexical.getToken()
			if token["Symbol"] == "sdoispontos":
				token = lexical.getToken()
				if token["Symbol"] == "sinteiro" or token["Symbol"] == "sbooleano":
					if token["Symbol"] == "sinteiro":
						symboltable.insertFuncType("inteiro")
					else:
						symboltable.insertFuncType("booleano")
					token = lexical.getToken()
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
		
	if hasCallReturn == False:
		errorFunction(listFunctionName[-1])
	listFunctionName.pop()
	dalloc = symboltable.restoreLevel(scope)
	if dalloc != 0:
		toAlloc = toAlloc - dalloc
	else:
		codegeneration.generate(None,"RETURNF",None,None)
	hasCallReturn = False
	toAlloc -= 1
	scope -= 1

def analyzeCommand():
	global token

	if token["Symbol"] == "sinicio":
		token = lexical.getToken()
		analyzeSimpleCommand()
		while token["Symbol"] != "sfim":
			if token["Symbol"] == "sponto_virgula":
				token = lexical.getToken()
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

def analyzeProcedureAssignment():
	global token
	global listFunctionName
	global hasCallReturn
	global toAlloc
	global countAlloc
	global hasCallReturn

	check,name,position,type,lexeme = symboltable.hasAssignment(token["Lexeme"])
	if check:
		if name == "function":
			if len(listFunctionName) != 0 and lexeme == listFunctionName[-1]:
				token = lexical.getToken()
				if token["Symbol"] == "satribuicao":
					analyzeAssignment(type)
					hasCallReturn = True
					if countAlloc != 0:
						codegeneration.generate(None,"RETURNF",(toAlloc-countAlloc),countAlloc)
					else:
						codegeneration.generate(None,"RETURNF",None,None)
				else:
					error("a :=", token["Line"])
			else:
				print("Found an error: It isn't possible assignment in line " + str(token["Line"]))
				exit()
		else:	
			token = lexical.getToken()
			if token["Symbol"] == "satribuicao":
				analyzeAssignment(type)
				if hasCallReturn == False:
					codegeneration.generate(None,"STR",position,None)
			else:
				error("a :=", token["Line"])
	else:
		check,label = symboltable.isProcedure(token["Lexeme"])
		if check:
			token = lexical.getToken()
			if hasCallReturn == False:
				codegeneration.generate(None,"CALL",label,None)
		else:
			print("Found an error: " + token["Lexeme"] + " was not declared as variable or procedure")
			exit()

def analyzeAssignment(type):
	global token
	global expression
	global hasCallReturn

	token = lexical.getToken()
	analyzeExpression()
	expressionPosFixa = posfixa.getPosFixa(expression)
	validateContentExpression(expressionPosFixa,type)
	if hasCallReturn == False:
		codegeneration.generatePos(expressionPosFixa)

	expression.clear()

def analyzeRead():
	global token
	global hasCallReturn

	token = lexical.getToken()
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		if token["Symbol"] == "sidentificador":
			check,position,type = symboltable.isVariable(token["Lexeme"])
			if check:
				if hasCallReturn == False:
					codegeneration.generate(None,"RD",None,None)
					codegeneration.generate(None,"STR",position,None)	
				token = lexical.getToken()
				if token["Symbol"] == "sfecha_parenteses":
					token = lexical.getToken()
				else:
					error("a )", token["Line"])
			else:
				print("Found an error: " + token["Lexeme"] + " was not declared as variable")
				exit()
		else:
			error("an identifier", token["Line"])
	else:
		error("a (", token["Line"])

def analyzeWrite():
	global token
	global hasCallReturn

	token = lexical.getToken()
	if token["Symbol"] == "sabre_parenteses":
		token = lexical.getToken()
		if token["Symbol"] == "sidentificador":
			check,name,position = symboltable.hasIdentifier(token["Lexeme"])
			if check:
				if hasCallReturn == False:
					if name == "function":
						codegeneration.generate(None,"CALL",position,None)
						codegeneration.generate(None,"PRN",None,None)
					else:
						codegeneration.generate(None,"LDV",position,None)
						codegeneration.generate(None,"PRN",None,None)
				token = lexical.getToken()
				if token["Symbol"] == "sfecha_parenteses":
					token = lexical.getToken()
				else:
					error("a )", token["Line"])
			else:
				print("Found an error: " + token["Lexeme"] + " was not declared as variable or function")
				exit()
		else:
			error("an identifier", token["Line"])
	else:
		error("a (", token["Line"])

def analyzeWhile():
	global token
	global label
	global expression
	global hasCallReturn

	auxLabel1 = label
	if hasCallReturn == False:
		codegeneration.generate(label,"NULL",None,None)
	label += 1
	token = lexical.getToken()
	analyzeExpression()
	expressionPosFixa = posfixa.getPosFixa(expression)
	validateContentExpression(expressionPosFixa,"booleano")
	if hasCallReturn == False:
		codegeneration.generatePos(expressionPosFixa)
	expression.clear()
	if token["Symbol"] == "sfaca":
		auxLabel2 = label
		if hasCallReturn == False:
			codegeneration.generate(None,"JMPF",label,None)
		label += 1
		token = lexical.getToken()
		analyzeSimpleCommand()
		if hasCallReturn == False:
			codegeneration.generate(None,"JMP",auxLabel1,None)
			codegeneration.generate(auxLabel2,"NULL",None,None)
	else:
		error("'faca'", token["Line"])

def analyzeIf():
	global token
	global label
	global expression
	global hasCallReturn

	token = lexical.getToken()
	analyzeExpression()
	expressionPosFixa = posfixa.getPosFixa(expression)
	validateContentExpression(expressionPosFixa,"booleano")
	if hasCallReturn == False:
		codegeneration.generatePos(expressionPosFixa)
	expression.clear()
	if token["Symbol"] == "sentao":
		auxLabel1 = label
		if hasCallReturn == False:
			codegeneration.generate(None,"JMPF",label,None)
		label += 1
		token = lexical.getToken()
		analyzeSimpleCommand()
		if token["Symbol"] == "ssenao":
			auxLabel2 = label
			if hasCallReturn == False:
				codegeneration.generate(None,"JMP",label,None)
			label += 1
			if hasCallReturn == False:
				codegeneration.generate(auxLabel1,"NULL",None,None)
			token = lexical.getToken()
			analyzeSimpleCommand()
			if hasCallReturn == False:
				codegeneration.generate(auxLabel2,"NULL",None,None)
		else:
			if hasCallReturn == False:
				codegeneration.generate(auxLabel1,"NULL",None,None)
	else:
		error("'entao'", token["Line"])

def analyzeExpression():
	global token
	global expression

	analyzeSimpleExpression()
	if token["Symbol"] == "smaior" or token["Symbol"] == "smaiorig" or token["Symbol"] == "sigual" or token["Symbol"] == "smenor" or token["Symbol"] == "smenorig" or token["Symbol"] == "sdif":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		analyzeSimpleExpression()

def analyzeSimpleExpression():
	global token
	global expression

	if token["Symbol"] == "smais" or token["Symbol"] == "smenos":
		expression.append(token["Lexeme"] + "u")
		token = lexical.getToken()
	analyzeTerm()
	while token["Symbol"] == "smais" or token["Symbol"] == "smenos" or token["Symbol"] == "sou":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		analyzeTerm()

def analyzeTerm():
	global token
	global expression

	analyzeFactor()
	while token["Symbol"] == "smult" or token["Symbol"] == "sdiv" or token["Symbol"] == "se":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		analyzeFactor()

def analyzeFactor():
	global token
	global expression

	if token["Symbol"] == "sidentificador":
		expression.append(token["Lexeme"])
		check,name,position = symboltable.hasIdentifier(token["Lexeme"])
		if check:
			token = lexical.getToken()
		else:
			print("Found an error: " + token["Lexeme"] + " was not declared as variable or function")
			exit()
	elif token["Symbol"] == "snumero":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
	elif token["Symbol"] == "snao":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		analyzeFactor()
	elif token["Symbol"] == "sabre_parenteses":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
		analyzeExpression()
		if token["Symbol"] == "sfecha_parenteses":
			expression.append(token["Lexeme"])
			token = lexical.getToken()
		else:
			error("an )", token["Line"])
	elif token["Symbol"] == "sverdadeiro" or token["Symbol"] == "sfalso":
		expression.append(token["Lexeme"])
		token = lexical.getToken()
	else:
		error("a Identifier, or Number, or 'nao', or (, or 'verdadeiro', or 'false'", token["Line"])
		
def validateContentExpression(expressionPosFixa,type):
	global token
	variableList = []
	typeResult = []
	
	if len(expressionPosFixa) != 1:
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
	else:
		if expressionPosFixa[0].isalpha():
			variableList.append(symboltable.getType(expressionPosFixa[-1]))
		else:
			variableList.append("inteiro")
	if variableList[0] != type:
		errorExpression(token["Line"])

def error(string,line):
    print("Found an error: Expected " + string + " in line " + str(line))
    exit()

def errorTable(string,line):
	print("Found an error: Duplicity " + string + " in line " + str(line))
	exit()
	
def errorFunction(string):
	print("Found an error: Not exist the return in function " + string)
	exit()

def errorExpression(line):
	print("Found an error: Wrong type variable to resolve the expression in line " + str(line))
	exit()
