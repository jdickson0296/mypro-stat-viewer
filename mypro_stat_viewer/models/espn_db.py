from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


Model = declarative_base(name="Model")


class Teams(Model):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    year = Column(Integer)
    league_id = Column(Integer)


class BoxScores(Model):
    __tablename__ = "box_scores"
    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    home_team = Column(String)
    away_team = Column(String)
    home_score = Column(Float)
    away_score = Column(Float)
    away_projected = Column(Float)
    home_projected = Column(Float)
    year = Column(Integer)
    league_id = Column(Integer)


class Players(Model):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)
    team = Column(String)
    owner = Column(String)
    points = Column(Float)
    projected_points = Column(Float)
    year = Column(Integer)
    league_id = Column(Integer)


engine = create_engine("sqlite:///espn-fantasy.db", echo=True)
Model.metadata.create_all(engine)
