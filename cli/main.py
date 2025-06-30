#!/usr/bin/env python3
import sys, argparse

from core.parser       import parse
from core.interpreter  import execute
from core.type_checker import type_check, TypeError

def cmd_run(args):
    src = open(args.file).read()
    ast = parse(src)
    try:
        type_check(ast)
    except TypeError as e:
        sys.exit(f"Type error: {e}")
    execute(ast)

def cmd_repl(args):
    print("Eidos REPL. `exit` o `quit` per uscire.")
    repl = execute  # user-runner non utile con funzioni
    # per semplicità, non supportiamo definire funzioni in REPL

def main():
    parser = argparse.ArgumentParser(prog="eidos")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Esegui file .ei")
    p_run.add_argument("file", help="Percorso .ei")
    p_run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
