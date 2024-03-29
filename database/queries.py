from sqlalchemy import create_engine
from database.models import Base, User, Gameweek, League, UserLeague, Selection, Team
from sqlalchemy.orm import Session
import hashlib

engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=False)
Base.metadata.create_all(engine)


def qry_add_user(first_name_, last_name_, username_, password_):
    '''
    A function that is used to add a user to the database

    Parameters
    ----------
    first_name_: first name of the user
    last_name_: last name of the user
    username_: username of the user
    password_: password of the user

    '''
    try:
        hasher = hashlib.sha256()
        hasher.update(bytes(password_, 'utf-8'))
        hasher = hasher.hexdigest()
        password_ = hasher
        with Session(engine) as sess:
            user = User(first_name=first_name_, last_name=last_name_, username=username_, password=password_)
            sess.add(user)
            sess.commit()
    except:
        raise ValueError("Username already exists")


def qry_add_league(gameweek_id_, league_name_):
    '''
    This function is used to add a league to the database
    Parameters
    ----------
    gameweek_id_
    league_name_
    '''
    with Session(engine) as sess:
        league = League(gameweek_id=gameweek_id_, league_name=league_name_)
        sess.add(league)
        sess.commit()


def qry_get_username_details(username_entry):
    '''
    This function is used to get the user_id, password for a given username

    Parameters
    ----------
    username_entry - username of user

    Returns
    a list containing user_id, username and password
    '''
    with Session(engine) as sess:
        output_lis = sess.query(User.user_id, User.username, User.password).filter_by(
            username=username_entry).first()
    return output_lis


# def qry_get_gameweek_timings():
#    with Session(engine) as sess:
#        output_lis = sess.query(Gameweek.start_date).all()
#    return output_lis


def qry_get_gameweek_id():
    '''
    This function is used to show all the gameweek start dates and their gameweek ids

    Returns
    -------
    a list of all the gameweek start dates and the corresponding gameweek id
    '''
    with Session(engine) as sess:
        output_id = sess.query(Gameweek.gameweek_id, Gameweek.start_date).all()
    return output_id


def qry_add_user_league(user_id_, league_id_):
    """
    This function is used to add a value to the user_league database which is a linking table
    This means that a user has joined a league

    Parameters
    ----------
    user_id_ - user_id of the user
    league_id_ - league_id of the league the user would like to join

    """
    try:
        with Session(engine) as sess:
            user_league_value = UserLeague(user_id=user_id_, league_id=league_id_)
            sess.add(user_league_value)
            sess.commit()
    except:
        raise ValueError("League not found")


def qry_add_selection_list(user_selections):
    """
    This function is used to add a list of user selections to the Selection database
    Parameters
    ----------
    user_selections - List of all selection made by a user in a format that can be directly added to the database
    """
    with Session(engine) as sess:
        sess.add_all(user_selections)
        sess.commit()


# def qry_add_selection(gameweek_id_, user_id_, team_id_, league_id_):
#    with Session(engine) as sess:
#        user_selection = Selection(gameweek_id=gameweek_id_, outcome=None, user_id=user_id_, team_id=team_id_,
#                                   league_id=league_id_)
#        sess.add(user_selection)
#        sess.commit()


def qry_get_teams():
    '''
    This function is used to return a list of all the team names and their team_id
    Returns
    a list of all the team id and corresponding team name

    '''
    with Session(engine) as sess:
        teams = sess.query(Team.team_id, Team.team_name).all()
    lis = []
    for i in teams:
        lis.append(i)
    return lis


def qry_get_league_starting_gameweek(league_id_):
    '''
    This function is used to get the starting gameweek of a league

    Parameters
    ----------
    league_id_ - league id of the league you would like the starting gameweek for

    Returns
    -------
    the starting gameweek of a league
    or a ValueError is the league does not exist

    '''
    try:
        with Session(engine) as sess:
            gameweek = sess.query(League.gameweek_id).filter_by(league_id=league_id_).first()
        return gameweek[0]
    except:
        raise ValueError("League not found")


def qry_get_final_league_gameweek():
    '''
    This function is used to get all the leagues
    Returns
    -------
    A list of all the leagues and their starting gameweek
    '''
    with Session(engine) as sess:
        gameweek_id = sess.query(League.league_id, League.gameweek_id).all()
    return gameweek_id


def qry_get_user_league_info(user_id_):
    '''
    This function is used to return a list of leagues the user is currently part of
    Parameters
    ----------
    user_id_

    Returns
    -------
    a list of the current leagues the user is part of
    '''
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
    '''
    This function converts a team_id to a name abbreviation
    Parameters
    ----------
    team_id_

    Returns
    -------
    The team name abbreviation for corresponding id
    '''
    with Session(engine) as sess:
        team_name = sess.query(Team.team_abb).filter_by(team_id=team_id_).first()
    return team_name[0]


def qry_get_user_name(user_ids):
    '''
    This function is used to get the usernames from a list of user_ids
    Parameters
    ----------
    user_ids - a list of the user ids you would like the username for

    Returns
    -------
    the usernames of the list of user ids

    '''
    with Session(engine) as sess:
        user_names = []
        for user_id in user_ids:
            user_name = sess.query(User.first_name, User.last_name).filter_by(user_id=user_id[0]).first()
            user_names.append(user_name)
    return user_names


def qry_get_user_ids(league_id_):
    '''
    This function is used to get a list of users that are part of a league

    Parameters
    ----------
    league_id_

    Returns
    -------
    a list of user_ids that contain are part of the league with league id: league_id
    '''
    with Session(engine) as sess:
        user_ids = sess.query(UserLeague.user_id).filter_by(league_id=league_id_).all()
    return user_ids


def qry_get_selection(league_id_, user_id_):
    """
    This functin is used to get all the selections a user has made in a specific league

    Parameters
    ----------
    league_id_
    user_id_

    Returns
    -------
    A 2 dimensional list of the selections of the user with each sublist having the data [user_id, team_id, gameweek_id]
    """
    with Session(engine) as sess:
        selections = sess.query(Selection.user_id, Selection.team_id, Selection.gameweek_id).filter_by(
            league_id=league_id_, user_id=user_id_).all()
    return selections


def qry_get_games(user_id_, league_id_):
    """
    This function is used to get all the selections made by a user in a specific league
    Parameters
    ----------
    user_id_
    league_id_

    Returns
    -------
    A 2 dimensional list of the selections of the user with each sublist having the data [team_id, gameweek_id]
    """
    with Session(engine) as sess:
        selections = sess.query(Selection.team_id, Selection.gameweek_id).filter_by(league_id=league_id_,
                                                                                    user_id=user_id_).all()
    return selections


def qry_check_in_league(user_id_, league_id_):
    '''

    Parameters
    ----------
    user_id_
    league_id_

    Returns
    -------
    a list containing a user_league_id if the user if part of this league if not an empty list
    '''
    with Session(engine) as sess:
        selection = sess.query(UserLeague.user_league_id).filter_by(league_id=league_id_, user_id=user_id_).all()
    return selection


def qry_get_league_name(league_id):
    """
    This function is used to get the league name of a league with league id: league_id

    Parameters
    ----------
    league_id

    Returns
    -------
    The league name
    """
    with Session(engine) as sess:
        selection = sess.query(League.league_name).filter_by(league_id=league_id).first()
    return selection[0]


def qry_get_league_starting_datetime(gameweek_id_):
    """
    This function is used ot get the gameweek start_date from the gameweek_id
    Parameters
    ----------
    gameweek_id_

    Returns
    -------
    gameweek start_date
    """
    with Session(engine) as sess:
        gameweek = sess.query(Gameweek.start_date).filter_by(gameweek_id=gameweek_id_).first()
    return gameweek[0]
