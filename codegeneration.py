# Projeto Compilador - Gerador de Codigo
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import lexical


commandsVM = []

# def main():
#     global commandsVM
#
#     generate(None,"START",None,None)
#     generate(None,"ALLOC",0,2)
#     generate(None,"JMP",1,None)
#     generate(2,"NULL",None,None)
#     generate(None,"ALLOC",2,1)
#     generate(None,"LDV",0,None)
#     generate(None,"STR",2,None)
#     generate(None,"LDV",0,None)
#     generate(None,"LDC",1,None)
#     generate(None,"SUB",None,None)
#     generate(None,"STR",0,None)
#     generate(None,"LDV",2,None)
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
            commandsVM.append(command + " " + str(arg1))
        elif command == "PRN":
            commandsVM.append(command + " " + str(arg1))
        elif command == "CALL":
            commandsVM.append(command + " " + str(arg1))
        elif command == "LDC":
            commandsVM.append(command + " " + str(arg1))
        elif command == "LDV":
            commandsVM.append(command + " " + str(arg1))
        elif command == "ALLOC":
            commandsVM.append(command + " " + str(arg1) + "," + str(arg2))
        elif command == "DALLOC":
            commandsVM.append(command + " " + str(arg1) + "," + str(arg2))
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
        elif command == "CMDIF":
            commandsVM.append(command)
        elif command == "CMDEQ":
            commandsVM.append(command)
        elif command == "CMAQ":
            commandsVM.append(command)
        elif command == "START":
            commandsVM.append(command)
        elif command == "HLT":
            commandsVM.append(command)
        elif command == "RETURN":
            commandsVM.append(command)


def makeObject(name):
    global commandsVM

    fileName = name + ".obj"
    f = open(fileName,"w")
    for line in commandsVM:
         f.write(line + "\n")
    f.close()
