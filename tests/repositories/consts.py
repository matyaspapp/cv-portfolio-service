from datetime import datetime


TEST_VALID_TRANSACTIONS = [
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': ['retire'],
        'date': datetime(2022, 2, 4),
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'ETH',
        'amount': 0.314,
        'historical_price': 3342,
        'currency': 'USD',
        'tags': ['fun'],
        'date': datetime(2022, 2, 4),
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.420,
        'historical_price': 13690,
        'currency': 'USD',
        'tags': ['fun'],
        'date': datetime(2022, 2, 21),
        'type': 'buy'
    },
]

TEST_INVALID_TRANSACTIONS = [
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': [],
        'date': datetime(2022, 2, 4),
        'foo': 'bar'
    }
]
