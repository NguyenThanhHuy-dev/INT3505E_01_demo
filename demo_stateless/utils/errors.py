from flask import jsonify

class APIError(Exception):
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv
    
class NotFoundError(APIError):
    status_code = 404
        
class BadRequestError(APIError):
    status_code = 400
        
class UnauthorizedError(APIError):
    status_code = 401

class ConflictError(APIError):
    status_code = 409

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def handle_404_error(error):
        response = jsonify({'error': 'Resource not found'})
        response.status_code = 404
        return response
    
    @app.errorhandler(500)
    def handle_500_error(error):
        response = jsonify({'error': 'Internal server error'})
        response.status_code = 500
        return response