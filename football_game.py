import pandas as pd
import random
import json
import os
from typing import Dict, List
import time

"""
TO DO:

1. every team plays every team twice (maybe based on df index??)
2. add goals for, against, difference
3. add index based on points

4. add squad


"""

# Define a dictionary of teams
# each team has its own set of information including location, name, squad,
# win/loss record

cities = ['New York', 'Los Angeles',
          'Chicago', 'Houston', 'Montreal', 'Philadelphia',
          'Phoenix', 'San Antonio', 'San Diego', 'Dallas',
          'Calgary', 'San Jose', 'Edmonton', 'Jacksonville',
          'Austin', 'Ottawa', 'San Francisco', 'Indianapolis',
          'Charlotte', 'Mississauga', 'Seattle', 'Winnipeg',
          'Denver', 'Washington', 'Boston', 'Memphis', 'Vancouver',
          'Oklahoma', 'Brampton', 'Louisville']


nouns = ['Lions', 'Leopards', 'Tigers', 'Wolves', 'Grizzlies',
         'Panthers', 'Bears', 'Thunder', 'Flash', 'Dinosaurs',
         'Bobcats', 'Hawks', 'Eagles', 'Dragons', 'Buffalo', 'Gators',
         'Tornadoes', 'Hurricanes', 'Monsoon', 'Avalanche', 'Blizzard',
         'River Beasts', 'Rhinos', 'Piranhas', 'Monitors', 'Barracudas',
         'Penguins', 'Black Widows', 'Bulls', 'Magic', 'Wizards', 'Cougars',
         'Buzzards']

teams = {

}


def save_file(teams):
    with open('teams.json', 'w') as f:
        json.dump(teams, f)


def generate_teams(cities, nouns):

    for team in range(0, 8):
        teams[random.choice(cities)] = {
            'name': random.choice(nouns),
            'squad': {},
            'played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'points': 0,
        }

    with open('teams.json', 'w') as f:
        json.dump(teams, f)


teams['Toronto'] = {
    'name': 'Blizzard',
    'squad': {},
    'played': 0,
    'wins': 0,
    'losses': 0,
    'draws': 0,
    'points': 0,
}


def generate_table(teams):

    league_table = {
        'Team': [f"{team} {teams[team]['name']}" for team in teams],
        'Games Played': [teams[team]['played'] for team in teams],
        'Wins': [teams[team]['wins'] for team in teams],
        'Losses': [teams[team]['losses'] for team in teams],
        'Draws': [teams[team]['draws'] for team in teams],
        'Points': [teams[team]['points'] for team in teams],
    }

    df = pd.DataFrame(league_table,
                      columns=['Team', 'Games Played', 'Wins',
                               'Losses', 'Draws', 'Points'], index=[
                          i for i in range(1, len(teams) + 1)])
    df.sort_values(by=['Points'], inplace=True, ascending=False)

    return df


def random_game(teams):

    home_score = random.randint(0, 8)
    away_score = random.randint(0, 8)

    home_team = random.choice(list(teams))
    away_team = random.choice(list(teams))

    if home_score > away_score:
        teams[home_team]['wins'] += 1
        teams[away_team]['losses'] += 1
    elif home_score < away_score:
        teams[home_team]['losses'] += 1
        teams[away_team]['wins'] += 1
    else:
        teams[home_team]['draws'] += 1
        teams[away_team]['draws'] += 1

    teams[home_team]['played'] += 1
    teams[away_team]['played'] += 1

    return teams


def simulate_game(match_list):

    i = 1


    for match in match_list:
        home_team, away_team = match
        print(f"Game {i}: {home_team} vs. {away_team}")
        i += 1


def point_calculator(teams):

    for team in teams:
        teams[team]['points'] = (
            teams[team]['wins'] * 3) + teams[team]['draws']

    return teams


def match_day_teams(match_day) -> List[str]:

    match_day_list = []

    for elem in match_day:

        match_day_list.append(list(elem)[0])
        match_day_list.append(list(elem)[1])

    return match_day_list


def match_generator(teams: dict) -> dict:

    team_list = [team for team in teams]
    match_list = []

    # N = x^2-x

    '''
    match_days =    {
                    1: [('Toronto', 'San Jose'), ('Philadelphia', 'Montreal')],
                    2: ('Toronto', 'San Jose'), ('Philadelphia', 'Montreal')}
    '''

    match_day_number = 2 * len(team_list) - 2

    match_days = {k:[] for k in range(1, match_day_number+1)}

    '''

    for i in range(len(team_list)):
        for team in team_list:
            if team != team_list[i]:
                match = (team_list[i], team)
                match_list.append(match)
                #match_days[i+1].append(match)

                '''

    home_games = []
    away_games= []

    for team in team_list:
        for i in range(len(team_list)):
            if team != team_list[i]:
                match_list.append((team, team_list[i]))

    remaining_matches = []

    while len(match_list) > 0:

        skipped_matches = []

        match = match_list[0]
        match_index = match_list.index(match)
        home_team, away_team = match[0], match[1]

        sorted_match_days = sorted(match_days, key=lambda k: len(match_days[k]))

        match_day = match_days[sorted_match_days[0]]

        match_day_list = match_day_teams(match_day)

        # time.sleep(1)
        print(10 * "*")
        print("\n")
        print(f"Match to add:", match)
        print("Current match day before adding: ", match_day)
        print("\n")
        print(10 * "*")

        if (home_team not in match_day_list) and (away_team not in match_day_list):
            if len(match_day) != 4:
                match_day.append(match)
                print(f"{match} was scheduled.")
                # time.sleep(1)
                print("Match day after adding match: ", match_day)
                # time.sleep(1)
        else:
            skipped_matches.append(match)
            print(f"{match} was NOT scheduled and will be thrown back in the list.")
            # time.sleep(1)

        match_list.pop(match_index)
        match_list.extend(skipped_matches)
        random.shuffle(match_list)
        random.shuffle(skipped_matches)

        print("\n", len(match_list))

        for day, matches in match_days.items():
            print(f"Match Day: {day}, Matches: {matches}")
        # time.sleep(1)
        #print(match_days)





    print(remaining_matches)

    for day, matches in match_days.items():
        print(f"Match Day: {day}, Matches: {matches}")




    # print(match_days)

    return match_list


if __name__ == "__main__":

    if os.path.isfile("./teams.json"):
        pass
    else:
        generate_teams(cities, nouns)

    load_teams = open('teams.json')
    teams = json.load(load_teams)

    league_table = generate_table(teams)

    #random_game(teams)
    match_list = match_generator(teams)
    #simulate_game(match_list)
    point_calculator(teams)
    save_file(teams)

    # print(league_table)
