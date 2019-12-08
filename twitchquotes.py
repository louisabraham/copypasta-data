#!/usr/bin/env python3

"""
Scrapes all the copypastas of https://www.twitchquotes.com/copypastas
and print the ones with only ASCII characters
"""


from itertools import chain
import multiprocessing as mp
import re
from urllib.request import urlopen
import sys

from bs4 import BeautifulSoup

url = "https://www.twitchquotes.com/copypastas"
reurl = re.compile("/copypastas\?page=(\d+)")

html = urlopen(url)
soup = BeautifulSoup(html, "html5lib")
n_pages = max(
    int(reurl.match(a.get("href")).group(1))
    for a in soup.find_all("a", {"href": reurl})
)

urls = list(url + "?page=%s" % i for i in range(1, n_pages + 1))


def extract_copypastas(url):
    try:
        html = urlopen(url)
    except Exception as e:
        print(e)
        return []
    soup = BeautifulSoup(html, "html5lib")
    return [
        str(pasta.text)
        for pasta in soup.find_all(
            "span", {"id": re.compile("quote_display_content_\d+")}
        )
    ]


pool = mp.Pool(processes=10)
l = list(chain(*pool.map(extract_copypastas, urls)))

nb_pasta = 0

for p in l:
    if all(ord(c) < 128 for c in p):
        print(p)
        nb_pasta += 1


print(nb_pasta, file=sys.stderr)
