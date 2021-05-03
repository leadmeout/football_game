import names
import pandas as pd
import random
import sys

from typing import Dict, List
from models.database import MongoDB


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
              'Oklahoma', 'Brampton', 'Louisville', 'Toronto']

    nouns = ['Lions', 'Leopards', 'Tigers', 'Wolves', 'Grizzlies',
             'Panthers', 'Bears', 'Thunder', 'Flash', 'Dinosaurs',
             'Bobcats', 'Hawks', 'Eagles', 'Dragons', 'Buffalo', 'Gators',
             'Tornadoes', 'Hurricanes', 'Monsoon', 'Avalanche', 'Blizzard',
             'River Beasts', 'Rhinos', 'Piranhas', 'Monitors', 'Barracudas',
             'Penguins', 'Black Widows', 'Bulls', 'Magic', 'Wizards', 'Cougars',
             'Buzzards']

    new_teams = {}

    for count in range(1, 19):
        team = random.choice(cities)
        name = random.choice(nouns)

        cities.pop(cities.index(team))
        nouns.pop(nouns.index(name))

        new_teams[team] = {
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

    return new_teams


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


def generate_table(arg):
    """
    Create the league table
    """

    table = {
        'Team': [f"{team} {arg[team]['name']}" for team in arg],
        'Points': [arg[team]['points'] for team in arg],
        'GP': [arg[team]['played'] for team in arg],
        'Wins': [arg[team]['wins'] for team in arg],
        'Losses': [arg[team]['losses'] for team in arg],
        'Draws': [arg[team]['draws'] for team in arg],
        'GF': [arg[team]['goals_for'] for team in arg],
        'GA': [arg[team]['goals_against'] for team in arg],
        'GD': [arg[team]['goal_difference'] for team in arg],
    }

    # Create DataFrame
    df = pd.DataFrame(table,
                      columns=['Team', 'Points', 'GP', 'Wins',
                               'Losses', 'Draws', 'GF', 'GA', 'GD'])

    # Sort by Points value
    df.sort_values(by=['Points'], inplace=True, ascending=False)
    # Insert position column at the beginning of the table, starting at 0
    df.insert(0, "Position", [i for i in range(1, len(arg) + 1)])

    # Hide index column
    df = df.to_string(index=False)

    return df


def get_next_match():
    match_days_with_matches = {

        k: v for k, v in match_days_dict.items() if len(v) > 0

    }

    sorted_match_days = sorted(
        match_days_with_matches, key=lambda k: len(match_days_with_matches[k]))

    match = match_days_dict[sorted_match_days[0]][0]

    return match, sorted_match_days


def _remove_match_(sorted_match_days):
    del match_days_dict[sorted_match_days[0]][0]


def simulate_match() -> None:
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
            teams_dict[home_team]['wins'] += 1
            teams_dict[away_team]['losses'] += 1
        elif home_score < away_score:
            teams_dict[home_team]['losses'] += 1
            teams_dict[away_team]['wins'] += 1
        else:
            teams_dict[home_team]['draws'] += 1
            teams_dict[away_team]['draws'] += 1

        teams_dict[home_team]['played'] += 1
        teams_dict[away_team]['played'] += 1

        teams_dict[home_team]['goals_for'] += home_score
        teams_dict[home_team]['goals_against'] += away_score

        teams_dict[away_team]['goals_for'] += away_score
        teams_dict[away_team]['goals_against'] += home_score

        match_day_results_dict[sorted_match_days[0]] += result

    _remove_match_(sorted_match_days)


def simulate_match_day():
    match_days_with_matches = {
        k: v for k, v in match_days_dict.items() if len(v) > 0}

    sorted_match_days = sorted(
        match_days_with_matches, key=lambda k: len(match_days_with_matches[k]))

    match_day = match_days_dict[sorted_match_days[0]]

    for match in match_day:
        if 0 in match:
            match_day.remove(match)

    for _ in range(len(match_day)):
        simulate_match()


def simulate_season():
    for day in range(len(match_days_dict)):
        simulate_match_day()


def point_calculator() -> None:
    """
    Calculate how many points each team has based on wins and draws (losses award no points)
    """
    for team in teams_dict:
        teams_dict[team]['points'] = (
                                             teams_dict[team]['wins'] * 3) + teams_dict[team]['draws']

        teams_dict[team]['goal_difference'] = teams_dict[team]['goals_for'] - \
                                              teams_dict[team]['goals_against']


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

    team_dict = arg.find_one()
    team_list = []

    for team_name in team_dict:
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
    for day in match_days_dict:
        try:
            if len(match_days_dict[day]) > 0:
                count += 1
        except TypeError:
            count += 0

    if count == 0:
        new_game = input("Start a new season with new teams?\n")

        if new_game != "y":

            print("Exiting game.")
            sys.exit()
        else:
            teams.delete_one({})
            match_days.delete_one({})
            match_day_results.delete_one({})

            print("Game files have been deleted.")
            sys.exit()


def generate_match_days_dict(arg) -> Dict:
    md_dict = arg.find_one()
    md_dict = dict([(k, v) for k, v in md_dict.items() if k != "_id"])

    return md_dict


def generate_teams_dict(arg) -> Dict:
    t_dict = arg.find_one()
    t_dict = dict([(k, v) for k, v in t_dict.items() if k != "_id"])
    return t_dict


def generate_match_day_results_dict(arg) -> Dict:
    mdr_dict = arg.find_one()
    mdr_dict = dict([(k, v) for k, v in mdr_dict.items() if k != "_id"])
    return mdr_dict


def setup_game():
    required = {'teams': generate_teams,
                'match_days': match_day_generator,
                'match_day_results': match_day_results_generator,
                }

    current_collections = mdb.db.list_collection_names()

    for collection in required.keys():
        if (collection not in current_collections) or (len(list(mdb.db[collection].find())) == 0):
            if collection == 'teams':

                teams_collection = required[collection]()
                mdb.write_teams_to_database(teams_collection)

            elif collection == 'match_days':
                teams_collection = mdb.db['teams']

                res = required[collection](teams_collection)
                mdb.write_match_days_to_database(res)

            elif collection == 'match_day_results':
                teams_collection = mdb.db['teams']

                res = required[collection](teams_collection)
                mdb.write_match_day_results_to_database(res)

    return mdb.db['teams'], mdb.db['match_days'], mdb.db['match_day_results']


if __name__ == "__main__":

    db_address = 'localhost'
    db_port_number = 27017
    db_name = 'fbg'

    mdb = MongoDB(db_address, db_port_number, db_name)
    teams, match_days, match_day_results = setup_game()

    match_days_dict = generate_match_days_dict(match_days)
    match_day_results_dict = generate_match_day_results_dict(match_day_results)
    teams_dict = generate_teams_dict(teams)

    try:
        # simulate_match()
        simulate_season()
        # simulate_match_day()
    except IndexError:
        league_table = generate_table(teams_dict)
        print(league_table)
        _check_season_over_condition()

    point_calculator()
    league_table = generate_table(teams_dict)
    print(league_table)

    mdb.write_teams_to_database(teams_dict)
    mdb.write_match_days_to_database(match_days_dict)
    mdb.write_match_day_results_to_database(match_day_results_dict)

    _check_season_over_condition()
