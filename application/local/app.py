import time
import socket
import redis
import getpass
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)


app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
    config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['REDIS_HOST'] = config.REDIS_HOST
app.config['REDIS_PORT'] = config.REDIS_PORT
app.config['DEBUG'] = config.DEBUG
app.config['TESTING'] = False
app.config['LISTENING_HOST'] = config.LISTENING_HOST
app.config['LISTENING_PORT'] = config.LISTENING_PORT

cache = redis.Redis(
    host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"])
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(25), unique=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def get_hit_count():
    retries = 5
    server_name = socket.gethostname()
    while True:
        try:
            return cache.incr(server_name)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/add_user", methods=["GET"])
def add_user():
    current_user = getpass.getuser()
    server_name = socket.gethostname()
    try:
        new_user = \
            User(current_user, '{}@{}'.format(current_user, server_name))
        db.session.add(new_user)
        db.session.commit()
        return "Success."
    except IntegrityError:
        return "User already exists."


# endpoint to show all users
@app.route("/users", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return '{}.\n'.format(result.data)


@app.route('/')
def hello():
    count = get_hit_count()
    server_name = socket.gethostname()
    return 'This is {} I have been seen {} times.\n'.format(server_name, count)


if __name__ == "__main__":
    app.run(host=app.config["LISTENING_HOST"],
            port=int(app.config["LISTENING_PORT"]))
