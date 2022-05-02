import unittest

from copy import deepcopy

from app.serializers.wallet import WalletSerializer
from tests.serializers.consts import INVALID_TEST_WALLETS, VALID_TEST_WALLETS


VALID_TEST_WALLETS = deepcopy(VALID_TEST_WALLETS)
INVALID_TEST_WALLETS = deepcopy(INVALID_TEST_WALLETS)


class WalletSerializerOneTest(unittest.TestCase):
    def test_getWrongTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, WalletSerializer.serialize_one, 3)
        self.assertRaises(TypeError, WalletSerializer.serialize_one, 3.14)
        self.assertRaises(TypeError, WalletSerializer.serialize_one, 'foo')
        self.assertRaises(TypeError, WalletSerializer.serialize_one, True)

    def test_getWrongSizeInput_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            WalletSerializer.serialize_one,
            wallet={'foo': 'bar'}
        )

    def test_getDictWithWrongKeys_raiseValueError(self) -> None:
        # Accept only: _id, owner_id, address, chain
        for wallet in INVALID_TEST_WALLETS:
            self.assertRaises(
                ValueError,
                WalletSerializer.serialize_one,
                wallet=wallet
            )

    def test_getValidWalletData_returnWellFormedWalletDict(self) -> None:
        # well formed:
        # - _id:ObjectId to id:str with same value
        wallet_data = VALID_TEST_WALLETS[0]

        serialized_wallet_data = WalletSerializer.serialize_one(wallet_data)

        self.assertNotIn('_id', serialized_wallet_data)
        self.assertIsInstance(serialized_wallet_data['id'], str)
        self.assertIsInstance(serialized_wallet_data['owner_id'], str)
        self.assertEqual(
            str(wallet_data['_id']),
            serialized_wallet_data['id']
        )
        self.assertEqual(
            {
                'id': '61f5b2c4a3ed85c67a304e5e',
                'owner_id': 'e5e403a76c58de3a4c2b5f16',
                'address': 'testwalletaddress',
                'chain': 'testchain'
            },
            serialized_wallet_data
        )


class WalletSerializerManyTest(unittest.TestCase):
    def test_getWrongTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, WalletSerializer.serialize_many, 3)
        self.assertRaises(TypeError, WalletSerializer.serialize_many, 3.14)
        self.assertRaises(TypeError, WalletSerializer.serialize_many, 'foo')
        self.assertRaises(TypeError, WalletSerializer.serialize_many, True)
        self.assertRaises(TypeError, WalletSerializer.serialize_many, {'foo': 'bar'})

    def test_getEmptyList_returnEmptyList(self) -> None:
        serialized_wallets = WalletSerializer.serialize_many([])
        self.assertEqual([], serialized_wallets)

    def test_getWrongSizedWalletData_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            WalletSerializer.serialize_many,
            [{'foo': 'bar'}]
        )

    def test_getDictWithWrongKeys_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            WalletSerializer.serialize_many,
            INVALID_TEST_WALLETS
        )

    def test_getValidTransactionDicts_returnListWithWellFormedTransactions(self) -> None:
        # well formed:
        # - change _id:ObjectId to id:str with same value
        serialized_wallets = WalletSerializer.serialize_many(VALID_TEST_WALLETS)
        self.assertEqual(
            {
                'id': '61f5b2c4a3ed85c67a304e5e',
                'owner_id': 'e5e403a76c58de3a4c2b5f16',
                'address': 'testwalletaddress',
                'chain': 'testchain'
            },
            serialized_wallets[0]
        )
        self.assertEqual(
            {
                'id': 'e5e403a76c58de3a4c2b5f16',
                'owner_id': '61f5b2c4a3ed85c67a304e5e',
                'address': 'testwalletaddress',
                'chain': 'testchain'
            },
            serialized_wallets[1]
        )
