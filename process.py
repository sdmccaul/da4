import crawl
import scrape
import dbops

def process():
    team_rows = scrape.scrape_team_info(
        'data/raw/teams.html', 'scraped/team_data.csv')
    assert(len(team_rows) == 32)
    crawl.crawl_pfr(
        [ t[0] for t in team_rows ], 2008, 2009, 'data/raw')    

if __name__ == '__main__':
    process()