from pymongo import MongoClient

TEST_CONN = MongoClient()
TEST_COLLECTION = 'test_items'
TEST_ITEM = {'test': 'item'}
