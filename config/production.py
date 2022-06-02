from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x9b\x10`<\xb97\xec\xbd\x16+\xe5\xf2\x18\xe0\xf4\xd1'