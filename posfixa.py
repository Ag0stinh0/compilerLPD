# Projeto Compilador - Pós-fixa
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

symbolList = []
symbolVerify = ["+", "-", "*", ">", "<", "=", "<=", ">=", "!=", "ou", "e", "div", "falso", "verdadeiro", "(", ")", "-u", "+u", "nao"]
firstPriorityVerify = ["-u", "+u", "nao"]
secondPriorityVerify = ["*", "div"]
thirdPriorityVerify = ["+", "-"]
fourthPriorityVerify = [">", "<", "=", "<=", ">=", "!="]

def getPosFixa(expression):
	global list
	global symbolList
	resultList = []

	if len(expression) != 1:
		resultList = organizeList(expression)
	else:
		resultList.append(expression[0])

	return resultList

def organizeList(expression):
	global symbolList
	resultList = []

	for position in range(0,len(expression)):
		if expression[position] in symbolVerify:
			if len(symbolList) == 0:
				symbolList.append(expression[position])
			else:
				if expression[position] in secondPriorityVerify:
					secondPriority(resultList)
				elif expression[position] in thirdPriorityVerify:
					thirdPriority(resultList)
				elif expression[position] in fourthPriorityVerify:
					fourthPriority(resultList)
				elif expression[position] == "e":
					fifthPriority(resultList)
				elif expression[position] == "ou":
					sixthPriority(resultList)

				if expression[position] == ")":
					consumeParentheses(resultList)
				else:
					symbolList.append(expression[position])
		else:
			resultList.append(expression[position])

	if len(symbolList) != 0:
		cleanSymbolList(resultList)

	return resultList

def consumeParentheses(resultList):
	global symbolList

	aux = len(symbolList)-1
	while symbolList[aux] != "(":
		resultList.append(symbolList[aux])
		symbolList.pop()
		aux -= 1
	symbolList.pop()

def cleanSymbolList(resultList):
	global symbolList

	aux = len(symbolList)-1
	while aux >= 0:
		resultList.append(symbolList[aux])
		symbolList.pop()
		aux -= 1

def secondPriority(resultList):
	global symbolList

	aux = len(symbolList)-1
	while aux >= 0:
		if symbolList[aux] == "(":
			break
		elif symbolList[aux] in firstPriorityVerify:
			resultList.append(symbolList[aux])
			symbolList.pop()
		aux -= 1

def thirdPriority(resultList):
	global symbolList

	aux = len(symbolList)-1
	while aux >= 0:
		if symbolList[aux] == "(":
			break
		elif symbolList[aux] in firstPriorityVerify or symbolList[aux] in secondPriorityVerify:
			resultList.append(symbolList[aux])
			symbolList.pop()
		aux -= 1

def fourthPriority(resultList):
	global symbolList

	aux = len(symbolList)-1
	while aux >= 0:
		if symbolList[aux] == "(":
			break
		elif symbolList[aux] in firstPriorityVerify or symbolList[aux] in secondPriorityVerify or symbolList[aux] in thirdPriorityVerify:
			resultList.append(symbolList[aux])
			symbolList.pop()
		aux -= 1

def fifthPriority(resultList):
	global symbolList

	aux = len(symbolList)-1
	while aux >= 0:
		if symbolList[aux] == "(":
			break
		elif symbolList[aux] in firstPriorityVerify or symbolList[aux] in secondPriorityVerify or symbolList[aux] in thirdPriorityVerify or symbolList[aux] in fourthPriorityVerify:
			resultList.append(symbolList[aux])
			symbolList.pop()
		aux -= 1

def sixthPriority(resultList):
	global symbolList

	aux = len(symbolList)-1
	while aux >= 0:
		if symbolList[aux] == "(":
			break
		elif symbolList[aux] in firstPriorityVerify or symbolList[aux] in secondPriorityVerify or symbolList[aux] in thirdPriorityVerify or symbolList[aux] in fourthPriorityVerify or symbolList[aux] == "e":
			resultList.append(symbolList[aux])
			symbolList.pop()
		aux -= 1
