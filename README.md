# HLInt Interpreter (CSS125L Project)

## Overview

This is a Python-based interpreter for a **Hypothetical Language (HL)** created for the CSS125L course project. The primary goal of the interpreter, named **HLInt**, is to demonstrate fundamental compiler/interpreter design principles, including lexical analysis and syntax validation.

## Features

The HLInt Interpreter performs three main tasks:

1.  **Code Cleaning:** Removes all unnecessary whitespace and generates the `NOSPACES.TXT` file.
2.  **Lexical Analysis:** Identifies all reserved words and special symbols, storing them in the `RES_SYM.TXT` file.
3.  **Syntax Validation:** Checks the HL source code line-by-line for correct grammar (declarations, assignments, conditional statements).

## HL Language Constructs

The interpreter supports the following basic constructs of the HL language:

| Construct | Example Syntax |
| :--- | :--- |
| **Data Types** | `integer`, `double` |
| **Declaration** | `x:integer;` |
| **Assignment** | `x:=5;` |
| **Arithmetic** | Addition (`+`), Subtraction (`-`) |
| **Output** | `output<<x+y;` |
| **Conditional**| `If(x<5) output<<x;` |

## How to Run the Project

### Prerequisites

* Python 3.x

### Execution

1.  Navigate to the project's root directory.
2.  Run the interpreter using the Python executable, passing the HL source file as an argument:

    ```bash
    python HLInt.py <source_file.hl>
    # Example: python HLInt.py PROG1.HL
    ```

3.  The program will output either **"NO ERROR(S) FOUND"** or **"ERROR"** to the console.

## Group Members

* Willard C. Soriano
* Joaquin Xavier S. Lajom
* Champagne Sheng T. Gonzales
