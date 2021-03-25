from pymongo import MongoClient

class Database:
    """
    Connect to Mongo DB to store team information, match days and match day results
    """
    def __init__(self):

        self.client = MongoClient('localhost', 27017)
        self.db = self.client['fbg']
        self.collection_teams = self.db['teams']
        self.collection_match_days = self.db['match_days']
        self.collection_match_day_results = self.db['match_day_results']

    def print_function(self):
        print(self.client)
