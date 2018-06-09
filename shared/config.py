import os

#: database
DEV_DB_URI = 'mysql+pymysql://root:sige1995@localhost:3306/bbk-server?charset=utf8'
TEST_DB_URI = None
PROD_DB_URI = None

SERVER_DATABASE_URI = DEV_DB_URI
SPIDER_DATABASE_URI = 'mysql://root:sige1995@localhost:3306/bbk-spider?charset=utf8'
SPIDER_REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
}

#: secret key
DEV_SECRET_KEY = 'secretkeyfordev'
PROD_SECRET_KEY = os.getenv('BBK_SECRET_KEY') or None

#: algorithm core
NUM_OF_KEY_WORDS = 30
