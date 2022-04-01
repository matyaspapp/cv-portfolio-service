import unittest

from bson import ObjectId
from bson.errors import InvalidId
from copy import deepcopy

from app.database.service import CRUDService
from app.repositories.transaction import TransactionRepository
from app.serializers.transaction import TransactionSerializer

from tests.consts import \
    TEST_INVALID_TRANSACTIONS, \
    TEST_VALID_TRANSACTIONS, \
    TEST_PORTFOLIO

from tests.repositories.settings import \
    TEST_TRANSACTION_CONN, \
    TEST_TRANSACTION_COLLECTION

from tests.utils import tag


TEST_VALID_TRANSACTIONS = deepcopy(TEST_VALID_TRANSACTIONS)
TEST_INVALID_TRANSACTIONS = deepcopy(TEST_INVALID_TRANSACTIONS)


class TransactionRepositoryCreateTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(test_crud_engine, test_serializer)

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    def test_getWrongSizeTransactionData_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            self._repository.create,
            {'foo': 'bar'}
        )

    def test_getWrongOwnerObjectId_raiseInvalidId(self) -> None:
        self.assertRaises(
            InvalidId,
            self._repository.create,
            TEST_INVALID_TRANSACTIONS[0]
        )

    def test_getWrongDictKeys_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            self._repository.create,
            TEST_INVALID_TRANSACTIONS[1]
        )

    def test_getValidTransactionData_returnSerializedData(self) -> None:
        test_transaction = TEST_VALID_TRANSACTIONS[0]
        new_serialized_transaction = self._repository.create(test_transaction)
        test_transaction['_id'] = ObjectId(new_serialized_transaction['id'])
        test_serialized_transaction = self._serializer.serialize_one(test_transaction)
        self.assertEqual(test_serialized_transaction, new_serialized_transaction)


class TransactionRepositoryGetByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(test_crud_engine, test_serializer)
        self._crud_service.create(TEST_VALID_TRANSACTIONS[0])

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    def test_getInvalidObjectId_raiseInvalidId(self) -> None:
        self.assertRaises(
            InvalidId,
            self._repository.get_by_id,
            '73570wn3r1d'
        )

    def test_getNonExistsId_returnEmptyDict(self) -> None:
        transaction = self._repository.get_by_id('61f5b2c4a3ed85c67a304e5e')
        self.assertDictEqual(transaction, {})

    def test_getExistsId_returnSerializedDict(self) -> None:
        test_transaction, = self._crud_service.get_all()
        test_transaction = self._serializer.serialize_one(test_transaction)
        transaction = self._repository.get_by_id(test_transaction['id'])
        self.assertDictEqual(transaction, test_transaction
)


class TransactionRepositoryGetAllTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(test_crud_engine, test_serializer)

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._crud_service.create(TEST_VALID_TRANSACTIONS[0])
            self._crud_service.create(TEST_VALID_TRANSACTIONS[1])

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyList(self) -> None:
        self.assertEqual(self._repository.get_all(), [])

    def test_getNonEmptyDb_returnListOfSerializedData(self) -> None:
        test_transactions = self._serializer.serialize_many(
            self._crud_service.get_all()
        )
        transactions = self._repository.get_all()
        self.assertEqual(test_transactions, transactions)


class TransactionRepositoryGetAllByAssetTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(
            test_crud_engine,
            test_serializer
        )

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                TEST_VALID_TRANSACTIONS
            ))

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyList(self) -> None:
        transactions_by_tag = self._repository.get_all_by_asset('foo')
        self.assertEqual(transactions_by_tag, [])

    def test_getNonExistsTag_returnEmptyList(self) -> None:
        transactions_by_tag = self._repository.get_all_by_asset('foo')
        self.assertEqual(transactions_by_tag, [])

    def test_getExistsId_returnListOfSerializedData(self) -> None:
        transactions_eth, = self._repository.get_all_by_asset('ETH')
        test_transaction_eth = self._serializer.serialize_one(
            self._crud_service.get_by_id(self._test_items_id[1])
        )
        transactionss_btc = self._repository.get_all_by_asset('BTC')
        test_transactions_btc = [
            self._serializer.serialize_one(
                self._crud_service.get_by_id(self._test_items_id[0])
            ),
            self._serializer.serialize_one(
                self._crud_service.get_by_id(self._test_items_id[2])
            )
        ]
        self.assertEqual(transactions_eth, test_transaction_eth)
        self.assertEqual(len(transactionss_btc), 2)
        self.assertListEqual(transactionss_btc, test_transactions_btc)


class TransactionRepositoryGetAllByTagTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(
            test_crud_engine,
            test_serializer
        )

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                TEST_VALID_TRANSACTIONS
            ))

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyList(self) -> None:
        transactions_by_tag = self._repository.get_all_by_tag('foo')
        self.assertEqual(transactions_by_tag, [])

    def test_getNonExistsTag_returnEmptyList(self) -> None:
        transactions_by_tag = self._repository.get_all_by_tag('foo')
        self.assertEqual(transactions_by_tag, [])

    def test_getExistsId_returnListOfSerializedData(self) -> None:
        transaction_retire, = self._repository.get_all_by_tag('retire')
        test_transaction_retire = self._serializer.serialize_one(
            self._crud_service.get_by_id(self._test_items_id[0])
        )
        transactions_fun = self._repository.get_all_by_tag('fun')
        test_transactions_fun = [
            self._serializer.serialize_one(
                self._crud_service.get_by_id(self._test_items_id[1])
            ),
            self._serializer.serialize_one(
                self._crud_service.get_by_id(self._test_items_id[2])
            )
        ]
        self.assertEqual(transaction_retire, test_transaction_retire)
        self.assertEqual(len(transactions_fun), 2)
        self.assertListEqual(transactions_fun, test_transactions_fun)


# TODO: !!! allowed fields !!!
class TransactionRepositoryUpdateByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(
            test_crud_engine,
            test_serializer
        )

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                TEST_VALID_TRANSACTIONS
            ))

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    def test_getInvalidTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, self._repository.update_by_id, 3, update_data={})
        self.assertRaises(TypeError, self._repository.update_by_id, 3.14, update_data={})
        self.assertRaises(TypeError, self._repository.update_by_id, True, update_data={})

    def test_getInvalidObjectId_raiseInvalidId(self) -> None:
        self.assertRaises(
            InvalidId,
            self._repository.update_by_id,
            id='73570wn3r1d',
            update_data={}
        )

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyDict(self) -> None:
        updated_transaction = self._repository.update_by_id(
            '61f5b2c4a3ed85c67a304e5e',
            {}
        )
        self.assertEqual(updated_transaction, {})

    def test_getNonExistsId_returnEmptyDict(self) -> None:
        updated_transaction = self._repository.update_by_id(
            '61f5b2c4a3ed85c67a304e5e',
            {}
        )
        self.assertEqual(updated_transaction, {})

    def test_getExistsIdWithWrongDataKey_raiseValueError(self) -> None:
        serialized_test_transaction = self._serializer.serialize_one(
            self._crud_service.get_by_id(self._test_items_id[0])
        )
        self.assertRaises(
            ValueError,
            self._repository.update_by_id,
            serialized_test_transaction['id'],
            {'foo': 'bar'}
        )

    def test_getExistsId_returnUpdatedSerializedData(self) -> None:
        updated_transaction = self._repository.update_by_id(
            self._test_items_id[0],
            {'amount': 42}
        )
        serialized_updated_test_transaction = self._serializer.serialize_one(
            self._crud_service.get_by_id(self._test_items_id[0])
        )
        self.assertEqual(
            updated_transaction,
            serialized_updated_test_transaction
        )


class TransactionRepositoryDeleteByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(
            test_crud_engine,
            test_serializer
        )

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                TEST_VALID_TRANSACTIONS
            ))

    def tearDown(self) -> None:
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()
        return super().tearDown()

    def test_getInvalidTypeInput_raiseInvalidId(self) -> None:
        self.assertRaises(TypeError, self._repository.delete_by_id, 3)
        self.assertRaises(TypeError, self._repository.delete_by_id, 3.14)
        self.assertRaises(TypeError, self._repository.delete_by_id, True)

    def test_getInvalidObjectId_raiseInvalidId(self) -> None:
        self.assertRaises(
            InvalidId,
            self._repository.delete_by_id,
            id='73570wn3r1d'
        )

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyDict(self) -> None:
        deleted_transaction = self._repository.delete_by_id(
            '61f5b2c4a3ed85c67a304e5e',
        )
        self.assertEqual(deleted_transaction, {})

    def test_getNonExistsId_returnEmptyDict(self) -> None:
        updated_transaction = self._repository.delete_by_id(
            '61f5b2c4a3ed85c67a304e5e'
        )
        self.assertEqual(updated_transaction, {})

    def test_getExistsId_deleteDataAndReturnSerializedDeletedData(self) -> None:
        all_transaction_data = self._serializer.serialize_many(
            self._crud_service.get_all()
        )
        target_transaction = all_transaction_data[0]
        self.assertIn(target_transaction, all_transaction_data)
        deleted_item = self._repository.delete_by_id(target_transaction['id'])
        all_transaction_data_after = self._serializer.serialize_many(
            self._crud_service.get_all()
        )
        self.assertEqual(target_transaction, deleted_item)
        self.assertIn(deleted_item, all_transaction_data)
        self.assertNotIn(deleted_item, all_transaction_data_after)
        self.assertEqual(
            len(all_transaction_data),
            len(all_transaction_data_after) + 1
        )


class TransactionRepositoryCalculatePortfolioTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._crud_service = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        self._serializer = TransactionSerializer()

        test_crud_engine = CRUDService(
            TEST_TRANSACTION_CONN,
            TEST_TRANSACTION_COLLECTION
        )
        test_serializer = TransactionSerializer()
        self._repository = TransactionRepository(
            test_crud_engine,
            test_serializer
        )

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                TEST_VALID_TRANSACTIONS
            ))

    def tearDown(self) -> None:
        super().tearDown()
        TEST_TRANSACTION_CONN.local[TEST_TRANSACTION_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyDict(self) -> None:
        self.assertEqual(self._repository.calculate_portfolio(), {})

    def test_getTestDb_returnCalculatedPortfolio(self) -> None:
        portfolio = self._repository.calculate_portfolio()

        self.assertAlmostEqual(
            portfolio['investment'],
            TEST_PORTFOLIO['investment']
        )

        for asset_data, test_asset_data \
        in zip(portfolio['assets'].values(), TEST_PORTFOLIO['assets'].values()):
            self.assertAlmostEqual(
                asset_data['meta']['amount'],
                test_asset_data['meta']['amount']
            )
            self.assertAlmostEqual(
                asset_data['meta']['average_price'],
                test_asset_data['meta']['average_price']
            )
            self.assertAlmostEqual(
                asset_data['meta']['investment'],
                test_asset_data['meta']['investment']
            )
