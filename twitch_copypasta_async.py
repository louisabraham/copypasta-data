#!/usr/bin/env python3

"""
Scrapes all the copypastas of https://twitch.gimu.org/
and print the ones with only ASCII characters
"""


from itertools import chain
import multiprocessing as mp
import re
from urllib.request import urlopen
import sys

from bs4 import BeautifulSoup

url = "https://twitch.gimu.org/"
reurl = re.compile(url[:-1] + "\?page=(\d+)")

html = urlopen(url)
soup = BeautifulSoup(html, "lxml")
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
    soup = BeautifulSoup(html, "lxml")
    return [str(pasta.p.text) for pasta in soup.find_all(class_="pasta-entry")]


pool = mp.Pool(processes=50)
l = list(chain(*pool.map(extract_copypastas, urls)))

nb_pasta = 0

for p in l:
    if all(ord(c) < 128 for c in p):
        print(p)
        nb_pasta += 1


print(nb_pasta, file=sys.stderr)
