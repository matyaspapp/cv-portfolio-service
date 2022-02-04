import unittest
from bson import ObjectId
from datetime import datetime
from app import serializers

from app.serializers.transaction import TransactionSerializer


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
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                'foo': 1,
                'owner_id': 2,
                'asset': 3,
                'amount': 4,
                'price': 5,
                'currency': 6,
                'tags': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'foo': 2,
                'asset': 3,
                'amount': 4,
                'price': 5,
                'currency': 6,
                'tags': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'foo': 3,
                'amount': 4,
                'price': 5,
                'currency': 6,
                'tags': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'asset': 3,
                'foo': 4,
                'price': 5,
                'currency': 6,
                'tags': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'asset': 3,
                'amount': 4,
                'foo': 5,
                'currency': 6,
                'tags': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'asset': 3,
                'amount': 4,
                'price': 5,
                'foo': 6,
                'tags': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'asset': 3,
                'amount': 4,
                'price': 5,
                'currency': 6,
                'foo': 7,
                'date': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'asset': 3,
                'amount': 4,
                'price': 5,
                'currency': 6,
                'tags': 7,
                'foo': 8,
                'type': 9
            }
        )
        self.assertRaises(
            ValueError,
            TransactionSerializer.serialize_one,
            transaction={
                '_id': 1,
                'owner_id': 2,
                'asset': 3,
                'amount': 4,
                'price': 5,
                'currency': 6,
                'tags': 7,
                'date': 8,
                'foo': 9
            }
        )

    def test_getValidTransactionDict_returnWellFormedTransactionDict(self) -> None:
        # well formed:
        # - change _id:ObjectId to id:str with same value
        transaction_data = {
            '_id': ObjectId('61f5b2c4a3ed85c67a304e5e'),
            'owner_id': ObjectId('e5e403a76c58de3a4c2b5f16'),
            'asset': 'BTC',
            'amount': 0.314,
            'price': 11680,
            'currency': 'USD',
            'tags': [],
            'date': datetime(2022, 2, 4),
            'type': 'buy'
        }

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
                'price': 11680,
                'currency': 'USD',
                'tags': [],
                'date': datetime(2022, 2, 4),
                'type': 'buy'
            },
            serialized_transaction_data
        )


class TransactionSerializerManyTest(unittest.TestCase):
    def test_getEmpyList_returnEmptyList(self) -> None:
        serialized_transactions = TransactionSerializer.serialize_many([])
        self.assertEqual([], serialized_transactions)
