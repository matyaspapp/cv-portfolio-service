from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

from app.database.service import CRUDService
from app.schemas.wallet import Wallet
from app.serializers.wallet import WalletSerializer


class WalletRepository:
    def __init__(
        self,
        crud_service: CRUDService,
        serializer: WalletSerializer
    ) -> None:
        self._crud_service = crud_service
        self._serializer = serializer

    def create(self, new_wallet: dict | Wallet) -> dict:
        new_wallet_dict = dict(new_wallet)
        if len(new_wallet_dict) != 3:
            raise ValueError

        try:
            ObjectId(new_wallet_dict['owner_id'])
        except InvalidId:
            raise

        valid_keys = {'owner_id', 'address', 'chain'}
        if set(new_wallet_dict.keys()) != valid_keys:
            raise ValueError

        inserted_id = self._crud_service.create(new_wallet_dict).inserted_id
        return self._serializer.serialize_one(
            self._crud_service.get_by_id(inserted_id)
        )

    def get_by_id(self, id: str | ObjectId) -> dict:
        try:
            id = ObjectId(id)
        except:
            raise

        wallet = self._crud_service.get_by_id(id)
        if not wallet:
            return {}

        return self._serializer.serialize_one(wallet)

    def get_all(self) -> list[dict]:
        return self._serializer.serialize_many(
            self._crud_service.get_all()
        )

    def update_by_id(self, id: str | ObjectId, update_data: dict) -> dict:
        if not isinstance(id, str) and not isinstance(id, ObjectId):
            raise TypeError

        id: ObjectId
        try:
            id = ObjectId(id)
        except:
            raise

        update_result = self._crud_service.update_by_id(
            id,
            **update_data
        )

        if not update_result.raw_result['updatedExisting']:
            return {}

        return self._serializer.serialize_one(
            self._crud_service.get_by_id(id)
        )

    def delete_by_id(self, id: str | ObjectId) -> dict:
        if not isinstance(id, str) and not isinstance(id, ObjectId):
            raise TypeError

        id: ObjectId
        try:
            id = ObjectId(id)
        except:
            raise

        deleted_wallet = self._crud_service.get_by_id(id)
        if not deleted_wallet:
            return {}

        self._crud_service.delete_by_id(deleted_wallet['_id'])

        return self._serializer.serialize_one(
            deleted_wallet
        )


def get_wallet_repository():  # pragma: no cover
    connection = MongoClient()
    crud_service = CRUDService(connection, 'wallets')
    repository = WalletRepository(
        crud_service,
        WalletSerializer
    )
    return repository


def get_test_wallet_repository():  # pragma: no cover
    connection = MongoClient()
    crud_service = CRUDService(connection, 'test_api_wallets')
    test_repository = WalletRepository(
        crud_service,
        WalletSerializer
    )
    return test_repository
