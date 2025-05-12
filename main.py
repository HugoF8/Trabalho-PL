import sys
import os
from cql_grammar import create_parser, ImportTableNode, PrintTableNode
from cql_eval    import Evaluator, Memory

def print_header():
    print("="*60)
    print(" CQL Interpreter ")
    print("="*60)

def print_help():
    print(":help    mostrar esta ajuda")
    print(":quit    sair")
    print()

def run_file(fname, parser, evaluator):
    with open(fname, encoding='utf-8') as f:
        script = f.read()
    prog = parser.parse(script)
    evaluator.visit(prog)

def run_datafile(fname, parser, evaluator):
    name, _ = os.path.splitext(os.path.basename(fname))
    print(f"Importando '{fname}' → tabela '{name}'")
    evaluator.visit(ImportTableNode(name, fname))
    evaluator.visit(PrintTableNode(name))

def repl(parser, evaluator):
    print_header()
    print("Escreva comandos CQL (‘:help’ para ajuda, ‘:quit’ para sair)\n")
    while True:
        try:
            line = input("cql> ").strip()
        except EOFError:
            break
        if not line:
            continue
        if line.startswith(':'):
            if line in (':quit', ':exit'):
                break
            if line == ':help':
                print_help()
            continue

        stmt = line if line.endswith(';') else line + ';'
        prog = parser.parse(stmt)
        evaluator.visit(prog)

def main():
    parser    = create_parser()
    memory    = Memory()
    evaluator = Evaluator(memory)

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        ext = os.path.splitext(arg)[1].lower()

        if ext == '.csv' and os.path.isfile(arg):
            run_datafile(arg, parser, evaluator)
        else:

            run_file(arg, parser, evaluator)
    else:
        repl(parser, evaluator)

if __name__ == "__main__":
    main()