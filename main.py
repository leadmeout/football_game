import json
import names
import os
import pandas as pd
import random
import sys
import time

from typing import Callable, Dict, List
import uuid
from models.database import MongoDB

"""
TO DO:

1. store game results in a chart (kreuztabelle)

4. add index based on points

5. add squad

"""


def generate_teams():
    """
    Creates the teams for the league
    """

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

    teams = {}

    for count in range(1, 9):
        team = random.choice(cities)
        name = random.choice(nouns)

        cities.pop(cities.index(team))
        nouns.pop(nouns.index(name))

        teams[team] = {
            'name': name,
            'squad': {},
            'played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'points': 0,
            'goals_for': 0,
            'goals_against': 0,
            'goal_difference': 0,
        }

    teams['Toronto'] = {
        'name': 'Blizzard',
        'squad': {},
        'played': 0,
        'wins': 0,
        'losses': 0,
        'draws': 0,
        'points': 0,
        'goals_for': 0,
        'goals_against': 0,
        'goal_difference': 0,
    }

    return teams


def _check_if_bye_week(sorted_match_days, match):
    """
    If a team if paired with a 0, it means that team has a bye week and no games on this match day.
    This function will remove that match and return the next game in the list as match

    If the match containing a 0 is the last in the list, the function will return None as the list is empty.
    """

    if 0 in match:
        match_days[sorted_match_days[0]].pop(0)
        return match_days[sorted_match_days[0]][0]
    else:
        return match


def generate_table(teams: dict):
    """
    Create the league table
    """

    league_table = {
        'Team': [f"{team} {teams[team]['name']}" for team in teams],
        'Points': [teams[team]['points'] for team in teams],
        'GP': [teams[team]['played'] for team in teams],
        'Wins': [teams[team]['wins'] for team in teams],
        'Losses': [teams[team]['losses'] for team in teams],
        'Draws': [teams[team]['draws'] for team in teams],
        'GF': [teams[team]['goals_for'] for team in teams],
        'GA': [teams[team]['goals_against'] for team in teams],
        'GD': [teams[team]['goal_difference'] for team in teams],
    }

    df = pd.DataFrame(league_table,
                      columns=['Team', 'Points', 'GP', 'Wins',
                               'Losses', 'Draws', 'GF', 'GA', 'GD'], index=[
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


def get_next_match():
    print()
    match_days_with_matches = {
        k: v for k, v in match_days.items() if len(v) > 0}
    sorted_match_days = sorted(
        match_days_with_matches, key=lambda k: len(match_days_with_matches[k]))
    match = match_days[sorted_match_days[0]][0]
    return match, sorted_match_days


def _remove_match_(sorted_match_days):
    del match_days[sorted_match_days[0]][0]


def simulate_match(get_next_match: Callable) -> None:
    """Simulates the next match in the schedule. Skips matches which are bye games,
        indicated by a 0 in the match day."""

    match, sorted_match_days = get_next_match()

    if 0 not in match:

        home_team = match[0]
        away_team = match[1]

        home_score = random.randint(0, 8)
        away_score = random.randint(0, 8)

        result = [[(home_team, home_score), (away_team, away_score)]]

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

        teams[home_team]['goals_for'] += home_score
        teams[home_team]['goals_against'] += away_score

        teams[away_team]['goals_for'] += away_score
        teams[away_team]['goals_against'] += home_score

        match_day_results[sorted_match_days[0]] += result

    _remove_match_(sorted_match_days)


def simulate_match_day():
    match_days_with_matches = {
        k: v for k, v in match_days.items() if len(v) > 0}

    sorted_match_days = sorted(
        match_days_with_matches, key=lambda k: len(match_days_with_matches[k]))

    match_day = match_days[sorted_match_days[0]]

    for match in match_day:
        if 0 in match:
            match_day.remove(match)

    for _ in range(len(match_day)):
        simulate_match(get_next_match)


def simulate_season():
    match_days_with_matches = {
        k: v for k, v in match_days.items() if len(v) > 0}

    sorted_match_days = sorted(
        match_days_with_matches, key=lambda k: len(match_days_with_matches[k]))

    match_day = match_days[sorted_match_days[0]]

    for day in range(len(match_days)):
        simulate_match_day()


def point_calculator(teams) -> None:
    """
    Calculate how many points each team has based on wins and draws (losses award no points)
    """
    for team in teams:
        teams[team]['points'] = (
                                        teams[team]['wins'] * 3) + teams[team]['draws']

        teams[team]['goal_difference'] = teams[team]['goals_for'] - \
                                         teams[team]['goals_against']


def match_day_teams(match_day) -> List[str]:
    match_day_list = []

    for elem in match_day:
        match_day_list.append(list(elem)[0])
        match_day_list.append(list(elem)[1])

    return match_day_list


def match_day_results_generator(arg):
    """
    Generate and return an empty dictionary with the match day numbers as the keys.

    This dictionary will store the results of each match.
    """

    teams_dict = arg.find_one()
    team_list = []

    for team_name in teams_dict:
        team_list.append(team_name)

    # the first entry is the id, remove it from the list
    team_list = team_list[1:]

    if len(team_list) % 2:
        team_list.append(0)

    match_day_number = 2 * len(team_list) - 2
    results_dict = {k: [] for k in range(1, match_day_number + 1)}

    str_results_dict = dict([(str(k), v) for k, v in results_dict.items()])

    return str_results_dict


def match_day_generator(arg):
    """
    Arg = teams_collection
    Create a schedule in which each teams plays every other team two times,
    once as the home team and again as the away team
    """

    # Get the teams document from the database
    teams_dict = arg.find_one()
    team_list = []

    for team_name in teams_dict:
        team_list.append(team_name)

    # the first entry is the id, remove it from the list
    team_list = team_list[1:]

    random.shuffle(team_list)
    match_day_number = 2 * len(team_list) - 2
    match_days_dict = {k: [] for k in range(1, match_day_number + 1)}

    if len(team_list) % 2:
        team_list.append(0)

    n = len(team_list)

    matches = []
    fixtures = []
    return_matches = []

    for fixture in range(1, n):
        for i in range(n // 2):
            matches.append((team_list[i], team_list[n - 1 - i]))
            return_matches.append((team_list[n - 1 - i], team_list[i]))
        team_list.insert(1, team_list.pop())
        fixtures.insert(len(fixtures) // 2, matches)
        fixtures.append(return_matches)
        matches = []
        return_matches = []

    fixtures = list(enumerate(fixtures, 1))

    count = 1
    for fixture in fixtures:
        match_days_dict[fixture[0]] = fixture[1]
        count += 1

    # new dict with str conversion for keys
    str_match_days = dict([(str(k), v) for k, v in match_days_dict.items()])

    return str_match_days


def _check_season_over_condition():
    count = 0
    for day in match_days:
        try:
            if len(match_days[day]) > 0:
                count += 1
        except TypeError:
            count += 0

    if count == 0:
        new_game = input("Start a new season with new teams?\n")

        if new_game == "y":
            for file in game_files:
                os.remove(file)

            collection_teams.delete_one({})
            collection_match_days.delete_one({})
            collection_match_day_results.delete_one({})

            print("Game files have been deleted.")
            sys.exit()
        else:
            print("Exiting game.")
            sys.exit()


def setup_game():
    required = {'teams': generate_teams,
                'match_days': match_day_generator,
                'match_day_results': match_day_results_generator,
                }

    current_collections = mdb.db.list_collection_names()

    print(current_collections)

    for collection in required.keys():
        print(collection)

        if collection not in current_collections:
            if collection == 'teams':
                print("Creating teams")
                teams_collection = required[collection]()
                mdb.write_teams_to_database(teams_collection)

            elif collection == 'match_days':
                teams_collection = mdb.db['teams']
                print(f"Creating collection {collection}.")
                res = required[collection](teams_collection)
                mdb.write_match_days_to_database(res)

            elif collection == 'match_day_results':
                teams_collection = mdb.db['teams']
                print(f"Creating collection {collection}.")
                res = required[collection](teams_collection)
                mdb.write_match_day_results_to_database(res)

        elif mdb.db[collection].estimated_count == 0:
            print(f"Collection {collection} exists and count is 0")
        else:
            print(f"{collection} exists.")

    return mdb.db['teams'], mdb.db['match_days'], mdb.db['match_day_results']


if __name__ == "__main__":

    db_address = 'localhost'
    db_port_number = 27017
    db_name = 'fbg'

    mdb = MongoDB(db_address, db_port_number, db_name)

    teams, match_days, match_day_results = setup_game()

    try:
        simulate_match(get_next_match)
        # simulate_season()
        # simulate_match_day()
    except IndexError:
        league_table = generate_table(teams)
        print(league_table)
        _check_season_over_condition()

    point_calculator(teams)
    league_table = generate_table(teams)
    print(league_table)

    # save_file(teams, match_days)
    mdb.write_teams_to_database(teams)
    mdb.write_match_days_to_database(match_days)
    mdb.write_match_day_results_to_database(match_day_results)

    _check_season_over_condition()
