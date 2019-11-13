# Projeto Compilador - Tabela de Simbolos
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679


table = []
index = 0


def searchVarDeclaration(lexeme):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "variavel":
            if table[i]["Lexeme"] == lexeme:
                return True
    return False


def searchVarDuplicity(lexeme):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "variavel":
            if table[i]["Lexeme"] == lexeme:
                return True
    return False


def searchVarFuncDeclaration(x):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "variavel":
            if table[i]["Lexeme"] == lexeme:
                return True
    return False


def insert(lexeme,name,level,label):
    global table

    symbol = {"Lexeme":lexeme,"Name":name,"Level":level,"Label":label,"Memory":None}
    if name == "variavel":
        symbol["Type"] = None
    table.append(symbol)


def defineType(type):
    global table
    global index

    for i in range(0,len(table)):
        if table[i]["Name"] == "variavel":
            if table[i]["Type"] == None:
                table[i]["Type"] = type



def searchProcDeclaration(lexeme):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "procedimento":
            if table[i]["Lexeme"] == lexeme:
                return True
    return False


def restoreLevel():
    global table

    aux = len(table) - 1
    while True:
        if table[aux]["Level"] == "L":
            table.pop()
            aux -= 1
        else:
            break


def searchFuncDeclaration(x):
    global table

    for i in range(0,len(table)):
        if table[i]["Name"] == "procedimento":
            if table[i]["Lexeme"] == lexeme:
                return True
    return False


def defineFuncType(type):
    global table

    table[len(table) - 1]["Type"] = type


def search(lexeme,level):
    ind = 0
    global table
    ## CHANGE IN THE syntactic ##
    for i in range(0,len(table)):
        if table[i]["Name"] == "procedimento":
            if table[i]["Lexeme"] == lexeme:
                ind = i
                return ind
    return -1


def get(ind):
    global table

    return table[ind]["Type"]


def main():
    global table
    token = {}
    token["Lexeme"] = "namaiejdoa"
    insert(token["Lexeme"],"nomedoprograma",None,None)
    token["Lexeme"] = "LOL"
    insert(token["Lexeme"],"variavel","L",None)
    token["Lexeme"] = "namaiejdoa"
    insert(token["Lexeme"],"nomedoprograma",None,None)
    token["Lexeme"] = "sinteiro"
    defineType(token["Lexeme"])
    for symbol in table:
        print (symbol)


if __name__ == '__main__':
    main()
