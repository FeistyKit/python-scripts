#!/usr/bin/env python
import argparse, sys
import re

parser = argparse.ArgumentParser()
parser.add_argument("--delimiter", "-d", default=';')
parser.add_argument("--toreplace", '-c', default='_')
parser.add_argument("file", nargs=1, type=str)
args = parser.parse_args()

def ask_question(in_str, failed):
    items = in_str.split(args.delimiter)
    items = list(map(lambda x: x.strip(), items))
    assert len(items) > 1, f"Item `{in_str}` does not have a delimiter!"
    times = len(re.findall(args.toreplace + "+", items[0]))
    assert times == len(items) - 1, f"Item `{in_str}` has too many splits!"
    answers= [answer.strip() for answer in input(items[0] + ": ").split(",")]
    if answers != items[1:]:
        if len(items[1:]) > 1:
            failed.append(f"For the question `{items[0]}`, `{', '.join(answers)}` was wrong! The correct answers were `{', '.join(items[1:])}`")
        else:
            failed.append(f"For the question `{items[0]}`, `{', '.join(answers)}` was wrong! The correct answer was `{items[1]}`")
    print("\033[F\033[F\n\033[F")


try:
    with open(args.file[0]) as f:
        content = f.read()
        questions = list(content.splitlines())
        failed: list[str] = []
        for q in questions:
            ask_question(q, failed)
        if failed:
            print('\n'.join(failed))
            print(f"You got `{len(failed)}` wrong!", file=sys.stderr)
        else:
            print("You got them all right!")
except IOError:
    print(f"Could not open file `{args.file[0]}`!", file=sys.stderr)
    sys.exit(1)
