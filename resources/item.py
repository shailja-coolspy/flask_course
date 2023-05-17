import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import ItemSchema,ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required,get_jwt


blp=Blueprint("items",__name__,description="Operation on item")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    # get request to get specific item information
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        #if the item is found it will return item or if not found then it will return 404 error
        #no need to error handle seprately
        item=ItemModel.query.get_or_404(item_id)
        return item

    # delete request to delete specific item
    @jwt_required()
    def delete(self,item_id):
        # #check for admin ::
        # jwt=get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401,message="Admin privilege required")
        #404 error when item does not exits
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted"}
        #error when item does exits and not able to delete
        # raise NotImplementedError("Deleting an item is not implemented")


    # put request to update a specific item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)#return
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price=item_data["price"]
            item.name=item_data["name"]
        else:
            item=ItemModel(**item_data,id=item_id)
        db.session.add(item)
        db.session.commit()
        return item

@blp.route("/item")
class ItemList(MethodView):
    # post request for creating new item for particular store
    #it require a fresh token
    @jwt_required(fresh=True)#you can not call this end point unless we send a jwt
    @blp.arguments(ItemSchema)#marshmallow
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item=ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured while inserting item.")

        return item, 201

    # get request for all items:
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
