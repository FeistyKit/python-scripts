import argparse, requests, asyncio
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)
parser.add_argument("--outfile", type=str, default="output.txt")
args = parser.parse_args()

async def download_en(link: str) -> str:
    l = f"https://www.spanishdict.com{link}"
    page = requests.get(l)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup.find(id="quickdef1-en").a.string

async def download_es(word: str):
    l = f"https://www.spanishdict.com/translate/{word.lower()}"
    page = requests.get(l)

    soup = BeautifulSoup(page.content, "html.parser")

    en_raw = soup.find(id="quickdef1-es").a
    
    en_text = en_raw.string

    es = await download_en(en_raw['href'])

    return es, en_text

async def run():
    to_translate = []
    with open(args.infile, "r") as f:
        for line in f.readlines():
            to_translate.append(line.strip())
    objects = [download_es(item) for item in to_translate] 

    results = await asyncio.gather(*objects)

    terms = []

    for d in results:
        str = f"{d[0]} = {d[1]}"
        terms.append(str)

    with open(args.outfile, "w") as f:
        f.write("\n".join(terms))
    print(f"Done! Wrote {len(terms)} words to {args.outfile}!")

asyncio.run(run())
