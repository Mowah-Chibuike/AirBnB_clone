#!/usr/bin/python3
"""
Tests for BaseModel class
"""
from uuid import uuid4
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Tests for BaseModel Class
    """
    def setUp(self):
        self.base = BaseModel()

    def test_init(self):
        self.assertNotEqual(self.base.id, str(uuid4()))
        self.assertTrue(isinstance(self.base.id, str))
        self.assertEqual(self.base.created_at, self.base.updated_at)

    def test_save(self):
        before = self.base.updated_at
        self.base.save()
        self.assertGreater(self.base.updated_at, before)

    def test_to_dict(self):
        expected = {
            "id": self.base.id,
            "created_at": self.base.created_at.isoformat(),
            "updated_at": self.base.updated_at.isoformat(),
            "__class__": "BaseModel"
        }
        self.assertEqual(self.base.to_dict(), expected)

    def test_create_from_dict(self):
        expected = self.base.to_dict()
        new = BaseModel(**expected)
        self.assertFalse(new is self.base)
        self.assertTrue(new.__dict__ == self.base.__dict__)
        self.assertEqual(new.to_dict(), expected)
