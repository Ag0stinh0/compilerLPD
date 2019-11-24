# Projeto Compilador - Main
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import argparse
import lexical
import syntactic
import codegeneration
import symboltable

def main():
    filePath,objPath = argsParser()
    lexical.getFile(filePath)

    token = lexical.getToken()
    codegeneration.generate(None,"START",None,None)
    if token["Symbol"] == "sprograma":
        token = lexical.getToken()
        if token["Symbol"] == "sidentificador":
            symboltable.insert(token["Lexeme"],"program",0,None,None)
            token = lexical.getToken()
            if token["Symbol"] == "sponto_virgula":
                syntactic.analyzeBlock()
                token = lexical.getToken()
                if token != "End":
                    if token["Symbol"] == "sponto":
                        token = lexical.getToken()
                        if token == "End":
                            codegeneration.generate(None,"DALLOC",0,syntactic.toAlloc)
                            codegeneration.generate(None,"HLT",None,None)
                        else:
                            error("the end of file", token["Line"])
                    else:
                        error(".", token["Line"])
                else:
                    print("Found an error: Expected . to finish the program!")
            else:
                error("an ;", token["Line"])
        else:
            error("an Identifier", token["Line"])
    else:
        error("programa", token["Line"])
    codegeneration.makeObject(objPath)


def argsParser():
    parser = argparse.ArgumentParser(description="Simple compiler")
    parser.add_argument('path', help = "path to the file")
    parser.add_argument('destination', help = "name of object file")
    args = parser.parse_args()

    if args.path == None or args.destination == None:
        print ("Usage: compiler.py <path_to_file> <obj_file>")
        exit()
    else:
        return args.path,args.destination

def error(string,line):
    print("Found an error: Expected " + string + " in line " + str(line))
    exit()

if __name__ == '__main__':
    main()
