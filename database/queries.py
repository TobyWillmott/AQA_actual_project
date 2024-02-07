from sqlalchemy import create_engine
from database.models import Base, User, Gameweek, League, UserLeague, Selection, Team
from sqlalchemy.orm import Session
import hashlib

engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=True)
Base.metadata.create_all(engine)


def qry_add_user(first_name_, last_name_, username_, password_):
    print("this is firts naem", first_name_)
    if first_name_ == "":
        first_name_ = None
    if last_name_ == "":
        last_name_ = None
    if username_ == "":
        username_ = None
    if password_ == "":
        password_ = None
    else:
        hasher = hashlib.sha256()
        hasher.update(bytes(password_, 'utf-8'))
        hasher = hasher.hexdigest()
        password_ = hasher
    with Session(engine) as sess:
        user = User(first_name=first_name_, last_name=last_name_, username=username_, password=password_)
        sess.add(user)
        sess.commit()



def qry_add_league(gameweek_id_, league_name_):
    with Session(engine) as sess:
        league = League(gameweek_id=gameweek_id_, league_name=league_name_)
        sess.add(league)
        sess.commit()


def qry_get_username_details(username_entry):
    with Session(engine) as sess:
        output_lis = sess.query(User.user_id, User.username, User.password).filter_by(
            username=username_entry).first()
    return output_lis


def qry_get_gameweek_timings():
    with Session(engine) as sess:
        output_lis = sess.query(Gameweek.start_date).all()
    return output_lis


def qry_get_gameweek_id():
    with Session(engine) as sess:
        output_id = sess.query(Gameweek.gameweek_id, Gameweek.start_date).all()
    return output_id


def qry_add_user_league(user_id_, league_id_):
    with Session(engine) as sess:
        user_league_value = UserLeague(user_id=user_id_, league_id=league_id_)
        sess.add(user_league_value)
        sess.commit()


def qry_add_selection_list(user_selections):
    with Session(engine) as sess:
        sess.add_all(user_selections)
        sess.commit()


#def qry_add_selection(gameweek_id_, user_id_, team_id_, league_id_):
#    with Session(engine) as sess:
#        user_selection = Selection(gameweek_id=gameweek_id_, outcome=None, user_id=user_id_, team_id=team_id_,
#                                   league_id=league_id_)
#        sess.add(user_selection)
#        sess.commit()


def qry_get_teams():
    with Session(engine) as sess:
        teams = sess.query(Team.team_id, Team.team_name).all()
    lis = []
    for i in teams:
        lis.append(i)
    return lis


def qry_get_league_starting_gameweek(league_id_):
    with Session(engine) as sess:
        gameweek = sess.query(League.gameweek_id).filter_by(league_id=league_id_).first()
    return gameweek[0]


def qry_get_final_league_gameweek():
    with Session(engine) as sess:
        gameweek_id = sess.query(League.league_id, League.gameweek_id).order_by(League.league_id.desc()).first()
    return gameweek_id


def qry_get_user_league_info(user_id_):
    with Session(engine) as sess:
        league_ids = sess.query(UserLeague.league_id).filter_by(user_id=user_id_).all()
    lis = []
    for i in league_ids:
        lis.append(i[0])
    with Session(engine) as sess:
        output_lis = []
        for j in lis:
            league_info = sess.query(League.league_id, League.league_name, League.gameweek_id).filter_by(
                league_id=j).first()
            output_lis.append(league_info)
    return output_lis


def qry_id_to_team(team_id_):
    with Session(engine) as sess:
        team_name = sess.query(Team.team_abb).filter_by(team_id=team_id_).first()
    return team_name[0]


def qry_get_user_name(user_ids):
    with Session(engine) as sess:
        user_names = []
        for user_id in user_ids:
            user_name = sess.query(User.first_name, User.last_name).filter_by(user_id=user_id[0]).first()
            user_names.append(user_name)
    return user_names


def qry_get_user_ids(league_id_):
    with Session(engine) as sess:
        user_ids = sess.query(UserLeague.user_id).filter_by(league_id=league_id_).all()
    return user_ids


def qry_get_selection(league_id_, user_id_):
    with Session(engine) as sess:
        selections = sess.query(Selection.user_id, Selection.team_id, Selection.gameweek_id).filter_by(league_id=league_id_).all()
    return selections

def qry_get_games(user_id_, league_id_):
    with Session(engine) as sess:
        selections = sess.query(Selection.team_id, Selection.gameweek_id).filter_by(league_id=league_id_, user_id=user_id_).all()
    print(selections)
    return selections