from sys import argv
import contextlib
import sys
import os
import io
import glob
from interpreter import ScrollScriptInterpreter
from parser import ScrollScriptParser
from utils import bcolors

GRAMMAR_PATH = "ScrollScript.gmr"

def main():
    if len(argv) < 2:
        print("No directory provided.")
        return
    
    path = argv[1]
    test_files = sorted(glob.glob(f"{path}/*.scroll"))
    max_len = max(len(f.split("\\")[-1].split(".")[0]) for f in test_files)

    print(bcolors.OKBLUE + "\n#--- Running Test Suite ---#\n" + bcolors.ENDC)
    
    passed = 0
    failed = 0
    
    for fpath in test_files:
        fname = fpath.split("\\")[-1].split(".")[0]
        print(fname.ljust(max_len), end="\t")
        try:
            if run_file(fpath):
                print(bcolors.OKGREEN + "Passed" + bcolors.ENDC)
                passed += 1
            else:
                print(bcolors.FAIL + "Failed" + bcolors.ENDC)
                failed += 1
        except Exception as e:
            print(bcolors.FAIL + f"Failed (error: {e})" + bcolors.ENDC)
    
    print(f"\n{bcolors.HEADER}Summary:")
    print(f"{bcolors.OKCYAN}Total: {passed+failed}")
    print(f"{bcolors.OKGREEN}Passed: {passed}")
    print(f"{bcolors.FAIL}Failed: {failed}{bcolors.ENDC}")

def run_file(program_path):
    parser = ScrollScriptParser(GRAMMAR_PATH)
    interpreter = ScrollScriptInterpreter()

    # Capture printed output
    captured_output = io.StringIO()
    sys_stdout = sys.stdout
    sys.stderr = io.StringIO()  # optional: capture stderr too
    sys.stdout = captured_output

    expected_output_path = os.path.join(
        os.path.dirname(program_path),
        "output",
        os.path.basename(program_path).replace(".scroll", ".o")
    )

    try:
        parse_tree = parser.parse(program_path)
        interpreter.transform(parse_tree)
        sys.stdout = sys_stdout
        actual_output = captured_output.getvalue().strip()

        with open(expected_output_path) as f:
            expected_output = f.read().strip()

        return actual_output == expected_output

    except Exception as e:
        sys.stdout = sys_stdout
        exception_name = type(e).__name__
        with open(expected_output_path) as f:
            expected_output = f.read().strip()
        return exception_name in expected_output or str(e).strip() == expected_output.strip()

if __name__ == '__main__': main()