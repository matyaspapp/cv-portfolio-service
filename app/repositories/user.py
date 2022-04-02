import jwt

from pymongo import MongoClient

from app.database.service import CRUDService
from app.schemas.user import User
from app.serializers.user import UserSerializer


class UserRepository:
    def __init__(
        self,
        crud_service: CRUDService,
        serializer: UserSerializer
    ) -> None:
        self._crud_service = crud_service
        self._serializer = serializer

    def create(self, new_user: User) -> dict:
        new_user_dict = dict(new_user)
        valid_keys = {'username', 'hashed_password'}

        if set(new_user_dict.keys()) != valid_keys:
            raise ValueError

        if not new_user_dict['hashed_password']:
            raise ValueError

        inserted_id = self._crud_service.create(new_user_dict).inserted_id
        return self._serializer.serialize_one(
            self._crud_service.get_by_id(inserted_id)
        )

    def get_by_username(self, username: str) -> dict:
        lookup_user = self._crud_service.get_all_by_key('username', username)
        if not lookup_user:
            return {}

        lookup_user, = lookup_user
     
        return self._serializer.serialize_one(lookup_user)

    def get_authenticated_user(self, username: str, password: str) -> dict:
        lookup_user = self.get_by_username(username)
        if not lookup_user:
            return {'authenticated': False, 'user': {}}

        if not password == lookup_user['hashed_password']:
            return {'authenticated': False, 'user': {}}

        return {'authenticated': True, 'user': lookup_user}

    def update_by_username(self, username: str, updated_data: dict) -> dict:
        if not isinstance(username, str):
            raise TypeError

        db_user = self.get_by_username(username)
        if not db_user:
            return {}

        update_result = self._crud_service.update_by_id(
            db_user['id'],
            **updated_data
        )

        return self._serializer.serialize_one(
            self._crud_service.get_by_id(db_user['id'])
        )


    def delete_by_username(self, username: str) -> dict:
        if not isinstance(username, str):
            raise TypeError

        try:
            target_user, = self._crud_service.get_all_by_key('username', username)
        except:
            return {}

        self._crud_service.delete_by_id(target_user['_id'])

        return self._serializer.serialize_one(
            target_user
        )

    @staticmethod
    def generate_jwt_token(user_data: dict, jwt_secret: str = 'SECRETKEY') -> dict:
        if not isinstance(user_data, dict):
            raise TypeError

        if not isinstance(jwt_secret, str):
            raise TypeError

        payload = {
            'id': user_data['id'],
            'username': user_data['username']
        }
        token = jwt.encode(payload, jwt_secret, algorithm='HS256')

        return {
            'access_token': token,
            'token_type': 'bearer'
        }

    @staticmethod
    def verify_jwt_token(jwt_token: str, jwt_secret: str = 'SECRETKEY') -> dict:
        if not isinstance(jwt_token, str):
            raise TypeError

        if not isinstance(jwt_secret, str):
            raise TypeError

        try:
            payload = jwt.decode(jwt_token, jwt_secret, algorithms=['HS256'])
        except:
            return {'authorized': False, 'username': ''}

        if 'username' not in payload:
            return {'authorized': False, 'username': ''}

        return {'authorized': True, 'username': payload['username']}


def get_user_repository():  # pragma: no cover
    connection = MongoClient()
    crud_service = CRUDService(connection, 'users')
    repository = UserRepository(
        crud_service,
        UserSerializer
    )
    return repository


def get_test_user_repository():  # pragma: no cover
    connection = MongoClient()
    crud_service = CRUDService(connection, 'test_api_users')
    repository = UserRepository(
        crud_service,
        UserSerializer
    )
    return repository
