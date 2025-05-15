from lark import Lark
from utils import load_file

class ScrollScriptParser(Lark):
    def __init__(self, grammar_path):
        try:
            grammar = load_file(grammar_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load grammar from {grammar_path}") from e
        
        super().__init__(grammar, parser="lalr")
    
    def parse(self, program_path):
        try:
            program = load_file(program_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load program from {program_path}") from e
        
        return super().parse(program)

