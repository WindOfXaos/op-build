from urllib import request
from urllib.request import Request
from bs4 import BeautifulSoup

def get_runes(lane, name):
    """
    Gets the runes of specific champion and lane
    """
    rune_options = []
    URL = "https://euw.op.gg/champion/" + name + "/statistics/" + lane
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    paths = soup.find_all('div', class_ = "champion-stats-summary-rune__name")
    rune_paths = ([path.text.split(' + ') for path in paths])
    active_runes = soup.find_all('div', class_ = ["perk-page__item perk-page__item--active",\
                                                  "perk-page__item perk-page__item--keystone perk-page__item--active"])
    # Determine the Primary/Secondary runes
    all_runes = []
    for runes in active_runes:
        all_runes.append((runes.find('img', alt=True)['alt'], runes.find('img', alt=True)['src']))

    # Determine the shards for each build
    all_shards = []
    active_shards = soup.find_all('div', class_ = "fragment__detail")
    for i in range(len(active_shards)):
        shard_option = active_shards[i].find_all('div', class_ = "fragment__row")
        _shard = []
        for j in range(len(shard_option)):
            for k in range(3):
                option = shard_option[j].find_all('img')[k]
                if ('class="active tip"' in str(option)):
                    _shard.append(option['src'])

    # TODO: clean up data processing. op.gg seems always have 4 options but that could change
    # Formats data into a list of all runes
        if i in [0,1]:
            primary_path = [rune_paths[0][0], all_runes[(6*i):(4+(i*6))]]
            secondary_path = [rune_paths[0][1],all_runes[4+(6*i):(6+(i*6))]]
            rune_options.append([primary_path,secondary_path,_shard])
        else:
            primary_path = [rune_paths[1][0],all_runes[(6*i):(4+(i*6))]]
            secondary_path = [rune_paths[1][1],all_runes[4+(6*i):(6+(i*6))]]
            rune_options.append([primary_path,secondary_path,_shard])
    return(rune_options)