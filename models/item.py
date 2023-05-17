from db import db

#This noe become mapping btw row in a table to a python class therefore python object
class ItemModel(db.Model):

    #It tell sqlachlemy that we want to create or use table called item for this clasas and all object in this class
    __tablename__="items"

    #Column:
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    price=db.Column(db.Float(precision=2),unique=False,nullable=False)
    #one to many relations
    #one store_id is associated to mant items
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False,nullable=False)
    store=db.relationship("StoreModel",back_populates="item")
    #back_populate "items" attribute must match in TagModel i.e there must be attribute named "items"
    tags=db.relationship("TagModel",back_populates="items",secondary="items_tags")
