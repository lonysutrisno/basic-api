import jwt
from .config import Config
from datetime import datetime, timedelta

import bcrypt
import json


JWT_SECRET = Config.API_KEY
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_MINUTES = 30

def create_token(str):
    payload = {
        'email': str,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXP_DELTA_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

def check_apikey(request):
    api_key = request.headers.get("x-api-key")
    if api_key != Config.API_KEY:
        return False
    else:
        return True