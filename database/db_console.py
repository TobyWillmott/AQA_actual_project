from sqlalchemy import create_engine
from models import Base, User, Gameweek, League, UserLeague, Selection, Team
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///database/fantasy_football.sqlite", echo=False)

if __name__ == "__main__":
    # with Session(engine) as sess:
    # Get all the instances of the objects from the DB

    sess = Session(engine)
    users = sess.query(User).all()
    teams = sess.query(Team).all()
    gameweeks = sess.query(Gameweek).all()
    leagues = sess.query(League).all()
    selection = sess.query(Selection).all()

    # Get the user with id=1 from the database
    my_user = sess.get(User, 1)

    # Add a new selections
    my_selection = [Selection(gameweek_id=1,
                              team_id=teams[0].team_id,
                              league_id=leagues[0].league_id),
                    Selection(gameweek_id=2,
                              team_id=4,
                              league_id=leagues[0].league_id),
                    ]

    # These will add the selections to my_user. I.e. they will
    # add the selections into the selections table with user_id equal
    # to the id for my_user
    my_user.selections.extend(my_selection)
    sess.commit()

    # Close the session (comment out the line below if you want to
    # experiment with the objects in the console.
    sess.close()
