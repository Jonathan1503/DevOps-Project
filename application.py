from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from database import db
from api import BlacklistResource

application = Flask(__name__)
application.config.from_object("config")

db.init_app(application)

jwt = JWTManager(application)

api = Api(application)
api.add_resource(BlacklistResource, "/blacklists", "/blacklists/<string:email>")

with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(debug=True)
