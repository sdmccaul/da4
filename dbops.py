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