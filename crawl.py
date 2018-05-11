import os
import time
import requests

def crawl_pfr(teamIds, yearStart, yearStop, targetDir):
    year_range = range(yearStart, yearStop)
    base_url = 'http://www.pro-football-reference.com/'
    roster_path = 'teams/{0}/{1}_roster.htm'
    raw_dir = os.path.abspath(targetDir)
    for team in teamIds:
        team_dir = os.path.join(raw_dir, team)
        if not os.path.exists(team_dir):
            os.makedirs(team_dir)
        for year in year_range:
            time.sleep(1)
            roster_url = base_url + roster_path.format(team, year)
            print(roster_url)
            resp = requests.get(roster_url, verify=False)
            if resp.status_code == 200:
                fname = '{0}_{1}.html'.format(team, year)
                fpath = os.path.join(team_dir, fname)
                with open(fpath, 'w') as f:
                    f.write(resp.content)
            else:
                print('Bad: {0} {1}'.format(team, year))

if __name__ == '__main__':
    crawl_pfr(['nyg','nyj'], 2008, 2009, 'data/raw')