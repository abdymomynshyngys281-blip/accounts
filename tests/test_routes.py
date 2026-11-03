"""Tests for the Accounts REST API, security headers and CORS"""
import os
import unittest

os.environ["DATABASE_URI"] = "sqlite:///:memory:"

# pylint: disable=wrong-import-position
from service import app  # noqa: E402
from service.models import db, Account  # noqa: E402

HTTPS_ENVIRON = {"wsgi.url_scheme": "https"}
DATA = {"name": "Jane Doe", "email": "jane@example.com",
        "address": "1 Main St", "phone_number": "555-1234"}


class TestAccountService(unittest.TestCase):
    """Account service tests"""

    def setUp(self):
        db.session.query(Account).delete()
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()

    def _create(self):
        resp = self.client.post("/accounts", json=DATA, environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()

    def test_index(self):
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 200)

    def test_health(self):
        resp = self.client.get("/health", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.get_json()["status"], "OK")

    def test_create_account(self):
        data = self._create()
        self.assertEqual(data["name"], DATA["name"])

    def test_create_bad_data(self):
        resp = self.client.post("/accounts", json={"name": "x"}, environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 400)

    def test_create_bad_media_type(self):
        resp = self.client.post("/accounts", data="x", content_type="text/plain",
                                environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 415)

    def test_list_accounts(self):
        self._create()
        self._create()
        resp = self.client.get("/accounts", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(len(resp.get_json()), 2)

    def test_read_account(self):
        acc = self._create()
        resp = self.client.get(f"/accounts/{acc['id']}", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["email"], DATA["email"])

    def test_read_not_found(self):
        resp = self.client.get("/accounts/0", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 404)

    def test_update_account(self):
        acc = self._create()
        acc["name"] = "John Doe"
        resp = self.client.put(f"/accounts/{acc['id']}", json=acc, environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "John Doe")

    def test_update_not_found(self):
        resp = self.client.put("/accounts/0", json=DATA, environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 404)

    def test_update_bad_data(self):
        acc = self._create()
        resp = self.client.put(f"/accounts/{acc['id']}", json={"x": 1}, environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 400)

    def test_delete_account(self):
        acc = self._create()
        resp = self.client.delete(f"/accounts/{acc['id']}", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get(f"/accounts/{acc['id']}", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 404)

    def test_method_not_allowed(self):
        resp = self.client.delete("/accounts", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, 405)

    def test_security_headers(self):
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(resp.headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'self'", resp.headers["Content-Security-Policy"])
        self.assertEqual(resp.headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_cors_header(self):
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.headers["Access-Control-Allow-Origin"], "*")
