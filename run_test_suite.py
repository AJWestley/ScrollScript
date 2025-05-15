from sys import argv
import sys
import os
import io
import glob
from interpreter import ScrollScriptInterpreter
from parser import ScrollScriptParser

GRAMMAR_PATH = "ScrollScript.gmr"

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def main():
    if len(argv) < 2:
        print("No directory provided.")
        return
    
    path = argv[1]
    test_files = sorted(glob.glob(f"{path}/*.scroll"))
    max_len = max(len(f.split("\\")[-1].split(".")[0]) for f in test_files)

    print(OKBLUE + "\n#--- Running Test Suite ---#\n" + ENDC)
    
    passed = 0
    failed = 0
    
    for fpath in test_files:
        fname = fpath.split("\\")[-1].split(".")[0]
        print(fname.ljust(max_len), end="\t")
        try:
            if run_file(fpath):
                print(OKGREEN + "Passed" + ENDC)
                passed += 1
            else:
                print(FAIL + "Failed" + ENDC)
                failed += 1
        except Exception as e:
            print(FAIL + f"Failed (error: {e})" + ENDC)
    
    print(f"\n{HEADER}Summary:")
    print(f"{OKCYAN}Total: {passed+failed}")
    print(f"{OKGREEN}Passed: {passed}")
    print(f"{FAIL}Failed: {failed}{ENDC}")

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