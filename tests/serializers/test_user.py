import unittest

from app.serializers.user import UserSerializer
from tests.serializers.consts import INVALID_TEST_USERS, VALID_TEST_USERS

class UserSerializerOneTest(unittest.TestCase):
    def test_getWrongTypeInput_raiseTypeError(self) -> None:
        self.assertRaises(TypeError, UserSerializer.serialize_one, 3)
        self.assertRaises(TypeError, UserSerializer.serialize_one, 3.14)
        self.assertRaises(TypeError, UserSerializer.serialize_one, 'foo')
        self.assertRaises(TypeError, UserSerializer.serialize_one, True)

    def test_getWrongSizeInput_raiseValueError(self) -> None:
        self.assertRaises(
            ValueError,
            UserSerializer.serialize_one,
            {'foo': 'bar'}
        )

    def test_getDictWithWrongKeys_raiseValueError(self) -> None:
        # Accept only: _id, username, hashed_password
        for user in INVALID_TEST_USERS:
            self.assertRaises(
                ValueError,
                UserSerializer.serialize_one,
                user=user
            )

    def test_getValidUserDict_returnWellFormedUserDict(self) -> None:
        # well formed:
        # - change _id:ObjectId to id:str with same value
        user_data = VALID_TEST_USERS[0]

        serialized_user_data = UserSerializer.serialize_one(user_data)

        self.assertNotIn('_id', serialized_user_data)
        self.assertIsInstance(serialized_user_data['id'], str)
        self.assertEqual(
            str(user_data['_id']),
            serialized_user_data['id']
        )
        self.assertEqual(
            {
                'id': '61f5b2c4a3ed85c67a304e5e',
                'username': 'testuser',
            },
            serialized_user_data
        )
