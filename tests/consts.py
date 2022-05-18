from datetime import datetime


TEST_VALID_WALLETS = [
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'address': 'testwalletaddress1',
        'chain': 'testchain1'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'address': 'testwalletaddress2',
        'chain': 'testchain2'
    }
]


TEST_INVALID_WALLETS = [
    {
        'owner_id': '73570wn3r1d',
        'address': 'testwalletaddress1',
        'chain': 'testchain'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'address': 'testwalletaddress1',
        'foo': 'bar'
    }
]


TEST_VALID_USERS = [
    {
        'username': 'testuser',
        'hashed_password':  'supersecrethashedpassword'
    },
    {
        'username': 'testuser2',
        'hashed_password':  'supersecrethashedpasswordagain'
    },
]

TEST_INVALID_USERS = [
    {
        'username': 'testuser',
        'foo': 'bar'
    },
    {
        'username': 'testuser',
        'hashed_password': ''
    },
]


TEST_VALID_TRANSACTIONS = [
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': ['retire'],
        'date': '2022-2-4',
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'ETH',
        'amount': 0.314,
        'historical_price': 3342,
        'currency': 'USD',
        'tags': ['fun'],
        'date': '2022-2-4',
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.420,
        'historical_price': 13690,
        'currency': 'USD',
        'tags': ['fun'],
        'date': '2022-2-21',
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
        'date': '2022-2-4',
        'type': 'buy'
    },
    {
        'owner_id': 'e5e403a76c58de3a4c2b5f16',
        'asset': 'BTC',
        'amount': 0.314,
        'historical_price': 11680,
        'currency': 'USD',
        'tags': [],
        'date': '2022-2-4',
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
                    'date': '2022-2-4',
                    'type': 'buy'
                },
                {
                    'owner_id': 'e5e403a76c58de3a4c2b5f16',
                    'asset': 'BTC',
                    'amount': 0.420,
                    'historical_price': 13690,
                    'currency': 'USD',
                    'tags': ['fun'],
                    'date': '2022-2-4',
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
                    'date': '2022-2-4',
                    'type': 'buy'
                },
            ]
        }
    }
}
