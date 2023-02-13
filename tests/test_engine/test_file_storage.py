#!/usr/bin/python3
"""
Modules contains tests for the FileStorage class
"""
import json
import os
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """
    Tests the FileStorage class
    """
    def setUp(self):
        self.store = FileStorage()

    def test_init(self):
        self.assertTrue(isinstance(self.store.all(), dict))

    def test_new(self):
        old_length = len(self.store.all())
        new = BaseModel()
        self.assertGreater(len(self.store.all()), old_length)
        key = "BaseModel.{}".format(new.id)
        self.assertTrue(key in self.store.all())
        self.store.all().pop(key)

    def test_save(self):
        self.store.save()
        with open("./file.json", "a+", encoding="utf-8") as file:
            file.seek(0, 0)
            test_str = file.read()
        test_dict = json.loads(test_str)
        expected = {}
        for key, value in self.store.all().items():
            expected[key] = value.to_dict()
        self.assertEqual(len(test_dict), len(expected))

    def test_reload(self):
        test_dict = {
            key: BaseModel(
                **value.to_dict()) for key, value in self.store.all().items()}
        length = len(self.store.all())
        for i in range(length):
            self.store.all().popitem()
        self.store.reload()
        self.assertEqual(len(self.store.all()), length)
