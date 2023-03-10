import os
from decouple import config
from datetime import timedelta

BASE_DIR =  os.path.dirname(os.path.realpath(__file__))

class Config:
  SECRET_KEY = config('SECRET_KEY', 'secret')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=70000)
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=7000)
  JWT_SECRET_KEY = config('JWT_SECRET_KEY', 'sjhd863b8f7fjdhnjd')


class DevConfig(Config):
  DEBUG = True
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_TRACK_MODIFICATION = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')


class TestConfig(Config):
  TESTING = True
  DEBUG = True
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_TRACK_MODIFICATION = False
  SQLALCHEMY_DATABASE_URI = 'sqlite://' 
  

class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_TRACK_MODIFICATION = False
  DEBUG = config('DEBUG', False, cast=bool)

  
config_dict = {
  'dev': DevConfig,
  'test' : TestConfig,
  'prod' : ProdConfig
}