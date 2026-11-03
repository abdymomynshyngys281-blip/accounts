"""JSON error handlers"""
from flask import jsonify
from service import app
from service.common import status


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handle 404"""
    return jsonify(status=404, error="Not Found", message=str(error)), 404


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    """Handle 405"""
    return jsonify(status=405, error="Method not Allowed", message=str(error)), 405


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handle 400"""
    return jsonify(status=400, error="Bad Request", message=str(error)), 400
