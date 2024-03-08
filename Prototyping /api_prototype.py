import requests
import json

def get_info():
    url = f"https://fantasy.premierleague.com/api/fixtures"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    lis_data = []
    for active_case in parse_json:
        lis = [active_case['team_h'], active_case['team_h_difficulty'], active_case['team_a'],
               active_case['team_a_difficulty']]
        lis_data.append(lis)
    print(lis_data)

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