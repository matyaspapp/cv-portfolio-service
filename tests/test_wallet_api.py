import unittest

from copy import deepcopy

from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.api.v1.user import get_current_user

from app.repositories.wallet import \
    get_wallet_repository, \
    get_test_wallet_repository

from app.main import portfolio_service

from tests.consts import \
    TEST_VALID_WALLETS, \
    TEST_INVALID_WALLETS


portfolio_service.dependency_overrides[get_current_user] = lambda: {'id': 'e5e403a76c58de3a4c2b5f16'}
portfolio_service.dependency_overrides[get_wallet_repository] = \
    get_test_wallet_repository

TEST_CLIENT = TestClient(portfolio_service)


class APIWalletCreateTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_WALLETS = deepcopy(TEST_VALID_WALLETS)
        self._TEST_INVALID_WALLETS = deepcopy(TEST_INVALID_WALLETS)

        self._mongo_client = MongoClient()

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        super().tearDown()

    def test_getInvalidWalletData_returnHTTP400(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/wallets',
            json=self._TEST_INVALID_WALLETS[0]
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Invalid wallet data..'
        )

    def test_getDeficientWalletData_returnHTTP422(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/wallets',
            json=self._TEST_INVALID_WALLETS[1]
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())

    def test_getValidWalletData_returnHTTP201WithStoredData(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/wallets',
            json=self._TEST_VALID_WALLETS[0]
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

        wallet_data_wo_id = {k: v for k, v in response.json().items()
                                  if k != 'id'}
        self.assertEqual(
            wallet_data_wo_id,
            self._TEST_VALID_WALLETS[0]
        )


class APIWalletGetByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._mongo_client = MongoClient()
        for wallet in deepcopy(TEST_VALID_WALLETS):
            self._mongo_client.local['test_api_wallets'].insert_one(wallet)

        cursor = self._mongo_client.local['test_api_wallets'].find({})
        self._inserted_wallets = [wallet for wallet in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_wallets'].drop()
        return super().tearDown()

    def test_getInvalidObjectId_returnHTTP404(self) -> None:
        test_id = '73571d'
        response = TEST_CLIENT.get(
            f'/api/v1/wallets/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Wallet is not found..'
        )

    def test_getNonExistsObjectId_returnHTTP404(self) -> None:
        test_id = '61f5b2c4a3ed85c67a304e5e'
        response = TEST_CLIENT.get(
            f'/api/v1/wallets/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Wallet is not found..'
        )

    def test_getExistsObjectId_returnHTTP200WithStoredData(self) -> None:
        test_id = self._inserted_wallets[0]['_id']
        response = TEST_CLIENT.get(
            f'/api/v1/wallets/{test_id}'
        )

        response_wallet = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_wallet['id'],
            str(test_id)
        )
        self.assertEqual(
            {
                k: v for k, v in self._inserted_wallets[0].items()
                     if k != '_id'
            },
            {
                k: v for k, v in response_wallet.items()
                     if k != 'id'
            }
        )


class APIWalletGetAllTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._mongo_client = MongoClient()
        for wallet in deepcopy(TEST_VALID_WALLETS):
            self._mongo_client.local['test_api_wallets'].insert_one(wallet)

        cursor = self._mongo_client.local['test_api_wallets'].find({})
        self._inserted_wallets = [wallet for wallet in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_wallets'].drop()
        return super().tearDown()

    def test_returnHTTP200WithListOfWalletData(self) -> None:
        response = TEST_CLIENT.get(
            f'/api/v1/wallets/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

        wallets = response.json()['data']
        wallet_ids = [
            str(wallet['_id'])
            for wallet in self._inserted_wallets
        ]

        self.assertEqual(len(wallets), len(wallet_ids))
        for wallet in wallets:
            self.assertIn(wallet['id'], wallet_ids)


class APIWalletUpdateByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._mongo_client = MongoClient()
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            for wallet in deepcopy(TEST_VALID_WALLETS):
                self._mongo_client.local['test_api_wallets'].insert_one(wallet)

            cursor = self._mongo_client.local['test_api_wallets'].find({})
            self._inserted_wallets = [wallet for wallet in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_wallets'].drop()
        return super().tearDown()

    def test_getInvalidObjectId_returnHTTP400(self) -> None:
        test_id = '73571d'
        response = TEST_CLIENT.put(
            f'/api/v1/wallets/{test_id}',
            json={}
        )

        print(response.text)

        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Wallet could not be updated..'
        )

    def test_getNonExistsObjectId_returnHTTP400(self) -> None:
        test_id = '61f5b2c4a3ed85c67a304e5e'
        response = TEST_CLIENT.put(
            f'/api/v1/wallets/{test_id}',
            json={}
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Wallet could not be updated..'
        )

    def test_getExistsObjectId_returnHTTP200(self) -> None:
        original_wallet = self._inserted_wallets[0]
        update_data = {'chain': 'updatedtestchain1'}
        response = TEST_CLIENT.put(
            f'''/api/v1/wallets/{original_wallet['_id']}''',
            json=update_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['id'],
            str(original_wallet['_id'])
        )
        self.assertEqual(
            response.json()['address'],
            original_wallet['address']
        )
        self.assertNotEqual(
            response.json()['chain'],
            original_wallet['chain']
        )
        self.assertEqual(
            response.json()['chain'],
            'updatedtestchain1'
        )


class APIWalletDeleteTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._mongo_client = MongoClient()
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            for wallet in deepcopy(TEST_VALID_WALLETS):
                self._mongo_client.local['test_api_wallets'].insert_one(wallet)

            cursor = self._mongo_client.local['test_api_wallets'].find({})
            self._inserted_wallets = [wallet for wallet in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_wallets'].drop()
        return super().tearDown()

    def test_getInvalidObjectId_returnHTTP404(self) -> None:
        test_id = '73571d'
        response = TEST_CLIENT.delete(
            f'/api/v1/wallets/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Wallet is not found..'
        )

    def test_getNonExistsObjectId_returnHTTP404(self) -> None:
        test_id = '61f5b2c4a3ed85c67a304e5e'
        response = TEST_CLIENT.delete(
            f'/api/v1/wallets/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Wallet is not found..'
        )

    def test_getExistsObjectId_returnHTTP200WithDeletedData(self) -> None:
        test_id = self._inserted_wallets[0]['_id']
        response = TEST_CLIENT.delete(
            f'/api/v1/wallets/{test_id}'
        )

        cursor = self._mongo_client.local['test_api_wallets'].find({})
        stored_wallet_ids = [str(wallet['_id']) for wallet in cursor]

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
        self.assertNotIn(
            response.json()['data']['id'],
            stored_wallet_ids
        )
