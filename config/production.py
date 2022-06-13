from config.default import *
import os
from dotenv import load_dotenv
import MySQLdb
import pymysql
pymysql.install_as_MYSQLdb()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x1a\xdf3\x07\x8e\x9br/\x90\xb6B\x91I!C\xfa'

load_dotenv(os.path.join(BASE_DIR, '.env'))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@{url}/{db}'.format(
    user=os.getenv('DB_USER'),
    pw=os.getenv('DB_PASSWORD'),
    url=os.getenv('DB_HOST'),
    db=os.getenv('DB_NAME'))

