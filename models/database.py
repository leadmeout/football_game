from pymongo import MongoClient


class MongoDB():

    # START DB STUFF

    def __init__(self, address, port_number, db_name):

        # self.client = MongoClient('localhost', 27017)
        self.client = MongoClient(address, port_number)
        # self.db = client['fbg']
        self.db = self.client[db_name]

        self.collection_teams = self.db['teams']
        self.collection_match_days = self.db['match_days']
        self.collection_match_day_results = self.db['match_day_results']


    def write_teams_to_database(self, teams):
        # collection_teams, collection_match_days, collection_match_day_results = connect_to_db()

        document = {}
        self.collection_teams.replace_one(document, teams, True)


    def write_match_days_to_database(self, match_days):
        # collection_teams, collection_match_days, collection_match_day_results = connect_to_db()

        # with open("../data/match_days.json") as f:
        #     data = json.load(f)

        document = {}
        self.collection_match_days.replace_one(document, match_days, True)


    def write_match_day_results_to_database(self, match_day_results):
        # collection_teams, collection_match_days, collection_match_day_results = connect_to_db()

        # with open("../data/match_day_results.json") as f:
        #     data = json.load(f)

        document = {}
        self.collection_match_day_results.replace_one(document, match_day_results, True)

