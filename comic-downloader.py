import argparse, requests, asyncio, os, glob
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("link", type=str, nargs="?")
parser.add_argument("--limit", "-l", type=int, default=None)
parser.add_argument("--offset", "-O", type=int, default=0)
parser.add_argument("--sort", action="store_const", const=True, default=False)
parser.add_argument("--auto_offset", action="store_const", const=True, default=False)
args = parser.parse_args()

if args.offset < 0:
    print("Offset must be greater than or equal to 0!")
    exit()

limit = args.limit + args.offset if args.limit else None

total_digits = len(str(limit)) if limit else 8



def sort_dir():
    names = [filename for filename in glob.glob("./*.png")]
    longest = 0
    largest = 0
    for filename in names:
        if filename.startswith("./"):
            filename = filename[2:]

            numbers = filename.split()[2].split(".")[0]

            l = len(numbers)
            if l > longest:
                longest = l
            n = int(numbers)
            if n > largest:
                largest = n
            # ['El', 'Goonish', 'Shive', '-', '058.png']

    for filename in names:
        l = filename.split()
        n = l[2].split(".")[0]
        if len(n) < longest:
            n = "0" * (longest - len(n)) + n
            os.rename(filename, f"Rain - {n}.png")
    return largest


async def get_egs_page(link, times=args.offset, names = []):
    try:
        raw = requests.get(link)

        soup = BeautifulSoup(raw.content, 'html.parser')

        img_raw = soup.find(id="cc-comic")
        img_link = img_raw.get('src')

        len_times = len(str(times + 1))
        img_name = "El Goonish Shive - " + "0" * (total_digits - len_times) + str(times + 1)

        box = soup.find(id="leftarea")

        title = None
        count = 0
        for item in box.children:
            if count == 3:
                title = item.string
                break
            count += 1

        names.append(f"{title}: Comic number {times}! Link: {link}")

        next_button = box.find("a", {"class": "cc-next"})
        next_task = None


        finished = False


        if next_button:
            next_link = next_button.get('href')

            if not limit or times < limit - 1:
                next_task = asyncio.create_task(get_egs_page(next_link, times + 1, names))

        with open(img_name + ".gif", "wb") as f:
            f.write(requests.get(img_link).content)
        print(f"Finished comic {title}, which is number {times + 1}! It has the link of: {link}")
        if next_task:
            await next_task

        if finished:
            if times == 0:
                print(f"Finished after writing 1 image to {os.getcwd()}!")
            else:
                print(f"Finished after writing {times + 1 - args.offset} images to {os.getcwd()}!")
            with open("Index.txt", "w") as f:
                f.write('\n'.join(names))
    except:
        print(f"Failed after downloading {times + 1 - args.offset} images! Writing downloaded comics to Index.txt!")
        with open("Index.txt", "w") as f:
            f.write('\n'.join(names))



async def get_rain_page(link, times=args.offset, names = []):
    try:
        raw = requests.get(link)

        soup = BeautifulSoup(raw.content, 'html.parser')

        img_raw = soup.find(id="comicimage")
        img_link = img_raw.get('src')
        title = img_raw.get('alt')

        len_times = len(str(times + 1))
        img_name = "Rain - " + "0" * (total_digits - len_times) + str(times + 1)

        next_link = None

        for item in soup.find_all('a', class_ = "comicnavlink"):
            if item.string.startswith("Next"):
                next_link = "https://rain.thecomicseries.com" + item.get('href')
                break

        names.append(f"Comic number {times}! Link: {link}")

        next_task = None


        finished = False


        if next_link:
            if not limit or times < limit - 1:
                next_task = asyncio.create_task(get_rain_page(next_link, times + 1, names))

        with open(img_name + ".png", "wb") as f:
            f.write(requests.get(img_link).content)
        if title is not None:
            print(f"Finished comic {title}, which is comic number {times + 1}! It has a link of: {link}!")
        else:
            print(f"Finished comic number {times + 1}! It has the link of: {link}")
        if next_task:
            await next_task

        if finished:
            if times == 0:
                print(f"Finished after writing 1 image to {os.getcwd()}!")
            else:
                print(f"Finished after writing {times + 1 - args.offset} images to {os.getcwd()}!")
            with open("Index.txt", "w") as f:
                f.write('\n'.join(names))
    except:
        print(f"Failed after downloading {times + 1 - args.offset} images! Writing downloaded comics to Index.txt!")
        with open("Index.txt", "w") as f:
            f.write('\n'.join(names))

offset = 0

if args.auto_offset:
    offset = sort_dir()
    if limit is not None:
        limit += offset

if args.sort:
    sort_dir()
else:
    if args.link:
        task = None

        if "egscomics" in args.link:
            task = get_egs_page(args.link.split()[0],offset)
        else:
            task = get_rain_page(args.link.split()[0],offset)
        asyncio.run(task)
    else:
        print("Link is required if flag 'sort' is not passed!")

if args.auto_offset:
    sort_dir()
