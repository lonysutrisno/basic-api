from elasticsearch import Elasticsearch
from .config import Config


def create_es_conn():

    es = Elasticsearch([
        {'host': Config.ES_HOST,'port': Config.ES_PORT}
    ])
    return es