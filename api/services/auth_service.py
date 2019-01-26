from api.models import users
from pprint import pprint
import datetime
import bcrypt

def get_user_by_email(email):
    return users.get_user(email)

def store_user(data):
    email = data.get("email")
       
    del data["email"]
    data["created_at"] = f"{datetime.datetime.now():%Y-%m-%d}"
    data["password"] = bcrypt.hashpw(data["password"].encode('utf8'), bcrypt.gensalt()).decode("utf8")

    res = get_user_by_email(email)
    if res.get("found") == True:
        return "Email Already Exist"
    return users.store_user(data, email)