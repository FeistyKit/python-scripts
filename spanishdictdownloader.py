import argparse, requests, asyncio
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)
parser.add_argument("--outfile", type=str, default="output.txt")
args = parser.parse_args()

async def download(word: str):
    page = requests.get(f"https://www.spanishdict.com/translate/{word.lower()}")

    soup = BeautifulSoup(page.content, "html.parser")
    
    es = str(soup.find(id="headword-es").h1.string)

    if ">feminine noun</a>" in page.text:
        es = "la " + es
    elif ">masculine noun</a>" in page.text:
        es = "el " + es

    en = str(soup.find(id="quickdef1-es").a.string)
    return es, en

async def run():
    to_translate = []
    with open(args.infile, "r") as f:
        for line in f.readlines():
            to_translate.append(line.strip())
    objects = [download(item) for item in to_translate] 

    results = await asyncio.gather(*objects)

    terms = []

    for d in results:
        str = f"{d[0]} = {d[1]}"
        terms.append(str)

    with open(args.outfile, "w") as f:
        f.write("\n".join(terms))
    print(f"Done! Wrote {len(terms)} words to {args.outfile}!")

asyncio.run(run())
