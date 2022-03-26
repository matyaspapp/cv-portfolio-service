from datetime import datetime


TEST_VALID_TRANSACTIONS = [
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': ['retire'],
        'date': datetime(2022, 2, 4).isoformat(),
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'ETH',
        'amount': 0.314,
        'historical_price': 3342,
        'currency': 'USD',
        'tags': ['fun'],
        'date': datetime(2022, 2, 4).isoformat(),
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.420,
        'historical_price': 13690,
        'currency': 'USD',
        'tags': ['fun'],
        'date': datetime(2022, 2, 21).isoformat(),
        'type': 'buy'
    },
]

TEST_INVALID_TRANSACTIONS = [
    {
        'owner_id': '73570wn3r1d',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': [],
        'date': datetime(2022, 2, 4).isoformat(),
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': [],
        'date': datetime(2022, 2, 4).isoformat(),
        'foo': 'bar'
    }
]

TEST_PORTFOLIO = {
    'investment': 10466.707999999999,
    'assets': {
        'BTC': {
            'meta': {
                'amount': 0.734,
                'investment': 9417.32,
                'average_price': 12830.136239782016
            },
            'transactions': [
                {
                    'owner_id': 'e5e403a76c58de3a4c2b5f16',
                    'asset': 'BTC',
                    'amount': 0.314,
                    'historical_price': 11680,
                    'currency': 'USD',
                    'tags': ['retire'],
                    'date': datetime(2022, 2, 4).isoformat(),
                    'type': 'buy'
                },
                {
                    'owner_id': 'e5e403a76c58de3a4c2b5f16',
                    'asset': 'BTC',
                    'amount': 0.420,
                    'historical_price': 13690,
                    'currency': 'USD',
                    'tags': ['fun'],
                    'date': datetime(2022, 2, 21).isoformat(),
                    'type': 'buy'
                },
            ]
        },
        'ETH': {
            'meta': {
                'amount': 0.314,
                'investment': 1049.388,
                'average_price': 3342
            },
            'transactions': [
                {
                    'owner_id': 'e5e403a76c58de3a4c2b5f16',
                    'asset': 'ETH',
                    'amount': 0.314,
                    'historical_price': 3342,
                    'currency': 'USD',
                    'tags': ['fun'],
                    'date': datetime(2022, 2, 4).isoformat(),
                    'type': 'buy'
                },
            ]
        }
    }
}