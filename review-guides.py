#!/usr/bin/env python
import argparse, sys, platform, re, os

parser = argparse.ArgumentParser()
parser.add_argument("--delimiter", "-d", default=';')
parser.add_argument("--toreplace", '-c', default='_')
parser.add_argument("file", nargs=1, type=str)
args = parser.parse_args()

def ask_question(in_str, failed, num):
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
    if answers != items[1:]:
        if len(items[1:]) > 1:
            failed.append(f"For the question `{items[0]}`, `{', '.join(answers)}` was wrong! The correct answers were `{', '.join(items[1:])}`.")
        else:
            failed.append(f"For the question `{items[0]}`, `{', '.join(answers)}` was wrong! The correct answer was `{items[1]}`.")

    if platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")


try:
    with open(args.file[0]) as f:
        content = f.read()
        questions = list(content.splitlines())
        failed: list[str] = []
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
except IOError:
    print(f"Could not open file `{args.file[0]}`!", file=sys.stderr)
    sys.exit(1)
