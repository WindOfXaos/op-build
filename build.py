import requests
from urllib import request, response, error, parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json


def get_build(lane, name):
    build = {'starter_items': '',
            'builds': '',
            'boots': ''}

    URL = "https://euw.op.gg/champion/" + name + "/statistics/" + lane
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table", {"class": "champion-overview__table"})
    tbody = table[1].find("tbody") #champion-overview__row champion-overview__row--first
    tr = tbody.find_all("tr", {"class": "champion-overview__row"})
    lis = []
    types = ['starter_items', 'builds', 'boots']
    counter = 0
    for i in range(0, len(tr)):
        td = tr[i].find("td", {"class": "champion-overview__data"})
        ul = td.find("ul", {"class": "champion-stats__list"})
        li = ul.find_all("li", {"class": "champion-stats__list__item tip"})
        newList = []
        for j in li:
            try:
                mystr = j['title']
                start = mystr.find('>') + 1
                end = mystr.find('<', 1)
                newList.append((mystr[start:end], j.img['src']))
            except KeyError:
                pass
        lis.append(newList)
        try:
            if ('champion-overview__row--first' in tr[i + 1]['class']):
                build.update({types[counter]: lis})
                lis = []
                counter = counter + 1
        except IndexError:
            build.update({types[counter]: lis})
    return build