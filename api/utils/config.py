class Config(object):
    DEBUG = False
    TESTING = False
    API_KEY= "secret"
    INDEX_NAME= "schools"
    ES_HOST="localhost"
    ES_PORT=9200

class ProductionConfig(Config):
    ES_HOST="localhost"
    ES_PORT=9200

class DevelopmentConfig(Config):
    DEBUG = True
    ES_HOST="localhost"
    ES_PORT=9200


