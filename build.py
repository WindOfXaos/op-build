import requests
from urllib import request, response, error, parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def get_build(lane, name):
    """
    Gets build for a champion in a specific lane
    """
    build = [
        ('starter_items_1', []),
        ('starter_items_2', []),
        ('build_1', []),
        ('build_2', []),
        ('build_3', []),
        ('build_4', []),
        ('build_5', []),
        ('boot_1', []),
        ('boot_2', []),
        ('boot_3', [])
    ]
    URL = "https://euw.op.gg/champion/" + name + "/statistics/" + lane
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table", {"class": "champion-overview__table"})
    tbody = table[1].find("tbody")
    tr = tbody.find_all("tr", {"class": "champion-overview__row"})
    if len(tr) < 10:
        build = build[ : 10 - len(tr) + 1] + build[len(tr) : 10]
    for i in range(0, len(tr)):
        td = tr[i].find("td", {"class": "champion-overview__data"})
        ul = td.find("ul", {"class": "champion-stats__list"})
        li = ul.find_all("li")
        for j in li:
            try:
                mystr = j['title']
                start = mystr.find('>') + 1
                end = mystr.find('<', 1)
                build[i][1].append(mystr[start:end])
            except KeyError:
                pass
    return build