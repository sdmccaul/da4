from bs4 import BeautifulSoup, Comment
import re
import requests
import sqlite3
import csv
import os

pfr = 'https://www.pro-football-reference.com/teams/nyg/2008_roster.htm'

def scrape_team_info(teamPage, target):
    # teams.html is a copy-n-paste of data from 
    # https://www.pro-football-reference.com/teams/
    # and the javascript drop-down on all pages (for divisions)
    with open( os.path.abspath(teamPage) ) as f:
        soup = BeautifulSoup(f, 'html.parser')

    team_data = {}

    division_list = soup.find('li')
    divs = division_list.find_all('div')
    for div in divs:
        conf, dvn = div.text.split(':')[0].strip().split()
        for link in div.find_all('a'):
            team_name_inc = link.text
            _,_,team_id,_ = link.attrs['href'].split('/')
            team_data[team_id] = {
                'prf_id' : team_id,
                'conference' : conf,
                'division' : dvn,
                'short_name' : team_name_inc
            }

    team_table = soup.find('table')
    team_headers = team_table.find_all('th')
    for th in team_headers:
        if th.find('a'):
            link = th.find('a')
            full_name = link.text
            _,_,team_id,_ = link.attrs['href'].split('/')
            team_data[team_id]['full_name'] = full_name

    # with open(target, 'w') as f:
    #     header = [ 'prf_id', 'full_name', 'short_name'
    #         'conference', 'division' ]
    #     writer = csv.DictWriter(f, header)
    #     for team in team_data:
    #         writer.writerow(team_data[team])

    team_rows =  [ (t['prf_id'], t['full_name'], t['short_name'],
        t['conference'], t['division']) for t in team_data.values() ]

    return team_rows

def parse_draft_data(draftSoup):
    draft_info = draftSoup.text.split('/')
    if draft_info == ['']:
        return ['UDFA', '', '', '']
    return [ d.strip() for d in draft_info ]

def get_player_data(playerSoup):
    # First cell in table, Uniform Number, is actually
    # a <th> element, so it's skipped.
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


def normalize_player_data(playerRow):
    player_data = (playerRow['pfr_id'], playerRow['name'],
        playerRow['birthdate'], playerRow['school'])
    roster_data = (playerRow['pfr_id'], playerRow['age'],
        playerRow['position'], playerRow['games_played'],
        playerRow['games_started'])
    draft_data = (playerRow['pfr_id'], playerRow['year_drafted'],
        playerRow['draft_round'], playerRow['draft_position'])
    return (player_data, roster_data, draft_data)


def scrape(pageFile):
    # html = urlopen(pfr)
    # page_soup = BeautifulSoup(html.read(), 'html.parser')

    with open(pageFile,'r') as f:
        page_soup = BeautifulSoup(f.read(), 'html.parser')

    # https://stackoverflow.com/questions/33138937/how-to-find-all-comments-with-beautiful-soup
    comments=page_soup.find_all(string=lambda text:isinstance(text,Comment))
    roster_comment = [ c for c in comments if 'id="games_played_team"' in c ]
    roster_soup = BeautifulSoup(roster_comment[0], "html.parser")
    table_rows = roster_soup.find(
        'table', {'id':'games_played_team'}).tbody.find_all('tr') 
    player_rows = [ row for row in table_rows
        if row.find('a',{'href': re.compile('players')}) ]
    player_data = [ get_player_data(row) for row in player_rows ]
    normalized = [ normalize_player_data(player)
        for player in player_data ]
    players = [ n[0] for n in normalized ]
    rosters = [ n[1] for n in normalized ]
    drafts = [ n[2] for n in normalized ]
    with open(playerCsv, 'a') as f:
        wrtr = csv.writer(f)
        for p in players:
            wrtr.writerow(p)

    with open(draftCsv, 'a') as f:
        wrtr = csv.writer(f)
        for d in drafts:
            wrtr.writerow(d) 

    with open(rosterCsv, 'w') as f:
        wrtr = csv.writer(f)
        for r in rosters:
            wrtr.writerow(r)

def get_team_and_year(fName):
    #https://www.pro-football-reference.com/teams/nyg/2016.htm
    return team_abbv, year

if __name__ == '__main__':
    crawl_dir = sys.argv[1]
    pages = [ f for f in os.listdir(crawl_dir)
        if isfile(os.path.join(crawl_dir, f)) ]
    for page in pages:
        tally = scrape(page)
    dbops.initialize_db('data/pfr_data.db')
    team_data = scrape_team_info()
    load_team_data(team_data)
    player_data = main()
    load_player_data(player_data, 'nyg')