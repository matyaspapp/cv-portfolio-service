from bson import ObjectId
from datetime import datetime


VALID_TEST_TRANSACTIONS = [
    {
        '_id': ObjectId('61f5b2c4a3ed85c67a304e5e'),
        'owner_id': ObjectId('e5e403a76c58de3a4c2b5f16'),
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': [],
        'date': datetime(2022, 2, 4),
        'type': 'buy'
    },
    {
        '_id': ObjectId('e5e403a76c58de3a4c2b5f16'),
        'owner_id': ObjectId('61f5b2c4a3ed85c67a304e5e'),
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': [],
        'date': datetime(2022, 2, 4),
        'type': 'buy'
    }
]


INVALID_TEST_TRANSACTIONS = [
    {
        'foo': 1,
        'owner_id': 2,
        'asset': 3,
        'amount': 4,
        'historical_price': 5,
        'currency': 6,
        'tags': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'foo': 2,
        'asset': 3,
        'amount': 4,
        'historical_price': 5,
        'currency': 6,
        'tags': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'foo': 3,
        'amount': 4,
        'historical_price': 5,
        'currency': 6,
        'tags': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'asset': 3,
        'foo': 4,
        'historical_price': 5,
        'currency': 6,
        'tags': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'asset': 3,
        'amount': 4,
        'foo': 5,
        'currency': 6,
        'tags': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'asset': 3,
        'amount': 4,
        'historical_price': 5,
        'foo': 6,
        'tags': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'asset': 3,
        'amount': 4,
        'historical_price': 5,
        'currency': 6,
        'foo': 7,
        'date': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'asset': 3,
        'amount': 4,
        'historical_price': 5,
        'currency': 6,
        'tags': 7,
        'foo': 8,
        'type': 9
    },
    {
        '_id': 1,
        'owner_id': 2,
        'asset': 3,
        'amount': 4,
        'historical_price': 5,
        'currency': 6,
        'tags': 7,
        'date': 8,
        'foo': 9
    }
]
