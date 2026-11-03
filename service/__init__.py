"""Flask app factory for the Accounts service"""
import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object("service.config")

# Security headers (Talisman) and CORS policies
talisman = Talisman(app, force_https=os.getenv("FORCE_HTTPS", "true").lower() == "true")
CORS(app)

# pylint: disable=wrong-import-position
from service import routes, models  # noqa: E402,F401
from service.common import error_handlers  # noqa: E402,F401

models.init_db(app)
app.logger.info("Accounts service initialized", extra={"python": sys.version})
