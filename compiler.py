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
    if token != "Error":
        if token["Symbol"] == "sprograma":
            token = lexical.getToken()
            if token["Symbol"] == "sidentificador":
                # insert in symboltable
                token = lexical.getToken()
                if token["Symbol"] == "sponto_virgula":
                    syntactic.analyzeBlock()
                    token = lexical.getToken()
                    if token == "End":
                        print("SUCESS!")
		    #if token["Symbol"] == "sponto":
			# token = lexical.getToken()
			#if token == "End":
			    #   print("SUCESS!")
			#else:
			    #   error()
                    else:
                        error("the end of file", token["Line"])
                else:
                    error("an ;", token["Line"])
            else:
                error("an Identifier", token["Line"])
        else:
            error("programa", token["Line"])
    else:
        print("Found an error: Expected } to finish the comment!")


def argsParser():
    parser = argparse.ArgumentParser(description="Simple compiler")
    parser.add_argument('path', help = "path to the file")
    args = parser.parse_args()

    if args.path == None:
        print ("Usage: compiler.py -f <path_to_file>")
        exit()
    else:
        return args.path


def error(string,line):
    print("Found an error: Expected " + string + " in line " + str(line))
    exit()






if __name__ == '__main__':
    main()
