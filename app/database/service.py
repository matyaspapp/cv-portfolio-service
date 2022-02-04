from bson import ObjectId
from pymongo import MongoClient
from typing import TypeVar


T = TypeVar('T')


class CRUDService:
    def __init__(self, conn: MongoClient, collecion: str) -> None:
        self._conn = conn
        self._collecion = collecion

    def create(self, new_item: T) -> object:
        return self._conn.local[self._collecion].insert_one(new_item)

    def get_by_id(self, id: ObjectId) -> T:
        return self._conn.local[self._collecion].find_one({'_id': id})

    def get_all(self) -> list[T]:
        cursor = self._conn.local[self._collecion].find({})
        return [item for item in cursor]

    def update_by_id(self, id: ObjectId, **update_data) -> object:
        return self._conn \
            .local[self._collecion] \
            .update_one({'_id': id}, {'$set': update_data})

    def delete_by_id(self, id: ObjectId) -> object:
        return self._conn.local[self._collecion].delete_one({'_id': id})
