import unittest

from copy import deepcopy

from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.repositories.transaction import get_transaction_repository, get_test_transaction_repository
from app.main import portfolio_service

from tests.consts import \
    TEST_VALID_TRANSACTIONS, \
    TEST_INVALID_TRANSACTIONS, \
    TEST_PORTFOLIO


TEST_VALID_TRANSACTIONS = deepcopy(TEST_VALID_TRANSACTIONS)
TEST_INVALID_TRANSACTIONS = deepcopy(TEST_INVALID_TRANSACTIONS)


portfolio_service.dependency_overrides[get_transaction_repository] = \
    get_test_transaction_repository

TEST_CLIENT = TestClient(portfolio_service)


class APITransactionCreateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._mongo_client = MongoClient()
        super().setUp()

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        super().tearDown()

    def test_getInvalidTransactionData_returnHTTP400(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/transactions',
            json=TEST_INVALID_TRANSACTIONS[0]
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Invalid transaction data..'
        )

    def test_getDeficientTransactionData_returnHTTP422(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/transactions',
            json=TEST_INVALID_TRANSACTIONS[1]
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())

    def test_getValidTransactionData_returnHTTP201WithStoredData(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/transactions',
            json=TEST_VALID_TRANSACTIONS[0]
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

        transaction_data_wo_id = {k: v for k, v in response.json().items()
                                       if k != 'id'}
        self.assertEqual(
            transaction_data_wo_id,
            TEST_VALID_TRANSACTIONS[0]
        )


class APITransactionGetByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._mongo_client = MongoClient()
        for transaction in deepcopy(TEST_VALID_TRANSACTIONS):
            self._mongo_client.local['test_api_transactions'].insert_one(transaction)

        cursor = self._mongo_client.local['test_api_transactions'].find({})
        self._inserted_transactions = [transaction for transaction in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        return super().tearDown()


    def test_getInvalidObjectId_returnHTTP404(self) -> None:
        test_id = '73571d'
        response = TEST_CLIENT.get(
            f'/api/v1/transactions/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Transaction is not found..'
        )

    def test_getNonExistsObjectId_returnHTTP404(self) -> None:
        test_id = '61f5b2c4a3ed85c67a304e5e'
        response = TEST_CLIENT.get(
            f'/api/v1/transactions/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Transaction is not found..'
        )

    def test_getExistsObjectId_returnHTTP200WithStoredData(self) -> None:
        test_id = self._inserted_transactions[0]['_id']
        response = TEST_CLIENT.get(
            f'/api/v1/transactions/{test_id}'
        )

        response_transaction = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_transaction['id'],
            str(test_id)
        )
        self.assertEqual(
            {
                k: v for k, v in self._inserted_transactions[0].items()
                     if k != '_id'
            },
            {
                k: v for k, v in response_transaction.items()
                     if k != 'id'
            }
        )


class APITransactionGetAllByAssetTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._mongo_client = MongoClient()
        for transaction in deepcopy(TEST_VALID_TRANSACTIONS):
            self._mongo_client.local['test_api_transactions'].insert_one(transaction)

        cursor = self._mongo_client.local['test_api_transactions'].find({})
        self._inserted_transactions = [transaction for transaction in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        return super().tearDown()

    def test_getNonExistsAsset_returnHTTP200WithEmptyList(self) -> None:
        test_asset = 'thisassetisnotexists'
        response = TEST_CLIENT.get(
            f'/api/v1/transactions?asset={test_asset}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
        self.assertEqual(response.json()['data'], [])

    def test_getExistsTag_returnHTTP200WithListOfTransactionData(self) -> None:
        test_asset = self._inserted_transactions[0]['asset']
        response = TEST_CLIENT.get(
            f'/api/v1/transactions?asset={test_asset}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

        transactions = response.json()['data']
        filtered_transaction_ids = [
            str(transaction['_id'])
            for transaction in self._inserted_transactions
            if transaction['asset'] == test_asset
        ]

        self.assertEqual(len(transactions), len(filtered_transaction_ids))
        for transaction in transactions:
            self.assertIn(transaction['id'], filtered_transaction_ids)


class APITransactionGetAllTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._mongo_client = MongoClient()
        for transaction in deepcopy(TEST_VALID_TRANSACTIONS):
            self._mongo_client.local['test_api_transactions'].insert_one(transaction)

        cursor = self._mongo_client.local['test_api_transactions'].find({})
        self._inserted_transactions = [transaction for transaction in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        return super().tearDown()

    def test_returnHTTP200WithListOfTransactionData(self) -> None:
        response = TEST_CLIENT.get(
            '/api/v1/transactions'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

        transactions = response.json()['data']
        transaction_ids = [
            str(transaction['_id'])
            for transaction in self._inserted_transactions
        ]

        self.assertEqual(len(transactions), len(transaction_ids))
        for transaction in transactions:
            self.assertIn(transaction['id'], transaction_ids)


class APITransactionDeleteByIdTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._mongo_client = MongoClient()
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            for transaction in deepcopy(TEST_VALID_TRANSACTIONS):
                self._mongo_client.local['test_api_transactions'].insert_one(transaction)

            cursor = self._mongo_client.local['test_api_transactions'].find({})
            self._inserted_transactions = [transaction for transaction in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        return super().tearDown()

    def test_getInvalidObjectId_returnHTTP404(self) -> None:
        test_id = '73571d'
        response = TEST_CLIENT.delete(
            f'/api/v1/transactions/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Transaction is not found..'
        )

    def test_getNonExistsObjectId_returnHTTP404(self) -> None:
        test_id = '61f5b2c4a3ed85c67a304e5e'
        response = TEST_CLIENT.delete(
            f'/api/v1/transactions/{test_id}'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Transaction is not found..'
        )

    def test_getExistsObjectId_returnHTTP200WithDeletedData(self) -> None:
        test_id = self._inserted_transactions[0]['_id']
        response = TEST_CLIENT.delete(
            f'/api/v1/transactions/{test_id}'
        )

        cursor = self._mongo_client.local['test_api_transactions'].find({})
        stored_transaction_ids = [str(transaction['_id']) for transaction in cursor]

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
        self.assertNotIn(
            response.json()['data']['id'],
            stored_transaction_ids
        )


class APITransactionCalculatePortfolioTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._mongo_client = MongoClient()
        for transaction in deepcopy(TEST_VALID_TRANSACTIONS):
            self._mongo_client.local['test_api_transactions'].insert_one(transaction)

        cursor = self._mongo_client.local['test_api_transactions'].find({})
        self._inserted_transactions = [transaction for transaction in cursor]

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_transactions'].drop()
        return super().tearDown()

    def test_getPortfolio_returnCalculatedPortfolio(self) -> None:
        response = TEST_CLIENT.get(
            '/api/v1/transactions/portfolio'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
        self.assertEqual(
            response.json()['data']['investment'],
            TEST_PORTFOLIO['investment']
        )
