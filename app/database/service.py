from bson import ObjectId
from pymongo import MongoClient
from typing import Any, TypeVar


T = TypeVar('T')


class CRUDService:
    def __init__(self, conn: MongoClient, collecion: str) -> None:
        self._conn = conn
        self._collecion = collecion

    def create(self, new_item: T) -> object:
        return self._conn.local[self._collecion].insert_one(new_item)

    def get_by_id(self, id: str | ObjectId) -> object:
        id = ObjectId(id)
        return self._conn.local[self._collecion].find_one({'_id': id})

    def get_all(self, **kwargs) -> list[object]:
        if 'owner_id' in kwargs:
            cursor = self._conn.local[self._collecion].find({'owner_id': kwargs['owner_id']})
        else:
            cursor = self._conn.local[self._collecion].find({})
        return [item for item in cursor]

    def get_all_by_key(self, key: str, value: Any) -> list[object]:
        cursor = self._conn.local[self._collecion].find({key: value})
        return [item for item in cursor]

    def update_by_id(self, id: str | ObjectId, **update_data) -> object:
        id = ObjectId(id)
        return self._conn \
            .local[self._collecion] \
            .update_one({'_id': id}, {'$set': update_data})

    def delete_by_id(self, id: str | ObjectId) -> object:
        id = ObjectId(id)
        return self._conn.local[self._collecion].delete_one({'_id': id})
