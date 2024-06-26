from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

from app.database.service import CRUDService
from app.fileprocessor.service import TransactionFileProcessor
from app.schemas.transaction import Transaction
from app.serializers.transaction import TransactionSerializer


class TransactionRepository:
    def __init__(
        self,
        crud_service: CRUDService,
        file_processor: TransactionFileProcessor,
        serializer: TransactionSerializer
    ) -> None:
        self._crud_service = crud_service
        self._file_processor = file_processor
        self._serializer = serializer

    def create(self, new_transaction: Transaction | dict) -> dict:
        new_transaction_dict = dict(new_transaction)
        if len(new_transaction_dict) != 8:
            raise ValueError

        try:
            ObjectId(new_transaction_dict['owner_id'])
        except InvalidId:
            raise

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
        if set(new_transaction_dict.keys()) != valid_keys:
            raise ValueError

        inserted_id = self._crud_service.create(new_transaction_dict).inserted_id
        return self._serializer.serialize_one(
            self._crud_service.get_by_id(inserted_id)
        )

    def get_by_id(self, id: str | ObjectId) -> dict:
        try:
            id = ObjectId(id)
        except:
            raise

        transaction = self._crud_service.get_by_id(id)
        if not transaction:
            return {}

        return self._serializer.serialize_one(transaction)

    def get_all(self, **kwargs) -> list[dict]:
        return self._serializer.serialize_many(
            self._crud_service.get_all(**kwargs)
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

        deleted_transaction = self._crud_service.get_by_id(id)
        if not deleted_transaction:
            return {}

        self._crud_service.delete_by_id(deleted_transaction['_id'])

        return self._serializer.serialize_one(
            deleted_transaction
        )

    def calculate_portfolio(self, **kwargs) -> dict:
        transactions = self.get_all(**kwargs)
        if not transactions:
            return {}

        portfolio = {
            'investment': 0,
            'assets': {}
        }
        # group by assets
        for transaction in transactions:
            asset_data = portfolio['assets'].setdefault(
                transaction['asset'].upper(),
                {
                    'meta': {},
                    'transactions': []
                }
            )
            asset_data['transactions'].append(transaction)

        # calculate amount by asset
        # calculate investment by assets and overall
        # calculate avg price by asset
        for asset_data in portfolio['assets'].values():
            asset_amount = 0
            asset_investment = 0
            for transaction in asset_data['transactions']:
                if transaction['type'] == 'buy':
                    asset_amount += transaction['amount']
                    asset_investment += \
                        transaction['amount'] * transaction['historical_price']
                else:
                    asset_amount -= transaction['amount']

            asset_data['meta']['amount'] = asset_amount
            asset_data['meta']['investment'] = asset_investment
            if asset_amount != 0:
                asset_data['meta']['average_price'] = asset_investment / asset_amount
            else:
                asset_data['meta']['average_price'] = 0
            portfolio['investment'] += asset_investment

        return portfolio

    def import_csv(self, file: bytes) -> list:  # pragma: no cover
        if not self._file_processor:
            return []

        return self._file_processor.import_csv(file)


def get_transaction_repository():  # pragma: no cover
    connection = MongoClient()
    crud_service = CRUDService(connection, 'transactions')
    file_processor = TransactionFileProcessor()
    repository = TransactionRepository(
        crud_service,
        file_processor,
        TransactionSerializer
    )
    return repository


def get_test_transaction_repository():  # pragma: no cover
    connection = MongoClient()
    crud_service = CRUDService(connection, 'test_api_transactions')
    file_processor = TransactionFileProcessor()
    test_repository = TransactionRepository(
        crud_service,
        file_processor,
        TransactionSerializer
    )
    return test_repository
