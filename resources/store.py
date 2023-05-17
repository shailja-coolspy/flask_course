import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp=Blueprint("stores",__name__,description="Operation on store")

@blp.route("/store/<int:store_id>")#end point
class Store(MethodView):
    # get request to get information of a specific store
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store

    # delete request to delete specific store
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted"}


#Flask smorest connects this with flask method view
#we have different method view for different end points

@blp.route("/store")
class StoreList(MethodView):
    # get request for all store :
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    # post request for creating new store:
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
            #unique name error::
        except IntegrityError:
            abort(400,message="A store with that name already exits.")
        except SQLAlchemyError:
            abort(500, message="An error occured while creating store.")
        return store