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

def insert(lexeme,name,level,label):
    global table
	
    if label == None:
        if name == "program" or name == "procedure":
            symbol = {"Lexeme":lexeme,"Name":name,"Level":level}
        else:
            symbol = {"Lexeme":lexeme,"Name":name,"Level":level,"Type":None}
    else:
        symbol = {"Lexeme":lexeme,"Name":name,"Level":level,"Type":None,"Memory":None}
    table.append(symbol)


def insertVarType(type):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "variable":
            if table[i]["Type"] == None:
                table[i]["Type"] = type
				
def insertFuncType(type):
    global table

    table[len(table) - 1]["Type"] = type

def restoreLevel(level):
    global table

    position = len(table) - 1
    while True:
        if table[position]["Level"] == level:
            table.pop()
            position -= 1
        else:
            break
			
def seeAllTable():
    global table
	
    print("")
    print("------- Symbol Table -------")
    for i in range(0,len(table)):
        print(table[i])
    print("")

def hasIdentifier(lexeme):
    global table
    
    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable" or table[position]["Name"] == "function":
                return True
        position -= 1
    return False
	
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
                return True
        position -= 1
    return False
	
def isProcedure(lexeme):
    global table
    
    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "procedure":
                return True
        position -= 1
    return False
	
def getType(lexeme):
    global table
    
    position = len(table) - 1
    while position >= 0:
        if table[position]["Lexeme"] == lexeme:
            if table[position]["Name"] == "variable" or table[position]["Name"] == "function":
                return table[position]["Type"]
        position -= 1
        
