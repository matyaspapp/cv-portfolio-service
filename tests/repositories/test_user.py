import jwt
import unittest

from bson import ObjectId
from copy import deepcopy

from app.database.service import CRUDService
from app.repositories.user import UserRepository
from app.serializers.user import UserSerializer

from tests.consts import TEST_VALID_USERS, TEST_INVALID_USERS

from tests.repositories.settings import \
    TEST_USER_CONN, \
    TEST_USER_COLLECTION

from tests.utils import tag


class UserRepositoryCreateTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._TEST_INVALID_USERS = deepcopy(TEST_INVALID_USERS)

        self._crud_service = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        self._serializer = UserSerializer()

        test_crud_engine = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        test_serializer = UserSerializer()
        self._repository = UserRepository(test_crud_engine, test_serializer)

    def tearDown(self) -> None:
        super().tearDown()
        TEST_USER_CONN.local[TEST_USER_COLLECTION].drop()

    def test_getWrongSizeUserData_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            self._repository.create,
            {'foo': 'bar'}
        )

    def test_getWrongDictKeys_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            self._repository.create,
            self._TEST_INVALID_USERS[0]
        )

    def test_getEmptyPassword_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            self._repository.create,
            self._TEST_INVALID_USERS[1]
        )

    def test_getValidUserData_returnSerializedData(self) -> None:
        test_user = self._TEST_VALID_USERS[0]
        new_serialized_user = self._repository.create(test_user)
        test_user['_id'] = ObjectId(new_serialized_user['id'])
        test_serialized_user = self._serializer.serialize_one(test_user)
        self.assertEqual(test_serialized_user, new_serialized_user)


class UserRepositoryGetUserByUsernameTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._TEST_INVALID_USERS = deepcopy(TEST_INVALID_USERS)

        self._crud_service = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        self._serializer = UserSerializer()

        test_crud_engine = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        test_serializer = UserSerializer()
        self._repository = UserRepository(test_crud_engine, test_serializer)

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._crud_service.create(self._TEST_VALID_USERS[0])

    def tearDown(self) -> None:
        super().tearDown()
        TEST_USER_CONN.local[TEST_USER_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnEmptyDict(self) -> None:
        lookup_user = self._repository.get_by_username('whateverdbisempty')
        self.assertEqual(lookup_user, {})

    def test_getNonExistsUsername_returnEmptyDict(self) -> None:
        lookup_user = self._repository.get_by_username('thisuserdoesnotexists')
        self.assertEqual(lookup_user, {})

    def test_getExistsUsername_returnSerializedUserData(self) -> None:
        lookup_user = self._repository.get_by_username('testuser')
        test_user = self._TEST_VALID_USERS[0]
        test_user['_id'] = ObjectId(lookup_user['id'])
        test_serialized_user = self._serializer.serialize_one(test_user)
        self.assertEqual(lookup_user, test_serialized_user)


class UserRepositoryGetAuthenticatedUserTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._TEST_INVALID_USERS = deepcopy(TEST_INVALID_USERS)

        self._crud_service = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        self._serializer = UserSerializer()

        test_crud_engine = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        test_serializer = UserSerializer()
        self._repository = UserRepository(test_crud_engine, test_serializer)

        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'empty_db' not in tags:
            self._crud_service.create(self._TEST_VALID_USERS[0])

    def tearDown(self) -> None:
        super().tearDown()
        TEST_USER_CONN.local[TEST_USER_COLLECTION].drop()

    @tag('empty_db')
    def test_getEmptyDb_returnUnauthenticated(self) -> None:
        authenticate_data = self._repository.get_authenticated_user(
            'whateverdbisempty',
            ''
        )
        self.assertEqual(
            authenticate_data,
            {'authenticated': False, 'user': {}}
        )

    def test_getNonExistsUsername_returnUnauthenticated(self) -> None:
        authenticate_data = self._repository.get_authenticated_user(
            'thisuserdoesnotexists',
            ''
        )
        self.assertEqual(
            authenticate_data,
            {'authenticated': False, 'user': {}}
        )

    def test_getWrongPassword_returnUnauthenticated(self) -> None:
        authenticate_data = self._repository.get_authenticated_user(
            'testuser',
            'thisisnotmypassword'
        )
        self.assertEqual(
            authenticate_data,
            {'authenticated': False, 'user': {}}
        )

    def test_getValidUserData_returnAuthenticated(self) -> None:
        test_user = self._TEST_VALID_USERS[0]
        authenticate_data = self._repository.get_authenticated_user(
            test_user['username'],
            test_user['hashed_password']
        )
        self.assertEqual(
            authenticate_data,
            {'authenticated': True, 'user': authenticate_data['user']}
        )


class UserRepositoryCreateJWTTokenTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._TEST_INVALID_USERS = deepcopy(TEST_INVALID_USERS)

        self._JWT_SECRET = 'testjwtsecret'

        test_crud_engine = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        test_serializer = UserSerializer()
        self._repository = UserRepository(test_crud_engine, test_serializer)

    def test_getWrongTypePayload_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, self._repository.generate_jwt_token, 3)
        self.assertRaises(TypeError, self._repository.generate_jwt_token, 3.14)
        self.assertRaises(TypeError, self._repository.generate_jwt_token, 'foo')
        self.assertRaises(TypeError, self._repository.generate_jwt_token, True)

    def test_getWrongTypeSecret_raiseTypeError(self) -> None:
        self.assertRaises(
            TypeError,
            self._repository.generate_jwt_token,
            {}, 3
        )
        self.assertRaises(
            TypeError,
            self._repository.generate_jwt_token,
            {}, 3.14
        )
        self.assertRaises(
            TypeError,
            self._repository.generate_jwt_token,
            {}, {}
        )
        self.assertRaises(
            TypeError,
            self._repository.generate_jwt_token,
            {}, True
        )

    def test_getUserData_returnDictWithJWTToken(self) -> None:
        test_user = self._repository.create(self._TEST_VALID_USERS[0])
        jwt_data = UserRepository.generate_jwt_token(
            test_user,
            self._JWT_SECRET
        )

        payload = jwt.decode(
            jwt_data['access_token'],
            self._JWT_SECRET,
            algorithms=['HS256']
        )

        self.assertEqual(
            set(jwt_data.keys()),
            {'access_token', 'token_type'}
        )

        self.assertEqual(
            set(payload.keys()),
            {'id', 'username'}
        )


class UserRepositoryVerifyJWTTokenTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self._TEST_VALID_USERS = deepcopy(TEST_VALID_USERS)
        self._TEST_INVALID_USERS = deepcopy(TEST_INVALID_USERS)

        self._JWT_SECRET = 'testjwtsecret'

        test_crud_engine = CRUDService(
            TEST_USER_CONN,
            TEST_USER_COLLECTION
        )
        test_serializer = UserSerializer()
        self._repository = UserRepository(test_crud_engine, test_serializer)

    def test_getWrongTypeToken_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, self._repository.verify_jwt_token, 3)
        self.assertRaises(TypeError, self._repository.verify_jwt_token, 3.14)
        self.assertRaises(TypeError, self._repository.verify_jwt_token, True)

    def test_getWrongTypeSecret_raiseTypeError(self) -> None:
        self.assertRaises(
            TypeError,
            self._repository.verify_jwt_token,
            'jwttoken', 3
        )
        self.assertRaises(
            TypeError,
            self._repository.verify_jwt_token,
            'jwttoken', 3.14
        )
        self.assertRaises(
            TypeError,
            self._repository.verify_jwt_token,
            'jwt_token', True
        )

    def test_getInvalidToken_returnFalse(self) -> None:
        verified_data = self._repository.verify_jwt_token(
            'itisaninvalidjwttoken',
            self._JWT_SECRET
        )
        self.assertEqual(
            verified_data,
            {'authorized': False, 'username': ''}
        )

    def test_getWrongToken_returnFalse(self) -> None:
        wrong_token = jwt.encode(
            {'foo': 'bar'},
            self._JWT_SECRET,
            algorithm='HS256'
        )

        verified_data = self._repository.verify_jwt_token(
            wrong_token,
            self._JWT_SECRET
        )

        self.assertEqual(
            verified_data,
            {'authorized': False, 'username': ''}
        )

    def test_getValidToken_returnTrue(self) -> None:
        valid_token = jwt.encode(
            {'username': 'testuser'},
            self._JWT_SECRET,
            algorithm='HS256'
        )

        verified_data = self._repository.verify_jwt_token(
            valid_token,
            self._JWT_SECRET
        )

        self.assertEqual(
            verified_data,
            {'authorized': True, 'username': 'testuser'}
        )


# TODO:
# class UserRepositoryUpdateByUsernameTest(unittest.TestCase):
#     pass


# class UserRepositoryDeleteByUsernameTest(unittest.TestCase):
#     pass
