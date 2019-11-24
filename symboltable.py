# Projeto Compilador - Tabela de Simbolos
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679


table = []
index = 0

def searchDuplicity(lexeme, level):
    global table

    for i in range(0,len(table)):
        if table[i]["Lexeme"] == lexeme:
            if table[i]["Level"] == level:
                return True
    return False

def insert(lexeme,name,level,label,memory):
    global table

    if label == None:
        if name == "program":
            symbol = {"Lexeme":lexeme,"Name":name,"Level":level}
        else:
            symbol = {"Lexeme":lexeme,"Name":name,"Level":level,"Type":None,"Memory":memory}
    else:
        if name == "procedure":
            symbol = {"Lexeme":lexeme,"Name":name,"Level":level,"Label":label}
        else:
            symbol = {"Lexeme":lexeme,"Name":name,"Level":level,"Label":label,"Type":None}
    table.append(symbol)


def insertVarType(type):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "variable":
            if table[i]["Type"] == None and table[i]["Name"] == "variable":
                table[i]["Type"] = type

def insertFuncType(type):
    global table

    table[len(table) - 1]["Type"] = type

def restoreLevel(level):
    global table

    countDalloc = 0
    position = len(table) - 1
    while True:
        if table[position]["Level"] == level:
            table.pop()
            countDalloc += 1
            position -= 1
        else:
            return countDalloc

def hasIdentifier(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable":
                return True,table[position]["Name"],table[position]["Memory"]
            elif table[position]["Name"] == "function":
                return True,table[position]["Name"],table[position]["Label"]
        position -= 1
    return False,None,None
	
def hasAssignment(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable":
                return True,table[position]["Name"],table[position]["Memory"],table[position]["Type"],None
            elif table[position]["Name"] == "function":
                return True,table[position]["Name"],None,table[position]["Type"],table[position]["Lexeme"]
        position -= 1
    return False,None,None,None,None

def getPosition(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable":
                return table[position]["Memory"]
        position -= 1

def isFunctionCall(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "function":
                return True
        position -= 1
    return False

def isVariable(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable":
                return True,table[position]["Memory"],table[position]["Type"]
        position -= 1
    return False,None,None

def isProcedure(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "procedure":
                return True,table[position]["Label"]
        position -= 1
    return False,None

def getType(lexeme):
    global table

    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable" or table[position]["Name"] == "function":
                return table[position]["Type"]
        position -= 1
