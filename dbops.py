import os
import sqlite3


def initialize_db(dbFile):
    if os.path.isfile(dbFile):
        return
    create_teams_table = """
        CREATE TABLE IF NOT EXISTS teams (
        id integer PRIMARY KEY,
        pfr_id text NOT NULL,
        full_name text NOT NULL,
        short_name text NOT NULL,
        conference text NOT NULL,
        division text NOT NULL
    ); """
    create_player_table = """
        CREATE TABLE IF NOT EXISTS players (
        id integer PRIMARY KEY,
        pfr_id text NOT NULL,
        name text NOT NULL,
        birthdate text,
        school text
    ); """
    create_roster_table = """
        CREATE TABLE IF NOT EXISTS rosters (
        id integer PRIMARY KEY,
        team_id integer NOT NULL,
        year text NOT NULL,
        player_id integer NOT NULL,
        player_age integer,
        player_position text,
        games_played integer,
        games_started integer,
        FOREIGN KEY(player_id) REFERENCES players(id),
        FOREIGN KEY(team_id) REFERENCES teams(id)
    ); """
    create_draft_table = """
        CREATE TABLE IF NOT EXISTS drafts (
        id integer PRIMARY KEY,
        player_id integer NOT NULL,
        team_id integer NOT NULL,
        year text NOT NULL,
        round integer,
        position integer,
        FOREIGN KEY(player_id) REFERENCES players(id),
        FOREIGN KEY(team_id) REFERENCES teams(id)
    ); """
    con = sqlite3.connect(dbFile)
    con.isolation_level = None
    cur = con.cursor()
    cur.execute(create_player_table)
    cur.execute(create_teams_table)
    cur.execute(create_roster_table)
    cur.execute(create_draft_table)
    con.close()
    return True

def load_player_data(playerData, teamId):
    con = sqlite3.connect("data/pfr_data.db")
    con.isolation_level = None
    cur = con.cursor()
    insert_player_row = """ INSERT INTO players (
        pfr_id,name,birthdate,school
        ) VALUES (
        '{0}','{1}','{2}','{3}');
    """
    for data in playerData:
        print(data)
        insert_sql = insert_player_row.format(
            data['pfr_id'],data['name'],data['birthdate'],
            data['school'])
        print(insert_sql)
        cur.execute(insert_sql)
    con.close()

def load_team_data(teamData):
    con = sqlite3.connect("data/pfr_data.db")
    con.isolation_level = None
    cur = con.cursor()
    insert_teams_row = """ INSERT INTO teams (
        pfr_id,full_name,short_name,conference,division
        ) VALUES (
        '{0}','{1}','{2}','{3}','{4}');
    """
    for team, data in team_data.items():
        insert_sql = insert_teams_row.format(
            data['team_id'],data['full_name'],data['short_name'],
            data['conference'],data['division'])
        print(insert_sql)
        cur.execute(insert_sql)
    con.close()

def load_roster_data(rosterData):
    pass

def load_draft_data(playerData):
    pass


def load_data()