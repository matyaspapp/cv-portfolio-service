from bson import ObjectId
from bson.errors import InvalidId

from app.database.service import CRUDService
from app.serializers.transaction import TransactionSerializer


class TransactionRepository:
    def __init__(
        self,
        crud_service: CRUDService,
        serializer: TransactionSerializer
    ) -> None:
        self._crud_service = crud_service
        self._serializer = serializer

    def create(self, new_transaction: dict) -> str:
        if len(new_transaction) != 8:
            raise ValueError

        try:
            ObjectId(new_transaction['owner_id'])
        except InvalidId:
            raise ValueError

        valid_keys = {
            'owner_id',
            'asset',
            'amount',
            'historical_price',
            'currency',
            'tags',
            'date',
            'type'
        }
        if set(new_transaction.keys()) != valid_keys:
            raise ValueError

        inserted_id = self._crud_service.create(new_transaction).inserted_id
        return self._serializer.serialize_one(
            self._crud_service.get_by_id(inserted_id)
        )

    def get_by_id(self, id: str | ObjectId) -> dict:
        try:
            id = ObjectId(id)
        except:
            raise ValueError

        transaction = self._crud_service.get_by_id(id)
        if not transaction:
            return {}

        return self._serializer.serialize_one(transaction)

    def get_all(self) -> list[dict]:
        return self._serializer.serialize_many(
            self._crud_service.get_all()
        )

    def get_all_by_asset(self, asset: str) -> list[dict]:
        return self._serializer.serialize_many(
            self._crud_service.get_all_by_key('asset', asset)
        )

    def get_all_by_tag(self, tag: str) -> list[dict]:
        return self._serializer.serialize_many(
            self._crud_service.get_all_by_key('tags', {'$in': [tag]})
        )

    def update_by_id(self, id: str | ObjectId, update_data: dict) -> dict:
        id: ObjectId
        try:
            id = ObjectId(id)
        except:
            raise ValueError

        update_result = self._crud_service.update_by_id(
            id,
            **update_data
        )

        if not update_result.raw_result['updatedExisting']:
            return {}

        return self._serializer.serialize_one(
            self._crud_service.get_by_id(id)
        )
