"""Accounts REST API"""
from flask import jsonify, request, make_response, abort, url_for
from service import app
from service.common import status
from service.models import Account, DataValidationError


@app.route("/health")
def health():
    """Health probe"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


@app.route("/")
def index():
    """Root URL"""
    return jsonify(name="Account REST API Service", version="1.0",
                   paths=url_for("list_accounts", _external=True)), status.HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """CREATE an account"""
    app.logger.info("Request to create an Account")
    if request.content_type != "application/json":
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")
    account = Account()
    try:
        account.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    account.create()
    location_url = url_for("read_accounts", account_id=account.id, _external=True)
    return make_response(jsonify(account.serialize()), status.HTTP_201_CREATED,
                         {"Location": location_url})


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """LIST all accounts"""
    app.logger.info("Request to list Accounts")
    accounts = [account.serialize() for account in Account.all()]
    return make_response(jsonify(accounts), status.HTTP_200_OK)


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    """READ an account"""
    app.logger.info("Request to read Account %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return account.serialize(), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """UPDATE an account"""
    app.logger.info("Request to update Account %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    try:
        account.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    account.update()
    return account.serialize(), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """DELETE an account"""
    app.logger.info("Request to delete Account %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT
