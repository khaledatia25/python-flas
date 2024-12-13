from functools import wraps
from flask import request, jsonify
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"message": "Token is missing!"}, 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, "your_secret_key", algorithms=['HS256'])
            current_user = {"id": data['user_id']}
        except:
            return {"message": "Invalid token!"}, 401
        return f(current_user, *args, **kwargs)
    return decorated
