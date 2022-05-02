from pymongo import MongoClient

TEST_USER_CONN = MongoClient()
TEST_USER_COLLECTION = 'test_users'

TEST_TRANSACTION_CONN = MongoClient()
TEST_TRANSACTION_COLLECTION = 'test_transactions'


TEST_WALLET_CONN = MongoClient()
TEST_WALLET_COLLECTION = 'test_wallets'
