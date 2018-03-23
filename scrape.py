from bs4 import BeautifulSoup
from collections import Counter
import pprint
from urllib.request import urlopen

epicurious = 'https://www.epicurious.com/recipes/food/views/instant-pot-sticky-hoisin-baby-back-ribs'
pfr = 'https://www.pro-football-reference.com/teams/nyg/2008_roster.htm'

def main():
    html = urlopen(pfr)
    soup = BeautifulSoup(html.read(), 'html.parser')
    cnt = Counter()
    # for child in soup.find_all():
    #     cnt[child.name] += 1
    # pprint.pprint(dict(cnt), indent=4)

    # Need to handle header rows
    for player_row in soup.find('table', {'id':'starters'}).tbody.tr.find_next_siblings():
        player_data = player_row.find_all('td')
        name_cell = player_data[0]
        print(name_cell.attrs['data-append-csv'], name_cell.a.text)

if __name__ == '__main__':
    main()