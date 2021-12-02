#!/usr/bin/env python

import clipboard, requests, asyncio, argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("link", type=str)
parser.add_argument("--limit", type=int, default=None)
args = parser.parse_args()

def get_script(link: str, limit, words=[]):
    raw = requests.get(link).text

    raw_link = link.split("&p=")[0]

    page = None

    if "&p=" not in link:
        page = 1
    else:
        page = int(link.split("&p=")[1])

    soup = BeautifulSoup(raw, 'html.parser')

    item = soup.find_all(id='disp-quote-body')[0]


    for word in item.children:
        print(limit)
        if limit is None:
            words.append(word.text)
        elif limit > 0:
            words.append(word.text)
            limit -= 1
        else:
            break

    if "\">Next" not in raw or (limit is not None and limit <= 0):
        return words
    else:
        return get_script(raw_link + "&p=" + str(page + 1), limit - 1 if limit is not None else None)


stuff = get_script(args.link, args.limit)
clipboard.copy('\n\n'.join(stuff))
print("Finished with", str(len(stuff)), "paragraphs!")
