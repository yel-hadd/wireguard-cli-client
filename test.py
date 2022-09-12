from itertools import cycle
from urllib.request import urlopen
from urllib.error import URLError
import sys


# emolst = ["👻", "👾", "👽"]


def check_internet():
    emolst = ["🌎", "🌍", "🌏"]
    emo = cycle(emolst)
    while True:
        sys.stdout.write(f"\rConnecting {next(emo)}...")
        try:
            response = urlopen('https://duckduckgo.com/', timeout=10)
            print("\n")
            return 0
        except URLError:
            sys.stdout.flush()
            pass


check_internet()
