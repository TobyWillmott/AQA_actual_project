import requests
import json


def api_match_info(game_week_id):
    url = f"https://fantasy.premierleague.com/api/fixtures/?event={game_week_id}"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    lis_game_week = []
    for active_case in parse_json:
        lis = [active_case['team_h'], active_case['team_h_difficulty'], active_case['team_a'],
               active_case['team_a_difficulty']]
        lis_game_week.append(lis)
    return lis_game_week


def api_check_points(user_ids, league_id, selections):
    url = "https://fantasy.premierleague.com/api/fixtures/"
    lives = []
    response = requests.get(url)
    data = response.json()
    for i in selections:
        print("this is a selection", i)
    for user in selections:
        num_points = 0
        for user_id, team_id, gameweek_id in user:
            for match in data:
                if match["event"] == gameweek_id and (match["team_a"] == team_id or match["team_h"] == team_id):
                    if match["team_a"] == team_id:
                        if match["team_a_score"] is None or match["team_h_score"] is None:
                            break
                        elif match["team_a_score"] == match["team_h_score"]:
                            num_points += 1
                        elif match["team_a_score"] > match["team_h_score"]:
                            num_points += 3
                    elif match["team_h"] == team_id:
                        if match["team_a_score"] is None or match["team_h_score"] is None:
                            break
                        elif match["team_a_score"] == match["team_h_score"]:
                            num_points += 1
                        elif match["team_a_score"] < match["team_h_score"]:
                            num_points += 3
        lives.append(num_points)
        print("lives", num_points)
    return lives


def get_games(user_selections):
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = requests.get(url)
    data = response.json()

    game_data = []
    for team_id, gameweek_id in user_selections:
        print("user selection: ", user_selections)
        for match in data:
            if match["event"] == gameweek_id and (match["team_a"] == team_id or match["team_h"] == team_id):
                if match["team_a"] == team_id:
                    game_data.append(
                        [gameweek_id, team_id, match["team_a_score"], match["team_a_difficulty"], match["team_h"],
                         match["team_h_score"], match["team_h_difficulty"]])
                if match["team_h"] == team_id:
                    team_a_id = match["team_a"]
                    game_data.append([gameweek_id, team_id, match["team_h_score"], match["team_h_difficulty"], match["team_a"],
                         match["team_a_score"], match["team_a_difficulty"]])
    return game_data

def team_playing(gameweek_id, team_id):
    url = f"https://fantasy.premierleague.com/api/fixtures/?event={gameweek_id}"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    for active_case in parse_json:
        if active_case['team_h'] == team_id:
            print("returning true")
            return True
        elif active_case['team_a'] == team_id:
            print("returning true")
            return True
    print("returning false")
    return False
