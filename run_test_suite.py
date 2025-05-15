from sys import argv
import contextlib
import io
import glob
from interpreter import ScrollScriptInterpreter
from parser import ScrollScriptParser
from utils import bcolors

GRAMMAR_PATH = "ScrollScript.gmr"

def main():
    if len(argv) < 2:
        print("No directory provided.")
    
    path = argv[1]
    
    print(bcolors.OKBLUE + "\nRunning Test Suite\n" + bcolors.ENDC)
    
    passed = 0
    failed = 0
    
    file_paths = glob.glob(f"{path}/*.scroll")
    max_len = max(len(fpath) for fpath in file_paths)
    
    for fpath in file_paths:
        print(f"{fpath.ljust(max_len)}", end='\t')
        try:
            run_file(fpath)
            print(bcolors.OKGREEN + "Passed" + bcolors.ENDC)
            passed += 1
        except:
            print(bcolors.FAIL + "Failed" + bcolors.ENDC)
            failed += 1
    
    print(bcolors.HEADER + f"\nSummary: {passed} passed, {failed} failed" + bcolors.ENDC)

def run_file(program_path):
    parser = ScrollScriptParser(GRAMMAR_PATH)

    # Redirect stdout and stderr to suppress output
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        parse_tree = parser.parse(program_path)
        interpret = ScrollScriptInterpreter()
        interpret.transform(parse_tree)

if __name__ == '__main__': main()