# HLInt.py
# Interpreter for a hypothetical language "HL"
# Usage: python HLInt.py <source_file.hl>

import re
import sys

class HLInterpreter:
    """
    A simple interpreter for the hypothetical language HL.

    It performs three main tasks:
    1. Reads an HL source file, removes all spaces, and saves it to NOSPACES.TXT.
    2. Identifies all reserved words and symbols and saves them to RES_SYM.TXT.
    3. Performs a syntax check and prints the result to the console.
    """

    def __init__(self, source_file_path):
        """Initializes the interpreter with the path to the source file."""
        self.source_file_path = source_file_path
        self.source_lines = []
        self.symbol_table = {}  # To store declared variables and their types

        # Define the language's grammar components
        self.reserved_words = {'integer', 'double', 'output', 'If'}
        # List is ordered to match longer tokens first (e.g., '==' before '=')
        self.symbols = ['<<', ':=', '==', '!=', '>', '<', ':', ';', '+', '-', '=', '(', ')', '"']

    def run(self):
        """Executes the main interpretation process."""
        try:
            self._read_and_clean_source()
            self._create_nospaces_file()
            self._create_res_sym_file()
            
            # Perform syntax check and print the final result
            if self._has_valid_syntax():
                print("NO ERROR(S) FOUND")
            else:
                print("ERROR")

        except FileNotFoundError:
            print(f"ERROR: Source file '{self.source_file_path}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _read_and_clean_source(self):
        """Reads the source file and stores non-empty, stripped lines."""
        with open(self.source_file_path, 'r') as f:
            # Store lines that are not empty after stripping whitespace
            self.source_lines = [line for line in (l.strip() for l in f) if line]

    def _create_nospaces_file(self):
        """Creates NOSPACES.TXT by removing all whitespace from the source code."""
        with open("NOSPACES.TXT", 'w') as f:
            for line in self.source_lines:
                # Remove all spaces and tabs
                no_space_line = re.sub(r'\s+', '', line)
                f.write(no_space_line)

    def _create_res_sym_file(self):
        """Creates RES_SYM.TXT with all found reserved words and symbols."""
        found_tokens = set()
        full_text = "\n".join(self.source_lines)

        # Find all reserved words using word boundaries
        for word in self.reserved_words:
            if re.search(r'\b' + re.escape(word) + r'\b', full_text):
                found_tokens.add(word)

        # Create a single regex to find all symbols, prioritizing longer ones
        symbol_pattern = '|'.join(re.escape(s) for s in self.symbols)
        for match in re.finditer(symbol_pattern, full_text):
            found_tokens.add(match.group(0))

        with open("RES_SYM.TXT", 'w') as f:
            # Write the unique tokens in sorted order
            for token in sorted(list(found_tokens)):
                f.write(token + '\n')

    def _check_expression_variables(self, expr_str):
        """Checks if all variables in an expression have been declared."""
        # Find all potential variable names (alphanumeric, starting with a letter)
        variables_in_expr = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', expr_str)
        for var in variables_in_expr:
            # A reserved word is not a variable, so we skip it
            if var in self.reserved_words:
                continue
            if var not in self.symbol_table:
                # This variable was used without being declared first
                return False
        return True
    
    def _is_valid_statement(self, line):
        """Checks if a single line is a valid assignment or output statement."""
        # Simplified check for statements allowed inside an 'If' block
        is_assignment = re.match(r'^\s*([a-zA-Z]\w*)\s*:=\s*(-?\d+(\.\d{1,2})?)\s*;\s*$', line)
        is_output = re.match(r'^\s*output\s*<<\s*(.*)\s*;\s*$', line)
        
        if is_assignment:
            var_name = is_assignment.group(1)
            return var_name in self.symbol_table
        if is_output:
            content = is_output.group(1).strip()
            # If content is not a string literal, check its variables
            if not (content.startswith('"') and content.endswith('"')):
                return self._check_expression_variables(content)
            return True # String literals are always valid
        return False

    def _has_valid_syntax(self):
        """
        Parses the source code line by line to validate its syntax.
        Returns True if syntax is correct, False otherwise.
        """
        line_index = 0
        while line_index < len(self.source_lines):
            line = self.source_lines[line_index]
            line_index += 1

            # Regex patterns for valid HL statements
            patterns = {
                'declaration': r'^\s*([a-zA-Z]\w*)\s*:\s*(integer|double)\s*;\s*$',
                'assignment': r'^\s*([a-zA-Z]\w*)\s*:=\s*(-?\d+(\.\d{1,2})?)\s*;\s*$',
                'output': r'^\s*output\s*<<\s*(.*)\s*;\s*$',
                'if_statement': r'^\s*If\s*\((.*)\)\s*$'
            }

            # 1. Check for Variable Declaration (e.g., x:integer;)
            match = re.match(patterns['declaration'], line)
            if match:
                var_name, var_type = match.groups()
                if var_name in self.symbol_table: return False # Error: Re-declaration
                self.symbol_table[var_name] = var_type
                continue

            # 2. Check for Assignment (e.g., x:=5;)
            match = re.match(patterns['assignment'], line)
            if match:
                var_name, value = match.groups()[:2]
                if var_name not in self.symbol_table: return False # Error: Undeclared variable
                var_type = self.symbol_table[var_name]
                # Check for type mismatch
                is_int = '.' not in value
                if (var_type == 'integer' and not is_int) or \
                   (var_type == 'double' and is_int and not value.isdigit()):
                    return False
                continue
            
            # 3. Check for Output (e.g., output<<x;)
            match = re.match(patterns['output'], line)
            if match:
                content = match.group(1).strip()
                # If content is not a string literal, check its variables
                if not (content.startswith('"') and content.endswith('"')):
                    if not self._check_expression_variables(content): return False
                continue

            # 4. Check for If Statement (e.g., If(x<5))
            match = re.match(patterns['if_statement'], line)
            if match:
                condition = match.group(1)
                if not self._check_expression_variables(condition): return False
                
                # The 'If' statement requires an indented body on the next line
                if line_index >= len(self.source_lines): return False # Error: 'If' with no body
                
                next_line_full = open(self.source_file_path).readlines()[line_index] # Re-read to check indentation
                next_line_stripped = self.source_lines[line_index]

                # Check for indentation (must start with a space or tab)
                if not (next_line_full.startswith(' ') or next_line_full.startswith('\t')): return False
                
                # Check if the indented body is a valid statement
                if not self._is_valid_statement(next_line_stripped): return False
                
                line_index += 1 # Skip the body line in the next iteration
                continue

            # If a line matches no valid patterns, it's a syntax error
            return False

        return True # All lines were successfully parsed

if __name__ == "__main__":
    # Ensure a filename is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python HLInt.py <source_file.hl>")
        sys.exit(1)

    source_file = sys.argv[1]
    interpreter = HLInterpreter(source_file)
    interpreter.run()