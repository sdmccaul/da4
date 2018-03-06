from bs4 import BeautifulSoup
from collections import Counter
import pprint
from urllib.request import urlopen

epicurious = 'https://www.epicurious.com/recipes/food/views/instant-pot-sticky-hoisin-baby-back-ribs'

def main():
    html = urlopen(epicurious)
    soup = BeautifulSoup(html.read(), 'html.parser')
    cnt = Counter()
    for child in soup.find_all():
        cnt[child.name] += 1
    pprint.pprint(dict(cnt), indent=4) 

if __name__ == '__main__':
    main()