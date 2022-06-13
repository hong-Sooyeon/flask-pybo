from config.default import *
import os
from dotenv import load_dotenv


SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x1a\xdf3\x07\x8e\x9br/\x90\xb6B\x91I!C\xfa'

# load_dotenv(os.path.join(BASE_DIR, '.env'))
#
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pw}@{url}/{db}'.format(
#     user=os.getenv('DB_USER'),
#     pw=os.getenv('DB_PASSWORD'),
#     url=os.getenv('DB_HOST'),
#     db=os.getenv('DB_NAME'),
#     charset='utf8')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbmasteruser:j8|hud}_WioM=M!&FBqRi%Pb[YcN[}@ls-f5684312acf8e1f5b0e0028773096ee66afe8f1d.cwqxrr7go7ko.ap-northeast-2.rds.amazonaws.com/hconnect'
