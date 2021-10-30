#!/usr/bin/env python
import argparse, sys, platform, re, os, random

parser = argparse.ArgumentParser()
parser.add_argument("--delimiter", "-d", default=';')
parser.add_argument("--toreplace", '-r', default='_')
parser.add_argument("--casesensitive", "-c", action="store_const", const=True, default=False)
parser.add_argument("--shuffle", "-s", action="store_const", const=True, default=False)
parser.add_argument("--output", "-o", action="store_const", const=True, default=False)
parser.add_argument("--outfile", nargs=1, type=str)
parser.add_argument("file", nargs=1, type=str)
args = parser.parse_args()

if args.outfile is None:
    args.outfile = "WRONG_" + args.file[0]
else:
    args.outfile = args.outfile[0]

def ask_question(in_str, failed, num, to_save=None):
    copied_str = in_str
    in_str = in_str.strip(" ;")
    items = in_str.split(args.delimiter)
    items = list(map(lambda x: x.strip(), items))
    if len(items) <= 1:
        print(f"ERROR: {args.file[0]}:{num + 1} Item `{in_str}` does not have a delimiter!", file=sys.stderr)
        return

    times = len(re.findall(args.toreplace + "+", items[0]))
    if times != len(items) - 1:
        print( f"ERROR: {args.file[0]}:{num + 1} Item `{in_str}` has too many splits: it has `{times}` splits and only `{len(items) - 1}` items!", file=sys.stderr)
        return

    answers= [answer.strip() for answer in input(items[0] + ": ").split(",")]

    if list(map(lambda x: x.lower(), answers)) != list(map(lambda x: x.lower(), items[1:])):
        if to_save is not None:
            to_save.append(copied_str)

        if len(items[1:]) > 1:
            failed.append(f"For the question `{items[0]}`, `{', '.join(answers)}` was wrong! The correct answers were `{', '.join(items[1:])}`.")
        else:
            failed.append(f"For the question `{items[0]}`, `{', '.join(answers)}` was wrong! The correct answer was `{items[1]}`.")

    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")


def run():
    content = None
    try:
        with open(args.file[0]) as f:
            content = f.read()
    except Exception:
        print(f"Could not open file `{args.file[0]}`!", file=sys.stderr)
        sys.exit(1)

    questions = list(content.splitlines())
    if args.shuffle:
        random.shuffle(questions)

    failed: list[str] = []
    to_save = []

    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")

    for i, q in enumerate(questions):
        ask_question(q, failed, i)
    if failed:
        print('\n'.join(failed))
        print(f"You got `{len(failed)}` wrong!", file=sys.stderr)
    else:
        print("You got them all right!")

    try:
        if args.output:
            with open(args.outfile, 'w') as f:
                f.write("\n".join(to_save))
    except Exception:
        print(f"Could not open file `{args.outfile}`!", file=sys.stderr)
        sys.exit(1)

run()
