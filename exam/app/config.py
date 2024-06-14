import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2592_exam:12345678@std-mysql.ist.mospolytech.ru/std_2592_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media', 'images')
ADMIN_ROLE_ID = 1
MODER_ROLE_ID = 2
PER_PAGE = 10

