import unittest

from copy import deepcopy

from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.repositories.user import get_user_repository, get_test_user_repository
from app.main import portfolio_service

from tests.consts import \
    TEST_VALID_USERS, \
    TEST_INVALID_USERS

portfolio_service.dependency_overrides[get_user_repository] = \
    get_test_user_repository

TEST_CLIENT = TestClient(portfolio_service)


class APIUserCreateTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._TEST_INVALID_USERS = deepcopy(TEST_INVALID_USERS)
        self._mongo_client = MongoClient()

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_users'].drop()
        super().tearDown()

    def test_getInvalidUserData_returnHTTP400(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/users',
            json=self._TEST_INVALID_USERS[1]
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Invalid user data..'
        )

    def test_getValidUserData_returnHTTP201WithStoredData(self) -> None:
        test_user = self._TEST_VALID_USERS[0]
        response = TEST_CLIENT.post(
            '/api/v1/users',
            json=test_user
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            set(response.json()),
            {'access_token', 'token_type'}
        )

    def test_getExistsUsername_returnHTTP400(self) -> None:
        test_user = self._TEST_VALID_USERS[0]
        response_first = TEST_CLIENT.post(
            '/api/v1/users',
            json=test_user
        )

        response_second = TEST_CLIENT.post(
            '/api/v1/users',
            json=test_user
        )

        self.assertEqual(response_first.status_code, 201)
        self.assertEqual(response_second.status_code, 400)
        self.assertIn('detail', response_second.json())
        self.assertEqual(
            response_second.json()['detail'],
            'This username is already taken..'
        )


class APIUserAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._mongo_client = MongoClient()
        self._mongo_client.local['test_api_users'].insert_one(
            self._TEST_VALID_USERS[0]
        )

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_users'].drop()
        super().tearDown()

    def test_getInvalidUsername_return401(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/users/auth',
            {'username': 'foo', 'password': 'foo'}
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Invalid credentials..'
        )

    def test_getInvalidPassword_return401(self) -> None:
        response = TEST_CLIENT.post(
            '/api/v1/users/auth',
            {'username': 'testuser', 'password': 'foo'}
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.json())
        self.assertEqual(
            response.json()['detail'],
            'Invalid credentials..'
        )

    def test_getValidUserData_return200WithAccessToken(self) -> None:
        test_user = self._TEST_VALID_USERS[0]
        response = TEST_CLIENT.post(
            '/api/v1/users/auth',
            {
                'username': test_user['username'],
                'password': test_user['hashed_password']
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        self.assertIn('token_type', response.json())
        self.assertEqual(
            response.json()['token_type'],
            'bearer'
        )


class APIUserGetCurrentUserTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._test_user = self._TEST_VALID_USERS[0]
        self._mongo_client = MongoClient()
        self._mongo_client.local['test_api_users'].insert_one(self._test_user)
        # login
        self._auth_user = TEST_CLIENT.post(
            '/api/v1/users/auth',
            {
                'username': self._test_user['username'],
                'password': self._test_user['hashed_password']
            }
        ).json()

    def tearDown(self) -> None:
        self._mongo_client.local['test_api_users'].drop()
        super().tearDown()

    def test_getWithoutToken_returnHTTP401(self) -> None:
        response = TEST_CLIENT.get(
            '/api/v1/users/me'
        )

        self.assertEqual(response.status_code, 401)

    def test_getValidToken_returnHTTP200WithUsername(self) -> None:
        response = TEST_CLIENT.get(
            '/api/v1/users/me',
            headers={
                'Authorization': f'''Bearer {self._auth_user['access_token']}'''
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['username'],
            self._test_user['username']
        )
