# Projeto Compilador - Main
# 	Agostinho Sanches de Araujo - 16507915
# 	Pedro Andrade Caccavaro - 16124679

import argparse
import lexical
import syntactic
# import semantic
# import generator
# import symboltable

def main():
    filePath = argsParser()
    lexical.getFile(filePath)
    # label = 1

    token = lexical.getToken()
    if token["Symbol"] == "sprograma":
        token = lexical.getToken()

        if token["Symbol"] == "sidentificador":
            # insert in symboltable
            token = lexical.getToken()

            if token["Symbol"] == "sponto_virgula":
                syntactic.analyzeBlock()

                if token["Symbol"] == "sponto":
                    token = lexical.getToken()
                    if token == "End":
                        print("SUCESS!")
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()



def argsParser():
    parser = argparse.ArgumentParser(description="Simple compiler")
    parser.add_argument('path', help = "path to the file")
    args = parser.parse_args()

    if args.path == None:
        print ("Usage: compiler.py -f <path_to_file>")
        exit()
    else:
        return args.path


def error():
    print("Found a error Compiler!")
    exit()





if __name__ == '__main__':
    main()
