from config.default import *
import os
from dotenv import load_dotenv
<<<<<<< HEAD
import flask_sqlalchemy
import MySQLdb
import pymysql
# pymysql.install_as_MYSQLdb()
=======
# import MySQLdb
# # import pymysql
# # pymysql.install_as_MYSQLdb()
>>>>>>> a2204c9a7db45d59abbad38eff1e5e4d0d617b07

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x1a\xdf3\x07\x8e\x9br/\x90\xb6B\x91I!C\xfa'

load_dotenv(os.path.join(BASE_DIR, '.env'))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@{url}/{db}'.format(
    user=os.getenv('DB_USER'),
    pw=os.getenv('DB_PASSWORD'),
    url=os.getenv('DB_HOST'),
    db=os.getenv('DB_NAME'),
    port=3306,
    charset='utf8')

