import unittest

from bson import ObjectId
from typing import TypeVar

from app.database.service import CRUDService
from tests.database.settings import TEST_CONN, TEST_COLLECTION, TEST_ITEM
from tests.utils import tag


T = TypeVar('T')


class CRUDServiceTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self._service = CRUDService(TEST_CONN, TEST_COLLECTION)

    def _create(self, new_item) -> T:
        return TEST_CONN.local[TEST_COLLECTION].insert_one(new_item)

    def _get_all(self) -> list[T]:
        cursor = TEST_CONN.local[TEST_COLLECTION].find({})
        return [item for item in cursor]

    def _get_by_id(self, id: ObjectId) -> T:
        return TEST_CONN.local[TEST_COLLECTION].find_one({'_id': id})

    def setUp(self) -> None:
        super().setUp()
        method = getattr(self, self._testMethodName)
        tags = getattr(method, 'tags', {})
        if 'skip_setup' in tags:
            return
        self._testitem = self._create(TEST_ITEM)

    def tearDown(self) -> None:
        super().tearDown()
        TEST_CONN.local[TEST_COLLECTION].drop()

    # ---  TEST SERVICE  ---
    @tag('skip_setup')
    def test_create(self) -> None:
        result = self._service.create({'foo': 'bar'})
        new_item, = self._get_all()

        self.assertNotEqual(new_item, None)
        self.assertEqual(new_item['_id'], result.inserted_id)
        self.assertEqual(new_item['foo'], 'bar')

    def test_get_by_id(self) -> None:
        test_item = self._service.get_by_id(self._testitem.inserted_id)

        self.assertNotEqual(test_item, None)
        self.assertEqual(test_item['test'], TEST_ITEM['test'])

    def test_get_all(self) -> None:
        self._create({'test': 'item2'})
        items_test = self._get_all()
        items_service = self._service.get_all()

        items_test.sort(key=lambda item: item['test'])
        items_service.sort(key=lambda item: item['test'])

        self.assertEqual(items_test, items_service)

    def test_update_by_id(self) -> None:
        updated_item = {'test': 'updated_item'}
        self._service.update_by_id(self._testitem.inserted_id, **updated_item)

        updated_item.update({'_id': self._testitem.inserted_id})
        test_item = self._get_by_id(self._testitem.inserted_id)

        self.assertEqual(updated_item, test_item)

    def test_delete_by_id(self) -> None:
        result = self._service.delete_by_id(self._testitem.inserted_id)
        items = self._get_all()

        self.assertEqual(result.deleted_count, 1)
        self.assertEqual(items, [])
