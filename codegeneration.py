# Projeto Compilador - Gerador de Codigo
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import lexical
import symboltable

commandsVM = []
symbolVerify = ["+", "-", "*", ">", "<", "=", "<=", ">=", "!=", "ou", "e", "div","-u", "+u", "nao"]

# def main():
#     global commandsVM
#
#     generate(None,"START",None,None)
#     generate(None,"ALLOC",0,2)
#     generate(None,"JMP",1,None)
#     generate(2,"NULL",None,None)
#     generate(None,"ALLOC",2,1)
#     generate(None,"LDC",0,None)
#     generate(None,"STR",2,None)
#     generate(None,"LDC",0,None)
#     generate(None,"LDC",1,None)
#     generate(None,"SUB",None,None)
#     generate(None,"STR",0,None)
#     generate(None,"LDC",2,None)
#     # print(commandsVM)
#     makeObject()
#
# if __name__ == '__main__':
#     main()


def generate(label,command,arg1,arg2):
    global commandsVM

    if label != None:
        label = "L" + str(label)
        commandsVM.append(label + " " + command)
    else:
        if command == "JMP" or command == "JMPF":
            arg1 = "L" + str(arg1)
            commandsVM.append(command + " " + arg1)
        elif command == "STR":
            commandsVM.append(command + " " + str(arg1))
        elif command == "RD":
            commandsVM.append(command)
        elif command == "PRN":
            commandsVM.append(command)
        elif command == "CALL":
            arg1 = "L" + str(arg1)
            commandsVM.append(command + " " + arg1)
        elif command == "LDC":
            commandsVM.append(command + " " + str(arg1))
        elif command == "LDV":
            commandsVM.append(command + " " + str(arg1))
        elif command == "ALLOC":
            commandsVM.append(command + " " + str(arg1) + " " + str(arg2))
        elif command == "DALLOC":
            commandsVM.append(command + " " + str(arg1) + " " + str(arg2))
        elif command == "ADD":
            commandsVM.append(command)
        elif command == "SUB":
            commandsVM.append(command)
        elif command == "MULT":
            commandsVM.append(command)
        elif command == "DIVI":
            commandsVM.append(command)
        elif command == "INV":
            commandsVM.append(command)
        elif command == "AND":
            commandsVM.append(command)
        elif command == "OR":
            commandsVM.append(command)
        elif command == "NEG":
            commandsVM.append(command)
        elif command == "CME":
            commandsVM.append(command)
        elif command == "CMA":
            commandsVM.append(command)
        elif command == "CEQ":
            commandsVM.append(command)
        elif command == "CDIF":
            commandsVM.append(command)
        elif command == "CMEQ":
            commandsVM.append(command)
        elif command == "CMAQ":
            commandsVM.append(command)
        elif command == "START":
            commandsVM.append(command)
        elif command == "HLT":
            commandsVM.append(command)
        elif command == "RETURN":
            commandsVM.append(command)
        elif command == "RETURNF":
            if arg1 == None and arg2 == None:
                commandsVM.append(command)
            else:
                commandsVM.append(command + " " + str(arg1) + " " + str(arg2))

def generatePos(expressionPosFixa):
    
    if len(expressionPosFixa) != 1:
        for position in range(0,len(expressionPosFixa)):
            if expressionPosFixa[position] in symbolVerify:
                if expressionPosFixa[position] == "+":
                    generate(None,"ADD",None,None)
                elif expressionPosFixa[position] == "-":
                    generate(None,"SUB",None,None)
                elif expressionPosFixa[position] == "*":
                    generate(None,"MULT",None,None)
                elif expressionPosFixa[position] == "div":
                    generate(None,"DIVI",None,None)
                elif expressionPosFixa[position] == "ou":
                    generate(None,"OR",None,None)
                elif expressionPosFixa[position] == "e":
                    generate(None,"AND",None,None)
                elif expressionPosFixa[position] == ">":
                    generate(None,"CMA",None,None)
                elif expressionPosFixa[position] == "<":
                    generate(None,"CME",None,None)
                elif expressionPosFixa[position] == "=":
                    generate(None,"CEQ",None,None)
                elif expressionPosFixa[position] == ">=":
                    generate(None,"CMAQ",None,None)
                elif expressionPosFixa[position] == "<=":
                    generate(None,"CMEQ",None,None)
                elif expressionPosFixa[position] == "!=":
                    generate(None,"CDIF",None,None)
                elif expressionPosFixa[position] == "nao":
                    generate(None,"NEG",None,None)
                elif expressionPosFixa[position] == "-u":
                    generate(None,"INV",None,None)
            else:
                if expressionPosFixa[position].isalpha():
                    check,name,label = symboltable.hasIdentifier(expressionPosFixa[position])
                    if name == "function":
                        generate(None,"CALL",label,None)
                    else:
                        generate(None,"LDV",label,None)
                else:
                    generate(None,"LDC",expressionPosFixa[position],None)
    else:
        if expressionPosFixa[0].isalpha():
            check,name,label = symboltable.hasIdentifier(expressionPosFixa[0])
            if name == "function":
                generate(None,"CALL",label,None)
            else:
                generate(None,"LDV",label,None)
        else:
            generate(None,"LDC",expressionPosFixa[0],None)

def makeObject(name):
    global commandsVM

    fileName = name + ".obj"
    f = open(fileName,"w")
    for line in commandsVM:
         f.write(line + "\n")
    f.close()
