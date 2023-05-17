import os
import secrets
from flask import Flask, request,jsonify
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager
import models
from flask_migrate import Migrate
from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None, username=None):
    # 'app' variable name should be same as file name bcz when flask will run app.py will find app variable in the file....
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTION"]=True
    app.config["API_TITLE"]="Stores REST API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/" #tell flask smorest where is the root of the api is it is "/" bcz all end point start with that

    # tell flask smorest to use "swagger" for api documentation
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://pswd:usernamet@localhost/db_flask'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    #it initializes flask sqlalchemy extention giving it app
    #so it can connect flask app to flask alchemy
    db.init_app(app)

    #since,we will be using flask-migrate to create our database table,we no longer need SqlAlchemy to do it::
    #Migrate detects changes in physical schema of database such as column,table,primarykey,index..
    migrate=Migrate(app,db)

    # it connect flask smorest extension to flask app:
    api = Api(app)

    #secret key is used to signing the jwt:: it is not same as encryption::
    # this secret key is also not safe as when user finds the secret key it can make its own secret key and pretend that we have created it::
    #to prevent it we will use secret generation software
    #prevent taampering with jwt
    app.config["JWT_SECRET_KEY"]="46443399168257834094863925095482929428"
    jwt=JWTManager(app)

    #jwt claim let us add extra information than the actual subject:::rarely used::check user admin
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identify):
    #     #Look in the databse and see whether the user is a admin
    #     if identify==1:
    #         return {"is_admin":True}
    #     return {"is_admin":False}

    #expect a fresh token but receive a non-fresh token
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "description":"The token has been revoked","error":"token_revoked"
                }
            ),401
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        #if this return true user will that token has been revoked or no longer used ,and request will not be generates
        #jti will be checked against the blocklist
        return jwt_payload["jti"]in BLOCKLIST


    #error msg for blocklist token,it will return when check_if_token_in_blocklist returns true
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"description":"The token has been revoked","error":"token_revoked"}),401
        )

    @jwt.expired_token_loader #it is a decorator function
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"message":"Token has expired","error":"token_expired"}),401
        )

    @jwt.invalid_token_loader  # it is a decorator function
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
        )

    @jwt.unauthorized_loader  # it is a decorator function
    def missing_token_callback(error):
        #here we are changing pre defined error message
        return (
            jsonify({"message": "Request does not contain an access token", "error": "authorization_requied"}), 401
        )

    #it will run if table does not exists
    #it know which table to create as we imported models
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
