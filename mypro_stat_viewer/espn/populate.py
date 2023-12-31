""" Populate the database with data from ESPN. """
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from mypro_stat_viewer.espn.football import ESPNFootball
from mypro_stat_viewer.models.espn_db import Teams, BoxScores, Players


# Setup DB Session
DATABASE_URL = "sqlite:///espn-fantasy.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB = SessionLocal()

# Get Environment Variables
ESPN_S2 = os.environ.get("ESPN_S2")
SWID = os.environ.get("SWID")
LEAGUE_ID = os.environ.get("LEAGUE_ID")
YEAR = 2023

# Create ESPN Client
ESPN_CLIENT = ESPNFootball(
    league_id=LEAGUE_ID,
    year=2023,
    private=True,
    espn_s2=ESPN_S2,
    swid=SWID,
)


def populate_teams(db_session):
    """_summary_

    Args:
        db_session (_type_): _description_
    """
    teams = ESPN_CLIENT.get_teams()
    for team in teams:
        new_team = Teams(
            id=team.team_id,
            name=team.team_name,
            wins=team.wins,
            losses=team.losses,
            year=YEAR,
            league_id=LEAGUE_ID,
        )
        db_session.add(new_team)
    db_session.commit()


def populate_box_scores(db_session):
    """_summary_

    Args:
        db_session (_type_): _description_
    """
    weeks = ESPN_CLIENT.get_reg_season_count()
    for week in range(1, weeks + 1):
        box_scores = ESPN_CLIENT.get_league().box_scores(week)
        for box_score in box_scores:
            new_box_score = BoxScores(
                week=week,
                home_team=box_score.home_team.team_name,
                away_team=box_score.away_team.team_name,
                home_score=box_score.home_score,
                away_score=box_score.away_score,
                home_projected=box_score.home_projected,
                away_projected=box_score.away_projected,
                year=YEAR,
                league_id=LEAGUE_ID,
            )
            db_session.add(new_box_score)
    db_session.commit()


def populate_players(db_session):
    """_summary_

    Args:
        db_session (_type_): _description_
    """
    teams = ESPN_CLIENT.get_teams()
    for team in teams:
        roster = team.roster
        for player in roster:
            new_player = Players(
                name=player.name,
                position=player.position,
                team=player.proTeam,
                owner=team.team_name,
                points=player.total_points,
                projected_points=player.projected_total_points,
                year=YEAR,
                league_id=LEAGUE_ID,
            )
            db_session.add(new_player)
    db_session.commit()


if __name__ == "__main__":
    populate_teams(DB)
    populate_box_scores(DB)
    populate_players(DB)
    DB.close()
