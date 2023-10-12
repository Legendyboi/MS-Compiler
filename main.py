from lexer import *
from emit import *
from parser import *
import sys
import subprocess


def main():
    print("MS-Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # Initialize the lexer, emitter, and parser.
    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()  # Start the parser.
    emitter.writeFile()  # Write the output to file.
    print("Compiling completed.")

    run_gcc()


def run_gcc():
    # Replace 'out.c' with the path to your C source file
    source_file = 'out.c'

    # Compile the C source file using GCC
    try:
        subprocess.check_output(['gcc', source_file, '-o', 'output_program'])
        print("Compilation successful")
    except subprocess.CalledProcessError as e:
        print("Compilation failed. Error output:")
        print(e.output)


main()
