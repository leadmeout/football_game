import json, random
import pandas as pd


# Define a dictionary of teams
# each team has its own set of information including location, name, squad, win/loss record

cities = ['New York', 'Toronto', 'Los Angeles',
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


def generate_teams(cities, nouns):

    teams['Toronto'] = {
                        'name' : 'Blizzard',
                        'squad' : {},
                        'played' : 0,
                        'wins' : 0,
                        'losses' : 0,
                        'draws' : 0,
                        'points' : 0,
                                    }


    for team in range(0, 8):
        teams[random.choice(cities)] = {
                                        'name' : random.choice(nouns),
                                        'squad' : {},
                                        'played' : 0,
                                        'wins' : 0,
                                        'losses' : 0,
                                        'draws' : 0,
                                        'points' : 0,
                                        }

    with open('teams.json', 'w') as f:
        json.dump(teams, f)

generate_teams(cities, nouns)
