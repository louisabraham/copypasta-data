#!/usr/bin/env python3

"""
Scrapes the copypastas of the n first pages starting from
the url and print the ones with only ASCII characters

n is the first command line argument
if n is -1, continues until there is a 'next' link

url is the second argument and defaults to
https://old.reddit.com/r/copypasta/top/?sort=top&t=all
"""

import multiprocessing as mp
import re
import urllib.request
import urllib.parse
import sys

from itertools import count
from bs4 import BeautifulSoup
from tqdm import tqdm
import gzip


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
}


def urlopen(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
    except Exception as e:
        print(e, file=sys.stderr)
        raise e
    if response.info().get("Content-Encoding") == "gzip":
        pagedata = gzip.decompress(response.read())
    elif response.info().get("Content-Encoding") == "deflate":
        pagedata = response.read()
    elif response.info().get("Content-Encoding"):
        print("Encoding type unknown", file=sys.stderr)
        raise Exception
    else:
        pagedata = response.read()
    return BeautifulSoup(pagedata, "lxml")


def extract_copypasta(url):
    soup = urlopen(url)
    elements = soup.select("#siteTable")[0]
    md = elements.find(class_="md")
    if md is None:
        return ""
    ans = md.text
    assert ans.endswith("\n")
    return ans


def handle_page(pool, soup):
    elements = soup.select("#siteTable")[0]
    urls = [
        "https://old.reddit.com" + urllib.parse.quote(i.get("data-url"))
        for i in elements.find_all("div", {"data-domain": "self.copypasta"})
    ]
    return pool.map(extract_copypasta, urls)


if __name__ == "__main__":

    l = []

    pool = mp.Pool(processes=25)

    nb_pages = int(sys.argv[1])
    url = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "https://old.reddit.com/r/copypasta/top/?sort=top&t=all"
    )

    for _ in tqdm(range(nb_pages) if nb_pages != -1 else count()):

        soup = urlopen(url)
        for p in handle_page(pool, soup):
            if p and all(ord(c) < 128 for c in p):
                print(p)

        findurl = soup.find("a", {"rel": "nofollow next"})
        if findurl is None:
            tqdm.write("last url", url, file=sys.stderr)
            break
        else:
            url = findurl.get("href")
