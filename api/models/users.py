from . import es_conn
from api.utils.config import Config


es = es_conn()
DOC_TYPE='users'

def get_user(email):
    try:
        return es.get(index='schools', doc_type=DOC_TYPE, id=email)
    except Exception:
        return {"found": False}

def store_user(data, email):
    
    return es.index(index=Config.INDEX_NAME, doc_type=DOC_TYPE, body=data, id=email)