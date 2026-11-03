"""Tests for the Account model"""
import os
import unittest

os.environ["DATABASE_URI"] = "sqlite:///:memory:"

# pylint: disable=wrong-import-position
from service import app  # noqa: E402,F401
from service.models import db, Account, DataValidationError  # noqa: E402


class TestAccountModel(unittest.TestCase):
    """Model tests"""

    def setUp(self):
        db.session.query(Account).delete()
        db.session.commit()

    def test_crud(self):
        acc = Account(name="A", email="a@b.c")
        acc.create()
        self.assertIsNotNone(acc.id)
        acc.name = "B"
        acc.update()
        self.assertEqual(Account.find(acc.id).name, "B")
        self.assertEqual(len(Account.all()), 1)
        acc.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_update_no_id(self):
        with self.assertRaises(DataValidationError):
            Account(name="A", email="a@b.c").update()

    def test_deserialize_missing(self):
        with self.assertRaises(DataValidationError):
            Account().deserialize({"name": "x"})

    def test_deserialize_bad_date(self):
        with self.assertRaises(DataValidationError):
            Account().deserialize({"name": "x", "email": "y", "date_joined": "nope"})

    def test_serialize_repr(self):
        acc = Account().deserialize({"name": "x", "email": "y", "date_joined": "2024-01-02"})
        self.assertEqual(acc.serialize()["date_joined"], "2024-01-02")
        self.assertIn("x", repr(acc))
