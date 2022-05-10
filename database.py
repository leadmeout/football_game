from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import certifi

class Database:
    """
    Connect to Mongo DB to store team information, match days and match day results
    """
    def __init__(self):

        # self.client = MongoClient('localhost', username='mrkhrvt', password='QCHPJfygttTsCq8u',authSource='fbg',authMechanism='SCRAM-SHA-256')
        self.client = MongoClient("mongodb+srv://mrkhrvt:QCHPJfygttTsCq8u@cluster0.quncg.mongodb.net/fbg?retryWrites=true&w=majority", server_api=ServerApi('1'), tlsCAFile=certifi.where())
        self.db = self.client['fbg']
        self.collection_teams = self.db['teams']
        self.collection_match_days = self.db['match_days']
        self.collection_match_day_results = self.db['match_day_results']

    def print_function(self):
        print(self.client)

    def write_teams_to_database(self, dict):
        self.collection_teams.drop()
        self.collection_teams.insert_one(dict)

    def write_match_days_to_database(self, dict):
        self.collection_match_days.drop()
        self.collection_match_days.insert_one(dict)

    def write_match_day_results_to_database(self, dict):
        self.collection_match_day_results.drop()
        self.collection_match_day_results.insert_one(dict)
