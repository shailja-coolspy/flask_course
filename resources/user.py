from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import UserSchema
from models import UserModel
from passlib.hash import pbkdf2_sha256
from db import db
from blocklist import BLOCKLIST
#create access token is set of characters and numbers that we are going to generate in the server
#if client sends correct username and password then we will send access token
from flask_jwt_extended import create_access_token,get_jwt,jwt_required,create_refresh_token,get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp=Blueprint("Users",__name__,description="Operation on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409,message="A user with that user name already exits")

        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message":"User creaed successfuly"},201

#note-in refresh token instead of asking user to re login and re authenticate using username and password ,
#client will do it automatically by refreshing the token
#non-refresh token will have access to some end points such as viewing post feed
#access token will have access to importent end points such as delete account



@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=UserModel.query.filter(
            UserModel.username==user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            #fresh token was generated from login in::
            access_token=create_access_token(identity=user.id,fresh=True)
            refresh_token=create_refresh_token(identity=user.id)
            return {"access_token":access_token,"refresh_token":refresh_token}

        abort(401,message="Inavalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        #it return non if there is no current user
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        #this generates one non-fresh token for every refresh token
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        #when we /login we get refresh token that is copied and put into /refresh end point in header then on pressing send it generate "access_token"
        #in /login access token we will have fresh=true
        #and in /refresh access token we will have fresh=false
        #this is done to detect type of token we have got i.e access token or non refesh token
        return {"access_token":new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out."}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user

    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted"},200