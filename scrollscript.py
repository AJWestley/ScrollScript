from sys import argv
from interpreter import ScrollScriptInterpreter
from parser import ScrollScriptParser

GRAMMAR_PATH = "ScrollScript.gmr"

def main():
    
    if len(argv) < 2:
        print("The ancient scrolls were not provided.")
    
    program_path = argv[1]
    
    parser = ScrollScriptParser(GRAMMAR_PATH)
    
    parse_tree = parser.parse(program_path)
    
    interpret = ScrollScriptInterpreter()

    interpret.start(parse_tree)


if __name__ == '__main__': main()