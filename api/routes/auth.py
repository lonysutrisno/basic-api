from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import credential
from api.services import auth_service
import api.utils.responses as resp
import json
from schema import Schema, And, Use, Optional, Regex, SchemaError


from pprint import pprint


auth = Blueprint("auth", __name__)

@auth.route('/get-token',methods=["POST"])
def get_token():
    try:
        if credential.check_apikey(request) == False:
            return response_with(resp.UNAUTHORIZED_403, value={"data": "invalid x-api-key"})    
            
        email = request.get_json().get('email')
        password = request.get_json().get('password')
        data = auth_service.get_user_by_email(email)

        if data.get("found") == True:
            if credential.check_password(password, json.dumps(data.get("_source").get("password")).strip('"')):
                token = credential.create_token(email)
                return response_with(resp.SUCCESS_200, value={"data": token})
            else:
                return response_with(resp.UNAUTHORIZED_403, value={"data": "invalid password"})    
        else:
            return response_with(resp.UNAUTHORIZED_403, value={"data": "invalid email"})    
            
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

@auth.route('/register',methods=["POST"])
def register():
    try:
        if credential.check_apikey(request) == False:
            return response_with(resp.UNAUTHORIZED_403, value={"data": "invalid x-api-key"}) 
        
        # validation
        try:
            Regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").validate(request.get_json().get("email"))
            Schema({'name': And(str),
                    'email':  And(str),
                    'password':  And(str)
                    }).validate(request.get_json())    
        except SchemaError:
            return response_with(resp.INVALID_INPUT_422)

        data = auth_service.store_user(request.get_json())
        if data=="Email Already Exist":
            return response_with(resp.BAD_REQUEST_400, value={"data": "Email Already Exist"})    
        token = credential.create_token(request.get_json().get("email"))
        return response_with(resp.SUCCESS_200, value={
            "data": data,
            "token":token
            })
            
    except Exception:
        return response_with(resp.INVALID_INPUT_422)
