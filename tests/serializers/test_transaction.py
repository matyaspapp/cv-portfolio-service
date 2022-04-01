import unittest

from copy import deepcopy
from datetime import datetime

from app.serializers.transaction import TransactionSerializer
from tests.serializers.consts import INVALID_TEST_TRANSACTIONS, VALID_TEST_TRANSACTIONS


VALID_TEST_TRANSACTIONS = deepcopy(VALID_TEST_TRANSACTIONS)
INVALID_TEST_TRANSACTIONS = deepcopy(INVALID_TEST_TRANSACTIONS)


class TransactionSerializerOneTest(unittest.TestCase):
    def test_getWrongTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, TransactionSerializer.serialize_one, 3)
        self.assertRaises(TypeError, TransactionSerializer.serialize_one, 3.14)
        self.assertRaises(TypeError, TransactionSerializer.serialize_one, 'foo')
        self.assertRaises(TypeError, TransactionSerializer.serialize_one, True)

    def test_getWrongSizeInput_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={'foo': 'bar'}
        )

    def test_getDictWithWrongKeys_raiseValuError(self) -> None:
        # Accept only: _id, owner_id, asset, amount, price, currency, tags, date, type
        for transaction in INVALID_TEST_TRANSACTIONS:
            self.assertRaises(
                ValueError,
                TransactionSerializer.serialize_one,
                transaction=transaction
            )

    def test_getValidTransactionDict_returnWellFormedTransactionDict(self) -> None:
        # well formed:
        # - change _id:ObjectId to id:str with same value
        transaction_data = VALID_TEST_TRANSACTIONS[0]

        serialized_transaction_data = TransactionSerializer.serialize_one(transaction_data)

        self.assertNotIn('_id', serialized_transaction_data)
        self.assertIsInstance(serialized_transaction_data['id'], str)
        self.assertIsInstance(serialized_transaction_data['owner_id'], str)
        self.assertEqual(
            str(transaction_data['_id']),
            serialized_transaction_data['id']
        )
        self.assertEqual(
            {
                'id': '61f5b2c4a3ed85c67a304e5e',
                'owner_id': 'e5e403a76c58de3a4c2b5f16',
                'asset': 'BTC',
                'amount': 0.314,
                'historical_price': 11680,
                'currency': 'USD',
                'tags': [],
                'date': datetime(2022, 2, 4),
                'type': 'buy'
            },
            serialized_transaction_data
        )


class TransactionSerializerManyTest(unittest.TestCase):
    def test_getWrongTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, TransactionSerializer.serialize_many, 3)
        self.assertRaises(TypeError, TransactionSerializer.serialize_many, 3.14)
        self.assertRaises(TypeError, TransactionSerializer.serialize_many, 'foo')
        self.assertRaises(TypeError, TransactionSerializer.serialize_many, True)
        self.assertRaises(TypeError, TransactionSerializer.serialize_many, {'foo': 'bar'})

    def test_getEmpyList_returnEmptyList(self) -> None:
        serialized_transactions = TransactionSerializer.serialize_many([])
        self.assertEqual([], serialized_transactions)

    def test_getWrongSizedTransactionData_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_many,
            [{'foo': 'bar'}]
        )

    def test_getDictWithWrongKeys_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_many,
            INVALID_TEST_TRANSACTIONS
        )

    def test_getValidTransactionDicts_returnListWithWellFormedTransactions(self) -> None:
        # well formed:
        # - change _id:ObjectId to id:str with same value
        serialized_transactions = TransactionSerializer.serialize_many(VALID_TEST_TRANSACTIONS)
        self.assertEqual(
            {
                'id': '61f5b2c4a3ed85c67a304e5e',
                'owner_id': 'e5e403a76c58de3a4c2b5f16',
                'asset': 'BTC',
                'amount': 0.314,
                'historical_price': 11680,
                'currency': 'USD',
                'tags': [],
                'date': datetime(2022, 2, 4),
                'type': 'buy'
            },
            serialized_transactions[0]
        )
        self.assertEqual(
            {
                'id': 'e5e403a76c58de3a4c2b5f16',
                'owner_id': '61f5b2c4a3ed85c67a304e5e',
                'asset': 'BTC',
                'amount': 0.314,
                'historical_price': 11680,
                'currency': 'USD',
                'tags': [],
                'date': datetime(2022, 2, 4),
                'type': 'buy'
            },
            serialized_transactions[1]
        )
