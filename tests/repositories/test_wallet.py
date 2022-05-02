import unittest

from bson import ObjectId
from bson.errors import InvalidId
from copy import deepcopy

from app.database.service import CRUDService
from app.repositories.wallet import WalletRepository
from app.serializers.wallet import WalletSerializer

from tests.consts import \
    TEST_INVALID_WALLETS, \
    TEST_VALID_WALLETS \

from tests.repositories.settings import \
    TEST_WALLET_CONN, \
    TEST_WALLET_COLLECTION

from tests.utils import tag


class WalletRepositoryCreateTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_WALLETS = deepcopy(TEST_VALID_WALLETS)
        self._TEST_INVALID_WALLETS = deepcopy(TEST_INVALID_WALLETS)

        self._crud_service = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        self._serializer = WalletSerializer()

        test_crud_engine = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        test_serializer = WalletSerializer()
        self._repository = WalletRepository(test_crud_engine, test_serializer)

    def tearDown(self) -> None:
        super().tearDown()
        TEST_WALLET_CONN.local[TEST_WALLET_COLLECTION].drop()

    def test_getWrongSizeWalletData_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            self._repository.create,
            {'foo': 'bar'}
        )

    def test_getWrongOwnerObjectId_raiseInvalidId(self) -> None:
        test_wallet = self._TEST_INVALID_WALLETS[0]
        self.assertRaises(
            InvalidId,
            self._repository.create,
            test_wallet
        )

    def test_getWrongDictKeys_raiseValueError(self) -> None:
        test_wallet = self._TEST_INVALID_WALLETS[1]
        self.assertRaises(
            ValueError,
            self._repository.create,
            test_wallet
        )

    def test_getValidWalletData_returnSerializedData(self) -> None:
        test_wallet = self._TEST_VALID_WALLETS[0]
        new_serialized_wallet = self._repository.create(test_wallet)
        test_wallet['_id'] = ObjectId(new_serialized_wallet['id'])
        test_serialized_wallet = self._serializer.serialize_one(test_wallet)
        self.assertEqual(test_serialized_wallet, new_serialized_wallet)


class WalletRepositoryGetByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_WALLETS = deepcopy(TEST_VALID_WALLETS)
        self._TEST_INVALID_WALLETS = deepcopy(TEST_INVALID_WALLETS)

        self._crud_service = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        self._serializer = WalletSerializer()

        test_crud_engine = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        test_serializer = WalletSerializer()
        self._repository = WalletRepository(test_crud_engine, test_serializer)
        self._inserted_wallet_id = str(self._crud_service.create(
            self._TEST_VALID_WALLETS[0]
        ).inserted_id)

    def tearDown(self) -> None:
        super().tearDown()
        TEST_WALLET_CONN.local[TEST_WALLET_COLLECTION].drop()

    def test_getInvalidObjectId_raiseInvalidId(self) -> None:
        self.assertRaises(
            InvalidId,
            self._repository.get_by_id,
            '73570wn3r1d'
        )

    def test_getNonExistsId_returnEmptyDict(self) -> None:
        wallet = self._repository.get_by_id(
            self._inserted_wallet_id[::-1]
        )
        self.assertEqual(wallet, {})

    def test_getExistsId_returnSerializedDict(self) -> None:
        test_wallet, = self._crud_service.get_all()
        test_wallet = self._serializer.serialize_one(test_wallet)
        wallet = self._repository.get_by_id(test_wallet['id'])
        self.assertDictEqual(wallet, test_wallet)


class WalletRepositoryGetAllTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_WALLETS = deepcopy(TEST_VALID_WALLETS)
        self._TEST_INVALID_WALLETS = deepcopy(TEST_INVALID_WALLETS)

        self._crud_service = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        self._serializer = WalletSerializer()

        test_crud_engine = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        test_serializer = WalletSerializer()
        self._repository = WalletRepository(test_crud_engine, test_serializer)

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._crud_service.create(self._TEST_VALID_WALLETS[0])
            self._crud_service.create(self._TEST_VALID_WALLETS[1])

    def tearDown(self) -> None:
        super().tearDown()
        TEST_WALLET_CONN.local[TEST_WALLET_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyList(self) -> None:
        self.assertEqual(self._repository.get_all(), [])

    def test_getNonEmptyDb_returnListOfSerializedData(self) -> None:
        test_wallets = self._serializer.serialize_many(
            self._crud_service.get_all()
        )
        wallets = self._repository.get_all()
        self.assertEqual(test_wallets, wallets)


class WalletRepositoryUpdateByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_WALLETS = deepcopy(TEST_VALID_WALLETS)
        self._TEST_INVALID_WALLETS = deepcopy(TEST_INVALID_WALLETS)

        self._crud_service = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        self._serializer = WalletSerializer()

        test_crud_engine = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        test_serializer = WalletSerializer()
        self._repository = WalletRepository(test_crud_engine, test_serializer)

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                self._TEST_VALID_WALLETS
            ))

    def tearDown(self) -> None:
        super().tearDown()
        TEST_WALLET_CONN.local[TEST_WALLET_COLLECTION].drop()

    def test_getInvalidTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(
            TypeError,
            self._repository.update_by_id,
            3, update_data={}
        )
        self.assertRaises(
            TypeError,
            self._repository.update_by_id,
            3.14, update_data={}
        )
        self.assertRaises(
            TypeError,
            self._repository.update_by_id,
            True, update_data={}
        )

    def test_getInvalidObjectId_raiseInvalidId(self) -> None:
        self.assertRaises(
            InvalidId,
            self._repository.update_by_id,
            id='73570wn3r1d',
            update_data={}
        )

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyDict(self) -> None:
        updated_wallet = self._repository.update_by_id(
            '61f5b2c4a3ed85c67a304e5e',
            {}
        )
        self.assertEqual(updated_wallet, {})

    def test_getNonExistsId_returnEmptyDict(self) -> None:
        updated_wallet = self._repository.update_by_id(
            '61f5b2c4a3ed85c67a304e5e',
            {}
        )
        self.assertEqual(updated_wallet, {})

    def test_getExistsIdWithWrongDataKey_raiseValueError(self) -> None:
        serialized_test_wallet = self._serializer.serialize_one(
            self._crud_service.get_by_id(self._test_items_id[0])
        )
        self.assertRaises(
            ValueError,
            self._repository.update_by_id,
            serialized_test_wallet['id'],
            {'foo': 'bar'}
        )

    def test_getExistsId_returnupdatedSerializedData(self) -> None:
        updated_wallet = self._repository.update_by_id(
            self._test_items_id[0],
            {'chain': 'trc20'}
        )
        serialized_updated_test_wallet = self._serializer.serialize_one(
            self._crud_service.get_by_id(self._test_items_id[0])
        )
        self.assertEqual(
            updated_wallet,
            serialized_updated_test_wallet
        )


class WalletRepositoryDeleteByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_WALLETS = deepcopy(TEST_VALID_WALLETS)
        self._TEST_INVALID_WALLETS = deepcopy(TEST_INVALID_WALLETS)

        self._crud_service = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        self._serializer = WalletSerializer()

        test_crud_engine = CRUDService(
            TEST_WALLET_CONN,
            TEST_WALLET_COLLECTION
        )
        test_serializer = WalletSerializer()
        self._repository = WalletRepository(test_crud_engine, test_serializer)

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._test_items_id = list(map(
                lambda new_item: self._crud_service.create(new_item).inserted_id,
                self._TEST_VALID_WALLETS
            ))

    def tearDown(self) -> None:
        super().tearDown()
        TEST_WALLET_CONN.local[TEST_WALLET_COLLECTION].drop()

    def test_getInvalidTypeInput_raiseTypeError(self) -> None:
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
        deleted_wallet = self._repository.delete_by_id(
            '61f5b2c4a3ed85c67a304e5e'
        )
        self.assertEqual(deleted_wallet, {})

    def test_getNonExistsId_returnEmptyDict(self) -> None:
        deleted_wallet = self._repository.delete_by_id(
            '61f5b2c4a3ed85c67a304e5e'
        )
        self.assertEqual(deleted_wallet, {})

    def test_getExistsId_deleteDataAndReturnSerializedDeletedData(self) -> None:
        all_wallet_data = self._serializer.serialize_many(
            self._crud_service.get_all()
        )
        target_wallet = all_wallet_data[0]
        deleted_item = self._repository.delete_by_id(target_wallet['id'])
        all_wallet_data_after = self._serializer.serialize_many(
            self._crud_service.get_all()
        )
        self.assertEqual(target_wallet, deleted_item)
        self.assertIn(deleted_item, all_wallet_data)
        self.assertNotIn(deleted_item, all_wallet_data_after)
        self.assertEqual(
            len(all_wallet_data),
            len(all_wallet_data_after) + 1
        )
