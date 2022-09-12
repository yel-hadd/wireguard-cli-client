from itertools import cycle
from urllib.request import urlopen
from urllib.error import URLError
import sys
from time import sleep


# emolst = ["👻", "👾", "👽"]


def check_internet():
    emolst = ["🌎", "🌍", "🌏"]
    emo = cycle(emolst)
    while True:
        sys.stdout.write(f"\rConnecting {next(emo)}...")
        try:
            response = urlopen('https://duckduckgo.com/', timeout=0.1)
            print("connected")
            return 0
        except URLError:
            sys.stdout.flush()
            pass


check_internet()
