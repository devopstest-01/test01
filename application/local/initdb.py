from app import db
import sqlalchemy
import config

engine = sqlalchemy.create_engine('mysql+pymysql://{}:{}@{}'.format(
    config.MYSQL_DB_USER, config.MYSQL_DB_PASSWORD, config.MYSQL_DB_HOST))
engine.execute('CREATE DATABASE IF NOT EXISTS {}'.format(config.MYSQL_DB_NAME))
engine.execute('USE {}'.format(config.MYSQL_DB_NAME))
db.create_all()
