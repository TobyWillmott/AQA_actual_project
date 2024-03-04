from sqlalchemy import Column, Integer, Table, String, UniqueConstraint, ForeignKey, DateTime, BLOB
from sqlalchemy.orm import relationship, declarative_base, validates
import re

# Base is called an Abstract Base Class - Our SQL Alchemy models will inherit from this classes
Base = declarative_base()


# user_league = Table("user_league",
#                   Base.metadata,
#                    Column("user_league_id", Integer, primary_key=True),
#                    Column("user_id", ForeignKey("user.user_id")),
#                    Column("league_id", ForeignKey("league.league_id")),
#                    UniqueConstraint("user_id", "league_id")
#                   )

class UserLeague(Base):
    __tablename__ = "user_league"
    user_league_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"), nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'league_id', name='user_league_uc'),)


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, unique=False, nullable=False)
    last_name = Column(String, unique=False, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)

    leagues = relationship("League",
                           secondary="user_league",
                           order_by="(League.league_id)",
                           back_populates="users",
                           )
    selections = relationship("Selection", back_populates='user')

    #@validates("firstname")
    #def validate_password(self, key, firstname):
    #    pattern = "/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/"
    #    if not re.fullmatch(pattern, password):
    #        raise ValueError("Invalid password \n Password must be minimum 8 characters, at least one letter and number")
    #    if key != "password":
    #        raise ValueError("Key must be 'password'")
    #    return password


class League(Base):
    __tablename__ = "league"
    league_id = Column(Integer, primary_key=True, autoincrement=True)
    gameweek_id = Column(Integer, ForeignKey("gameweek.gameweek_id"), nullable=False)
    league_name = Column(String, unique=False, nullable=False)
    users = relationship("User",
                         secondary="user_league",
                         order_by="(User.user_id)",
                         back_populates="leagues")
    selections = relationship("Selection", back_populates="league")
    gameweek = relationship("Gameweek", back_populates="leagues")


class Team(Base):
    __tablename__ = "team"
    team_id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String, unique=True, nullable=False)
    team_abb = Column(String, unique=True, nullable=False)
    selections = relationship("Selection", back_populates="team")


class Selection(Base):
    __tablename__ = "selection"
    selection_id = Column(Integer, primary_key=True, autoincrement=True)
    gameweek_id = Column(Integer, ForeignKey("gameweek.gameweek_id"), unique=False, nullable=False)
    outcome = Column(String, unique=False, nullable=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), unique=False, nullable=False)
    team_id = Column(Integer, ForeignKey("team.team_id"), unique=False, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"), unique=False, nullable=False)

    user = relationship("User", back_populates="selections")
    gameweek = relationship("Gameweek", back_populates="selections")
    team = relationship("Team", back_populates="selections")
    league = relationship("League", back_populates="selections")

class Gameweek(Base):
    __tablename__ = "gameweek"
    gameweek_id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(DateTime, unique=False, nullable=False)
    selections = relationship("Selection", back_populates="gameweek")

    leagues = relationship("League", back_populates="gameweek")
