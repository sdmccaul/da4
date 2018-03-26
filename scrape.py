from bs4 import BeautifulSoup, Comment
import re
from urllib.request import urlopen

pfr = 'https://www.pro-football-reference.com/teams/nyg/2008_roster.htm'

def parse_draft_data(draftSoup):
    draft_info = draftSoup.text.split('/')
    if draft_info == ['']:
        return ['UDFA', '', '', '']
    return [ d.strip() for d in draft_info ]

def get_player_data(playerSoup):
    # First cell in table, Uniform Number, is actually
    # a th element, so it's skipped.
    # Otherwise table structure is as follows:
    # Player|Age|Pos|G|GS|Wt|Ht|College/Univ|BirthDate|Yrs|AV|Drafted(tm/rnd/yr)
    # We'll be interested in the following:
    pd = {
        'pfr_id' : '', #Disambiguation
        'name' : '',
        'games_played' : '',
        'games_started' : '',
        'age' : '',
        'school' : '', #Disambiguation
        'birthdate' : '', #Disambiguation
        'years_played' : '',
        'position' : '',
        'year_drafted' : '',
        'drafted_by' : '',
        'draft_position' : '',
        'draft_round' : ''
    }
    player_data = playerSoup.find_all('td')
    pd['name'] = player_data[0].attrs['csk']
    pd['pfr_id'] = player_data[0].attrs['data-append-csv']
    pd['age'] = player_data[1].text
    pd['position'] = player_data[2].text
    pd['games_played'] = player_data[3].text
    pd['games_started'] = player_data[4].text
    pd['school'] = player_data[7].text
    pd['birthdate'] = player_data[8].attrs['csk']
    pd['years_played'] = player_data[9].text
    team, rnd, pos, year = parse_draft_data(player_data[11])
    pd['drafted_by'] = team
    pd['draft_round'] = rnd
    pd['draft_position'] = pos
    pd['year_drafted'] = year
    return pd

def main():
    # html = urlopen(pfr)
    # page_soup = BeautifulSoup(html.read(), 'html.parser')

    with open('data/pfr-sample.html','r') as f:
        page_soup = BeautifulSoup(f.read(), 'html.parser')

    # https://stackoverflow.com/questions/33138937/how-to-find-all-comments-with-beautiful-soup
    comments=page_soup.find_all(string=lambda text:isinstance(text,Comment))
    roster_comment = [ c for c in comments if 'id="games_played_team"' in c ]
    roster_soup = BeautifulSoup(roster_comment[0], "html.parser")
    table_rows = roster_soup.find(
        'table', {'id':'games_played_team'}).tbody.find_all('tr') 
    player_rows = [ row for row in table_rows
        if row.find('a',{'href': re.compile('players')}) ]
    for row in player_rows:
        print(get_player_data(row))

if __name__ == '__main__':
    main()